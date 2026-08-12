import { createRequire } from 'node:module'
import { existsSync, mkdirSync, readdirSync, writeFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { dirname, join, resolve } from 'node:path'

function parseArgs(argv) {
  const args = { cowartPluginRoot: null, output: null, force: false }
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index]
    if (value === '--cowart-plugin-root') args.cowartPluginRoot = argv[++index]
    else if (value === '--output') args.output = argv[++index]
    else if (value === '--force') args.force = true
    else throw new Error(`Unknown argument: ${value}`)
  }
  return args
}

function versionParts(value) {
  return String(value).split(/[^0-9]+/).filter(Boolean).map(Number)
}

function compareVersionsDescending(left, right) {
  const a = versionParts(left)
  const b = versionParts(right)
  const length = Math.max(a.length, b.length)
  for (let index = 0; index < length; index += 1) {
    const difference = (b[index] ?? 0) - (a[index] ?? 0)
    if (difference !== 0) return difference
  }
  return right.localeCompare(left)
}

function isCowartPluginRoot(candidate) {
  return existsSync(join(candidate, 'package.json')) &&
    existsSync(join(candidate, 'node_modules', '@tldraw', 'editor'))
}

function discoverCowartPluginRoot() {
  const codexHome = resolve(process.env.CODEX_HOME || join(homedir(), '.codex'))
  const cacheRoot = join(codexHome, 'plugins', 'cache', 'cowart-github', 'cowart')
  if (!existsSync(cacheRoot)) {
    throw new Error(`Cowart plugin root was not found under ${cacheRoot}`)
  }
  const candidates = readdirSync(cacheRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort(compareVersionsDescending)
    .map((name) => join(cacheRoot, name))
  const pluginRoot = candidates.find(isCowartPluginRoot)
  if (!pluginRoot) {
    throw new Error(`Cowart plugin root with @tldraw/editor was not found under ${cacheRoot}`)
  }
  return pluginRoot
}

function resolveCowartPluginRoot(explicitRoot) {
  const pluginRoot = explicitRoot ? resolve(explicitRoot) : discoverCowartPluginRoot()
  if (!isCowartPluginRoot(pluginRoot)) {
    throw new Error(`Cowart plugin root is invalid or lacks @tldraw/editor: ${pluginRoot}`)
  }
  return pluginRoot
}

function createValidatedBlankSnapshot(pluginRoot) {
  const requireFromPlugin = createRequire(join(pluginRoot, 'package.json'))
  const { createTLStore } = requireFromPlugin('@tldraw/editor')
  if (typeof createTLStore !== 'function') {
    throw new Error(`Cowart plugin does not expose createTLStore: ${pluginRoot}`)
  }

  const sourceStore = createTLStore()
  if (typeof sourceStore.ensureStoreIsUsable !== 'function') {
    throw new Error(`Cowart tldraw store does not expose ensureStoreIsUsable: ${pluginRoot}`)
  }
  sourceStore.ensureStoreIsUsable()
  const snapshot = sourceStore.getStoreSnapshot()

  const validationStore = createTLStore()
  const migratedSnapshot = validationStore.migrateSnapshot(snapshot)
  for (const record of Object.values(migratedSnapshot.store)) {
    validationStore.put([record], 'initialize')
  }
  const validatedSnapshot = validationStore.getStoreSnapshot()
  const records = Object.values(validatedSnapshot.store)
  const pageIds = records.filter((record) => record.typeName === 'page').map((record) => record.id)
  const documentIds = records.filter((record) => record.typeName === 'document').map((record) => record.id)

  if (pageIds.length !== 1 || documentIds.length !== 1) {
    throw new Error(`Cowart blank snapshot must contain one page and one document; received pages=${pageIds.length}, documents=${documentIds.length}`)
  }
  return { snapshot: validatedSnapshot, pageIds }
}

function main() {
  const args = parseArgs(process.argv.slice(2))
  const pluginRoot = resolveCowartPluginRoot(args.cowartPluginRoot)
  const { snapshot, pageIds } = createValidatedBlankSnapshot(pluginRoot)
  const outputPath = args.output ? resolve(args.output) : null

  if (outputPath) {
    if (existsSync(outputPath) && !args.force) {
      throw new Error(`Output already exists; pass --force to replace it: ${outputPath}`)
    }
    mkdirSync(dirname(outputPath), { recursive: true })
    writeFileSync(outputPath, `${JSON.stringify(snapshot, null, 2)}\n`, 'utf8')
  }

  const summary = {
    ok: true,
    pluginRoot,
    output: outputPath,
    recordCount: Object.keys(snapshot.store).length,
    pageIds,
  }
  if (!outputPath) summary.snapshot = snapshot
  process.stdout.write(`${JSON.stringify(summary)}\n`)
  process.exit(0)
}

try {
  main()
} catch (error) {
  process.stderr.write(`ERROR: ${error instanceof Error ? error.message : String(error)}\n`)
  process.exit(2)
}
