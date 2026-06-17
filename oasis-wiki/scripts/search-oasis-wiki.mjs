#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillRoot = path.dirname(__dirname);
const wikiRoot = path.join(skillRoot, "references", "wiki");

function usage() {
  console.error("Usage: node scripts/search-oasis-wiki.mjs <query> [--max 40] [--context 0]");
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
  usage();
  process.exit(args.length === 0 ? 1 : 0);
}

let query = "";
let max = 40;
let context = 0;

for (let i = 0; i < args.length; i += 1) {
  const arg = args[i];
  if (arg === "--max") {
    max = Number.parseInt(args[++i] ?? "", 10);
  } else if (arg === "--context") {
    context = Number.parseInt(args[++i] ?? "", 10);
  } else if (!query) {
    query = arg;
  } else {
    query += ` ${arg}`;
  }
}

if (!query || !Number.isFinite(max) || max < 1 || !Number.isFinite(context) || context < 0) {
  usage();
  process.exit(1);
}

function walkMarkdown(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkMarkdown(fullPath));
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      files.push(fullPath);
    }
  }
  return files;
}

const lowerQuery = query.toLocaleLowerCase();
let printed = 0;

for (const file of walkMarkdown(wikiRoot)) {
  const text = fs.readFileSync(file, "utf8");
  const lines = text.split(/\r?\n/);
  for (let index = 0; index < lines.length; index += 1) {
    if (!lines[index].toLocaleLowerCase().includes(lowerQuery)) continue;

    const start = Math.max(0, index - context);
    const end = Math.min(lines.length - 1, index + context);
    for (let lineIndex = start; lineIndex <= end; lineIndex += 1) {
      console.log(`${file}:${lineIndex + 1}:${lines[lineIndex]}`);
    }
    printed += 1;
    if (printed >= max) process.exit(0);
  }
}

process.exit(printed > 0 ? 0 : 1);
