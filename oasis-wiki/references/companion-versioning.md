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

## Release Contract

Before calling a Companion version complete, keep these values synchronized:

- `package.json` and `package-lock.json`;
- `src-tauri/tauri.conf.json`;
- `src-tauri/Cargo.toml` and the root package entry in `src-tauri/Cargo.lock`;
- `CURRENT_SKILL_VERSION` in `src-tauri/src/skill/mod.rs`;
- the Companion/Skill version displayed by `src/windows/Settings.tsx`;
- bundled and installed Skill `VERSION` markers;
- the generated installer compatibility version and any published Git tag or release name.

## Windows MSI Compatibility

The product and Skill keep the canonical `M.YYMMDD.N` version. The Windows MSI build config uses valid SemVer `M.YY.MMDD+N` in `tauri.build.conf.json` because WiX restricts the minor field to 255. Tauri converts its numeric build metadata to WiX `M.YY.MMDD.N`. For example, product version `1.260815.1` uses config version `1.26.815+1` and maps only its MSI metadata to `1.26.815.1`; this mapping is not a product downgrade.

## GitHub Synchronization Gate

Every distributable iteration must exist on the GitHub default branch with a pushed `v{version}` tag. A local build, test run, or installation is not complete by itself.

When a Companion release bundles Skill changes, both `oasis-wiki` and `oasis-wiki-comp` must contain the matching release commits on their GitHub default branches and both repositories must publish the matching tag. If any commit or tag push fails, the release is not complete and must be reported as incomplete.

Do not reuse an already published `M.YYMMDD.N`. Do not infer `N` from Git commit count; choose the next unused distributable iteration for that date.
