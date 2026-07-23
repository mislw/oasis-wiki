#!/usr/bin/env node
/**
 * UGCAskQ CLI proxy for Codex/WorkBuddy.
 *
 * This is NOT an MCP stdio server. It is a plain command-line client that
 * connects to the editor UGCAskQ SSE MCP endpoint, calls tools, prints the
 * result, and exits. The goal is to let Codex use ordinary shell commands
 * instead of registering a direct MCP server.
 *
 * Examples:
 *   node ugcaskq-cli.js tools
 *   node ugcaskq-cli.js read ctx:
 *   node ugcaskq-cli.js read py:index
 *   node ugcaskq-cli.js call ue_read "{\"queries\":[\"ctx:\"]}"
 *   node ugcaskq-cli.js py "print('hello from editor')"
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const DEFAULT_SSE_URL = process.env.UGCASKQ_SSE_URL || 'http://127.0.0.1:12463/sse';
const DEBUG_LOG = process.env.UGCASKQ_CLI_LOG || path.join(process.env.USERPROFILE || '.', '.codex', 'tmp', 'ugcaskq-cli.log');
const TIMEOUT_MS = Number(process.env.UGCASKQ_CLI_TIMEOUT_MS || 120000);

let nextId = 1;
let postEndpoint = null;
let sseResponse = null;
const pending = new Map();

function debug(message, extra) {
  try {
    fs.mkdirSync(path.dirname(DEBUG_LOG), { recursive: true });
    const suffix = extra === undefined ? '' : ` ${JSON.stringify(extra).slice(0, 1200)}`;
    fs.appendFileSync(DEBUG_LOG, `${new Date().toISOString()} ${message}${suffix}\n`);
  } catch (_) {}
}

function usage() {
  return `UGCAskQ CLI proxy\n\nUsage:\n  node ugcaskq-cli.js [--url <sse-url>] [--json] <command> [...args]\n\nCommands:\n  tools                         List MCP tools exposed by UGCAskQ\n  read <query...>                Call ue_read with one or more queries\n  py <python-code>               Call ue_py with Python code\n  plan <plan-yaml-or-json>        Call ue_plan_submit\n  call <tool-name> [json-args]    Call any MCP tool by name\n\nExamples:\n  node ugcaskq-cli.js tools\n  node ugcaskq-cli.js read ctx:\n  node ugcaskq-cli.js read py:index "py:workflow asset_browser"\n  node ugcaskq-cli.js call ue_read "{\"queries\":[\"ctx:\"]}"\n  node ugcaskq-cli.js py "print('hello')"\n\nEnv:\n  UGCASKQ_SSE_URL                Default: ${DEFAULT_SSE_URL}\n  UGCASKQ_CLI_LOG                Default: ${DEBUG_LOG}\n`;
}

function parseArgs(argv) {
  const out = { url: DEFAULT_SSE_URL, json: false, rest: [] };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--url') {
      if (!argv[i + 1]) throw new Error('--url requires a value');
      out.url = argv[++i];
    } else if (arg === '--json') {
      out.json = true;
    } else if (arg === '-h' || arg === '--help' || arg === 'help') {
      out.help = true;
    } else {
      out.rest.push(arg);
    }
  }
  return out;
}

function connectSSE(sseUrl) {
  return new Promise((resolve, reject) => {
    const req = http.get(sseUrl, { headers: { Accept: 'text/event-stream' } }, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`SSE HTTP ${res.statusCode}`));
        return;
      }

      sseResponse = res;
      let buf = '';
      let eventType = 'message';
      let dataLines = [];
      let endpointResolved = false;

      function resolveEndpoint(value) {
        if (endpointResolved) return;
        endpointResolved = true;
        postEndpoint = value;
        resolve(value);
      }

      function dispatch() {
        if (!dataLines.length) return;
        const data = dataLines.join('\n').trim();
        dataLines = [];
        if (!data) return;

        if (eventType === 'endpoint') {
          debug('endpoint', { data });
          resolveEndpoint(data);
          return;
        }

        try {
          const msg = JSON.parse(data);
          debug('sse message', { id: msg.id, method: msg.method, hasResult: !!msg.result, hasError: !!msg.error });
          if (msg.id !== undefined && pending.has(msg.id)) {
            const item = pending.get(msg.id);
            pending.delete(msg.id);
            item.resolve(msg);
          }
        } catch (err) {
          debug('sse parse ignored', { error: err.message, data: data.slice(0, 500) });
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
        debug('sse response error', { error: err.message });
        if (!endpointResolved) reject(err);
      });

      res.on('close', () => {
        debug('sse closed', { pending: pending.size });
        for (const [id, item] of pending.entries()) {
          pending.delete(id);
          item.reject(new Error('SSE connection closed'));
        }
        if (!endpointResolved) reject(new Error('SSE connection closed before endpoint event'));
      });
    });

    req.on('error', reject);
    req.setTimeout(15000, () => req.destroy(new Error('SSE connect timeout')));
  });
}

function postJson(sseUrl, msg) {
  return new Promise((resolve, reject) => {
    if (!postEndpoint) {
      reject(new Error('No SSE POST endpoint received'));
      return;
    }
    const base = new URL(sseUrl);
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
      res.on('end', resolve);
    });
    req.on('error', reject);
    req.setTimeout(15000, () => req.destroy(new Error('POST timeout')));
    req.write(body);
    req.end();
  });
}

function rpc(sseUrl, method, params, notification = false) {
  const msg = notification ? { jsonrpc: '2.0', method, params } : { jsonrpc: '2.0', id: nextId++, method, params };
  debug('rpc send', { id: msg.id, method });
  if (notification) return postJson(sseUrl, msg).then(() => null);

  const wait = new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      pending.delete(msg.id);
      reject(new Error(`Timeout waiting for ${method}`));
    }, TIMEOUT_MS);
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
  return postJson(sseUrl, msg).then(() => wait);
}

async function initialize(sseUrl) {
  await connectSSE(sseUrl);
  const init = await rpc(sseUrl, 'initialize', {
    protocolVersion: '2024-11-05',
    capabilities: {},
    clientInfo: { name: 'ugcaskq-cli', version: '1.0.0' },
  });
  if (init.error) throw new Error(`initialize failed: ${init.error.message || JSON.stringify(init.error)}`);
  await rpc(sseUrl, 'notifications/initialized', {}, true);
}

async function callTool(sseUrl, name, args) {
  const response = await rpc(sseUrl, 'tools/call', { name, arguments: args || {} });
  if (response.error) throw new Error(`${name} failed: ${response.error.message || JSON.stringify(response.error)}`);
  return response.result;
}

function parseJsonArg(text) {
  if (!text) return {};
  try {
    return JSON.parse(text);
  } catch (err) {
    throw new Error(`Invalid JSON args: ${err.message}\nInput: ${text}`);
  }
}

function renderResult(result, asJson) {
  if (asJson) return JSON.stringify(result, null, 2);
  if (result && Array.isArray(result.tools)) {
    return result.tools.map((tool) => `${tool.name}\t${tool.description || ''}`).join('\n');
  }
  if (result && Array.isArray(result.content)) {
    const parts = result.content.map((item) => {
      if (!item) return '';
      if (item.type === 'text') return item.text || '';
      return JSON.stringify(item);
    }).filter(Boolean);
    if (parts.length) return parts.join('\n');
  }
  return typeof result === 'string' ? result : JSON.stringify(result, null, 2);
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help || opts.rest.length === 0) {
    process.stdout.write(usage());
    return;
  }

  const [command, ...args] = opts.rest;
  await initialize(opts.url);

  let result;
  if (command === 'tools' || command === 'tools/list') {
    const response = await rpc(opts.url, 'tools/list', {});
    if (response.error) throw new Error(`tools/list failed: ${response.error.message || JSON.stringify(response.error)}`);
    result = response.result;
  } else if (command === 'read') {
    if (!args.length) throw new Error('read requires at least one query');
    result = await callTool(opts.url, 'ue_read', { queries: args });
  } else if (command === 'py') {
    if (!args.length) throw new Error('py requires Python code');
    result = await callTool(opts.url, 'ue_py', { code: args.join(' ') });
  } else if (command === 'plan') {
    if (!args.length) throw new Error('plan requires a YAML/JSON plan string');
    result = await callTool(opts.url, 'ue_plan_submit', { plan: args.join(' ') });
  } else if (command === 'call') {
    if (!args[0]) throw new Error('call requires a tool name');
    const toolName = args[0];
    const jsonText = args.slice(1).join(' ').trim();
    result = await callTool(opts.url, toolName, parseJsonArg(jsonText));
  } else {
    throw new Error(`Unknown command: ${command}\n\n${usage()}`);
  }

  process.stdout.write(renderResult(result, opts.json));
  process.stdout.write('\n');
}

main().catch((err) => {
  debug('fatal', { error: err.stack || err.message });
  process.stderr.write(`UGCAskQ CLI error: ${err.message}\n`);
  process.exitCode = 1;
}).finally(() => {
  try { if (sseResponse) sseResponse.destroy(); } catch (_) {}
});
