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

## Post-Update Verification Gate

After updating either the Skill or Companion, run:

```powershell
python .\scripts\check_companion_skill_versions.py
```

The check compares the installed Skill `VERSION` with the actual running `oasis-companion.exe`. It normalizes MSI/Tauri versions such as `1.26.816+2` or `1.26.816.2` to canonical `1.260816.2` before comparing.

Treat only `status=match` and exit code `0` as complete. If the result is `mismatch` or `blocked`, do not report the update as successful. Install or restart the matching Companion, verify the running executable path, and rerun the check. A Skill update status, Git revision, settings page, or matching installer on disk is not proof that the running desktop process has the correct version.
