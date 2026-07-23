#!/usr/bin/env node
/**
 * Long-lived UGCAskQ MCP HTTP proxy.
 *
 * This is NOT an MCP server for Codex to register. It keeps a long SSE
 * connection to the editor UGCAskQ MCP endpoint and exposes plain local HTTP
 * endpoints so Codex or any script can call MCP without using Codex's MCP tool
 * bus.
 *
 * Start:
 *   node C:\\Users\\ASUS\\.codex\\ugcaskq-proxy-server.js
 *
 * Examples:
 *   curl http://127.0.0.1:18763/health
 *   curl http://127.0.0.1:18763/tools
 *   curl "http://127.0.0.1:18763/read?uri=ctx:"
 *   curl -X POST http://127.0.0.1:18763/py -H "Content-Type: application/json" -d "{\"code\":\"print('hello')\"}"
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const SSE_URL = process.env.UGCASKQ_SSE_URL || 'http://127.0.0.1:12463/sse';
const HOST = process.env.UGCASKQ_PROXY_HOST || '127.0.0.1';
const PORT = Number(process.env.UGCASKQ_PROXY_PORT || 18763);
const LOG_FILE = process.env.UGCASKQ_PROXY_LOG || path.join(process.env.USERPROFILE || '.', '.codex', 'tmp', 'ugcaskq-proxy-server.log');
const RPC_TIMEOUT_MS = Number(process.env.UGCASKQ_PROXY_RPC_TIMEOUT_MS || 120000);
const RECONNECT_DELAY_MS = Number(process.env.UGCASKQ_PROXY_RECONNECT_DELAY_MS || 1500);

let nextId = 1;
let postEndpoint = null;
let sseReq = null;
let sseRes = null;
let state = 'idle';
let initialized = false;
let connectingPromise = null;
let reconnectTimer = null;
let lastError = null;
let connectedAt = null;
let connectionGeneration = 0;
const pending = new Map();

function log(message, extra) {
  try {
    fs.mkdirSync(path.dirname(LOG_FILE), { recursive: true });
    const suffix = extra === undefined ? '' : ` ${safeStringify(extra).slice(0, 2000)}`;
    fs.appendFileSync(LOG_FILE, `${new Date().toISOString()} ${message}${suffix}\n`, 'utf8');
  } catch (_) {}
}

function safeStringify(value) {
  try { return JSON.stringify(value); } catch (_) { return String(value); }
}

function jsonResponse(res, statusCode, payload) {
  const body = JSON.stringify(payload, null, 2);
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Length': Buffer.byteLength(body),
  });
  res.end(body);
}

function textFromMcpResult(result) {
  if (!result || !Array.isArray(result.content)) return '';
  return result.content.map((item) => {
    if (!item) return '';
    if (item.type === 'text') return item.text || '';
    return safeStringify(item);
  }).filter(Boolean).join('\n');
}

function rejectAllPending(reason) {
  for (const [id, item] of pending.entries()) {
    pending.delete(id);
    item.reject(reason);
  }
}

function clearConnection(reason) {
  state = 'disconnected';
  initialized = false;
  postEndpoint = null;
  connectedAt = null;
  const err = reason instanceof Error ? reason : new Error(String(reason || 'connection closed'));
  lastError = err.message;
  rejectAllPending(err);
  try { if (sseReq) sseReq.destroy(); } catch (_) {}
  try { if (sseRes) sseRes.destroy(); } catch (_) {}
  sseReq = null;
  sseRes = null;
}

function scheduleReconnect() {
  if (reconnectTimer) return;
  reconnectTimer = setTimeout(() => {
    reconnectTimer = null;
    ensureReady().catch((err) => log('background reconnect failed', { error: err.message }));
  }, RECONNECT_DELAY_MS);
}

function connectSSE() {
  const generation = ++connectionGeneration;
  state = 'connecting';
  initialized = false;
  postEndpoint = null;
  lastError = null;
  log('connecting sse', { url: SSE_URL, generation });

  return new Promise((resolve, reject) => {
    let endpointResolved = false;
    let settled = false;
    const url = new URL(SSE_URL);

    const req = http.get({
      hostname: url.hostname,
      port: url.port || 80,
      path: `${url.pathname}${url.search}`,
      headers: { Accept: 'text/event-stream' },
    }, (res) => {
      sseRes = res;
      if (res.statusCode !== 200) {
        const err = new Error(`SSE HTTP ${res.statusCode}`);
        lastError = err.message;
        settled = true;
        reject(err);
        res.resume();
        return;
      }

      let buf = '';
      let eventType = 'message';
      let dataLines = [];

      function resolveEndpoint(value) {
        if (endpointResolved) return;
        endpointResolved = true;
        postEndpoint = value;
        state = 'connected';
        connectedAt = new Date().toISOString();
        log('sse endpoint', { endpoint: value, generation });
        if (!settled) {
          settled = true;
          resolve(value);
        }
      }

      function dispatch() {
        if (!dataLines.length) return;
        const data = dataLines.join('\n').trim();
        dataLines = [];
        if (!data) return;

        if (eventType === 'endpoint') {
          resolveEndpoint(data);
          return;
        }

        try {
          const msg = JSON.parse(data);
          log('sse message', { id: msg.id, method: msg.method, hasResult: !!msg.result, hasError: !!msg.error });
          if (msg.id !== undefined && pending.has(msg.id)) {
            const item = pending.get(msg.id);
            pending.delete(msg.id);
            item.resolve(msg);
          }
        } catch (err) {
          log('sse parse ignored', { error: err.message, data: data.slice(0, 500) });
        }
      }

      res.on('data', (chunk) => {
        buf += chunk.toString('utf8');
        const lines = buf.split(/\r?\n/);
        buf = lines.pop();
        for (const line of lines) {
          if (line === '') {
            dispatch();
            eventType = 'message';
            dataLines = [];
          } else if (line.startsWith(':')) {
            // heartbeat/comment
          } else if (line.startsWith('event:')) {
            eventType = line.slice(6).trim() || 'message';
          } else if (line.startsWith('data:')) {
            dataLines.push(line.slice(5).replace(/^ /, ''));
          }
        }
      });

      res.on('error', (err) => {
        log('sse response error', { error: err.message });
        if (!endpointResolved && !settled) {
          settled = true;
          reject(err);
        }
      });

      res.on('close', () => {
        if (generation !== connectionGeneration) return;
        log('sse closed', { pending: pending.size, endpointResolved, initialized });
        clearConnection('SSE connection closed');
        if (!endpointResolved && !settled) {
          settled = true;
          reject(new Error('SSE connection closed before endpoint event'));
        }
        scheduleReconnect();
      });
    });

    sseReq = req;
    req.on('error', (err) => {
      log('sse request error', { error: err.message });
      lastError = err.message;
      if (!settled) {
        settled = true;
        reject(err);
      }
      if (generation === connectionGeneration) {
        clearConnection(err);
        scheduleReconnect();
      }
    });
    req.setTimeout(15000, () => req.destroy(new Error('SSE connect timeout')));
  });
}

function postJson(msg) {
  return new Promise((resolve, reject) => {
    if (!postEndpoint) {
      reject(new Error('No SSE POST endpoint received'));
      return;
    }
    const base = new URL(SSE_URL);
    const postUrl = new URL(postEndpoint, base);
    const body = JSON.stringify(msg);
    const req = http.request({
      hostname: postUrl.hostname,
      port: postUrl.port || 80,
      path: `${postUrl.pathname}${postUrl.search}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    }, (res) => {
      res.resume();
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) resolve();
        else reject(new Error(`POST HTTP ${res.statusCode}`));
      });
    });
    req.on('error', reject);
    req.setTimeout(15000, () => req.destroy(new Error('POST timeout')));
    req.write(body);
    req.end();
  });
}

async function rpc(method, params, notification = false) {
  if (!postEndpoint && method !== 'initialize') await ensureReady();
  const msg = notification ? { jsonrpc: '2.0', method, params } : { jsonrpc: '2.0', id: nextId++, method, params };
  log('rpc send', { id: msg.id, method });
  if (notification) {
    await postJson(msg);
    return null;
  }

  const wait = new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      pending.delete(msg.id);
      reject(new Error(`Timeout waiting for ${method}`));
    }, RPC_TIMEOUT_MS);
    pending.set(msg.id, {
      resolve: (value) => {
        clearTimeout(timer);
        resolve(value);
      },
      reject: (err) => {
        clearTimeout(timer);
        reject(err);
      },
    });
  });
  await postJson(msg);
  const response = await wait;
  if (response.error) {
    throw new Error(`${method} failed: ${response.error.message || safeStringify(response.error)}`);
  }
  return response.result;
}

async function initializeMcp() {
  await connectSSE();
  const init = await rpc('initialize', {
    protocolVersion: '2024-11-05',
    capabilities: {},
    clientInfo: { name: 'ugcaskq-http-proxy', version: '1.0.0' },
  });
  await rpc('notifications/initialized', {}, true);
  initialized = true;
  state = 'ready';
  log('initialized', { serverInfo: init && init.serverInfo });
  return init;
}

async function ensureReady() {
  if (initialized && postEndpoint && state === 'ready') return;
  if (connectingPromise) return connectingPromise;
  connectingPromise = initializeMcp().finally(() => {
    connectingPromise = null;
  });
  return connectingPromise;
}

async function callTool(name, args) {
  await ensureReady();
  return rpc('tools/call', { name, arguments: args || {} });
}

async function readBodyJson(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  const text = Buffer.concat(chunks).toString('utf8').trim();
  if (!text) return {};
  try { return JSON.parse(text); } catch (err) {
    const e = new Error(`Invalid JSON body: ${err.message}`);
    e.statusCode = 400;
    throw e;
  }
}

async function handleRequest(req, res) {
  if (req.method === 'OPTIONS') {
    jsonResponse(res, 200, { ok: true });
    return;
  }

  const url = new URL(req.url, `http://${HOST}:${PORT}`);
  try {
    if (req.method === 'GET' && url.pathname === '/health') {
      jsonResponse(res, 200, {
        ok: true,
        state,
        initialized,
        sseUrl: SSE_URL,
        proxy: `http://${HOST}:${PORT}`,
        connectedAt,
        pending: pending.size,
        lastError,
        logFile: LOG_FILE,
      });
      return;
    }

    if (req.method === 'GET' && url.pathname === '/tools') {
      await ensureReady();
      const result = await rpc('tools/list', {});
      jsonResponse(res, 200, { ok: true, result });
      return;
    }

    if (req.method === 'GET' && url.pathname === '/read') {
      const queries = [
        ...url.searchParams.getAll('uri'),
        ...url.searchParams.getAll('q'),
        ...url.searchParams.getAll('query'),
      ].filter(Boolean);
      if (!queries.length) {
        jsonResponse(res, 400, { ok: false, error: 'Missing uri/q/query parameter' });
        return;
      }
      const result = await callTool('ue_read', { queries });
      jsonResponse(res, 200, { ok: true, queries, result, text: textFromMcpResult(result) });
      return;
    }

    if (req.method === 'POST' && url.pathname === '/call') {
      const body = await readBodyJson(req);
      const name = body.name || body.tool || body.toolName;
      if (!name) {
        jsonResponse(res, 400, { ok: false, error: 'Missing name/tool/toolName in JSON body' });
        return;
      }
      const args = body.arguments || body.args || {};
      const result = await callTool(name, args);
      jsonResponse(res, 200, { ok: true, name, result, text: textFromMcpResult(result) });
      return;
    }

    if (req.method === 'POST' && url.pathname === '/py') {
      const body = await readBodyJson(req);
      if (!body.code) {
        jsonResponse(res, 400, { ok: false, error: 'Missing code in JSON body' });
        return;
      }
      const result = await callTool('ue_py', { code: body.code });
      jsonResponse(res, 200, { ok: true, result, text: textFromMcpResult(result) });
      return;
    }

    if (req.method === 'POST' && url.pathname === '/plan') {
      const body = await readBodyJson(req);
      if (!body.plan) {
        jsonResponse(res, 400, { ok: false, error: 'Missing plan in JSON body' });
        return;
      }
      const result = await callTool('ue_plan_submit', { plan: body.plan });
      jsonResponse(res, 200, { ok: true, result, text: textFromMcpResult(result) });
      return;
    }

    jsonResponse(res, 404, {
      ok: false,
      error: 'Not found',
      endpoints: [
        'GET /health',
        'GET /tools',
        'GET /read?uri=ctx:',
        'POST /call {"name":"ue_read","arguments":{"queries":["ctx:"]}}',
        'POST /py {"code":"print(1)"}',
        'POST /plan {"plan":"..."}',
      ],
    });
  } catch (err) {
    log('request failed', { method: req.method, path: url.pathname, error: err.stack || err.message });
    jsonResponse(res, err.statusCode || 500, { ok: false, error: err.message, state, lastError });
  }
}

const server = http.createServer((req, res) => {
  handleRequest(req, res).catch((err) => {
    log('unhandled request error', { error: err.stack || err.message });
    jsonResponse(res, 500, { ok: false, error: err.message });
  });
});

server.listen(PORT, HOST, () => {
  log('proxy listening', { host: HOST, port: PORT, sseUrl: SSE_URL });
  process.stdout.write(`UGCAskQ proxy listening at http://${HOST}:${PORT}\n`);
  process.stdout.write(`Upstream SSE: ${SSE_URL}\n`);
  process.stdout.write(`Log: ${LOG_FILE}\n`);
  ensureReady().catch((err) => log('initial connect failed', { error: err.stack || err.message }));
});

process.on('SIGINT', () => {
  log('SIGINT shutting down');
  server.close(() => process.exit(0));
});

process.on('SIGTERM', () => {
  log('SIGTERM shutting down');
  server.close(() => process.exit(0));
});
