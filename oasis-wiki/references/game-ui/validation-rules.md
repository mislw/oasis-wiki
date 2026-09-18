# Validation Rules

## Default layers

| Layer | Content |
|---:|---|
| 0 | Page background |
| 10 | Main window |
| 20 | Content panels |
| 30 | Cards, lists, slots |
| 40 | Icons, characters, buildings |
| 50 | Text and values |
| 60 | Interaction controls |
| 70 | Selection and state highlights |
| 80 | Popups, dropdowns, tooltips |
| 90 | Tutorials and masks |
| 100 | System alerts and confirmations |

## Blocking errors

- Missing UI Tree or parent.
- Serious occlusion or interaction blockage.
- Use of `deprecated` or `rejected` controls.
- Existing controls redesigned without correction approval.
- New controls missing `pending_review`.
- Page structure conflicts with the requirement.
- A requested project component is not `active`.
- A semantic item is unresolved, its asset needs a fresh preview, or the cached preview is missing.
- A `project_library_asset` preview key does not match the referenced image SHA-256.
- A proposed WidgetBlueprint replacement is missing any existing Lua-facing control, callback owner, dynamic state, or refresh surface without an explicit compatibility mapping.
- A visible button plate extends outside its actual Button hit region without a reviewed interaction reason and device verification.

## Checks

- Background is lowest; popup is above ordinary content; system confirmation is highest.
- Text and icons belong to concrete controls or containers.
- Button text is above the button plate.
- Selection is above content but does not hide critical text.
- Decoration does not intercept input.
- Dynamic repeated content has a declared ownership model: fixed children for a truly fixed set, or a reusable Item/List contract with data binding and teardown for runtime-sized data.
- Children remain inside the visible parent unless overflow is explicitly allowed.
- Colors, corners, borders, shadows, typography, icons, and states match the resolved project profile.
- Asset IDs, component IDs, semantic keys, and item IDs are unique within their catalogs.
- Committed project manifests contain only project-relative files, Unreal object paths, and preview keys. Local cache paths never enter committed manifests.
- `classified` describes a reviewed raw asset; it is not equal to component status `active`.
