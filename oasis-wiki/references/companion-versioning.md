# Oasis Companion Versioning

Oasis Companion and its bundled `oasis-wiki` Skill use this release version format:

```text
M.YYMMDD.N
```

- `M`: major product generation. Increase only when the Companion or Skill has a major product-level change.
- `YYMMDD`: release date in the `Asia/Shanghai` timezone.
- `N`: one-based distributable iteration number for that calendar date. Increase for every local or GitHub-synchronized build on the same date; reset to `1` when the date changes.

Example:

```text
1.260814.4
```

This means major generation `1`, date `2026-08-14`, and the fourth distributable iteration made that day.

Windows MSI builds use a separate valid SemVer mapping in `tauri.build.conf.json`:

```text
M.YY.MMDD+N
```

For example, canonical version `1.260816.2` maps to MSI build version `1.26.816+2`. Tauri and WiX expose that build as Windows file version `1.26.816.2`. Always build the MSI with `--config tauri.build.conf.json`; the canonical product and Skill version remain unchanged.

## Release Contract

Before calling a Companion version complete, keep these values synchronized:

- `package.json` and `package-lock.json`;
- `src-tauri/tauri.conf.json`;
- `tauri.build.conf.json`, using the `M.YY.MMDD+N` MSI mapping;
- `src-tauri/Cargo.toml` and the root package entry in `src-tauri/Cargo.lock`;
- `CURRENT_SKILL_VERSION` in `src-tauri/src/skill/mod.rs`;
- the Companion/Skill version displayed by `src/windows/Settings.tsx`;
- bundled and installed Skill `VERSION` markers;
- the generated executable version and any published Git tag or release name.

Do not reuse an already published `M.YYMMDD.N`. Do not infer `N` from Git commit count; choose the next unused distributable iteration for that date.
