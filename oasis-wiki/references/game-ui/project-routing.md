# Project Routing

Run `scripts/game-ui/detect_project.py` before reading or changing a style library.

## Project name detection

1. Use the directory immediately below `UGCProjects`.
2. Otherwise use the nearest Git root directory name.
3. Otherwise use the current directory name.
4. Resolve aliases with `project-registry.json`.

## Profile priority

Load the first existing profile:

1. `<project-root>/.game-ui-system/profile.json`
2. `%USERPROFILE%/.codex/game-ui-design-system/projects/<slug>/profile.json`
3. `references/game-ui/projects/<slug>.json`
4. `assets/game-ui/project-profile-template/profile.json`

Project-local files override user profiles; user profiles override bundled seeds. Do not merge conflicting component definitions silently. The higher tier wins, while the lower definition remains available as comparison history.

Write to the user profile by default. Write to the project-local profile only when the developer explicitly asks to share the UI system with the project.
