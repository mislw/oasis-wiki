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

## Checks

- Background is lowest; popup is above ordinary content; system confirmation is highest.
- Text and icons belong to concrete controls or containers.
- Button text is above the button plate.
- Selection is above content but does not hide critical text.
- Decoration does not intercept input.
- Children remain inside the visible parent unless overflow is explicitly allowed.
- Colors, corners, borders, shadows, typography, icons, and states match the resolved project profile.
