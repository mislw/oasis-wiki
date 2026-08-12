# Workflow

## 1. Reference image analysis

1. Identify page type, purpose, and main operations.
2. Divide background, header, navigation, content, detail, action, popup, hint, and mask regions.
3. Build the complete UI Tree with parent and layer for every node.
4. Extract controls and match them against the resolved project library.
5. Record name, ID, category, purpose, page, parent, layer, states, reuse, similarity, confidence, and status.
6. Put uncertain results in `candidate` and explain why.
7. Validate hierarchy before proposing library changes.

## 2. Component extraction

- Use lowercase dot-separated IDs in the form `type.purpose.state`.
- Reuse confirmed definitions without changing core shape, palette, border, highlight, shadow, material, interaction meaning, or states.
- Use instance numbers only for identical repeated controls inside a page.
- Store a high-confidence but unconfirmed extraction as `pending_review`, not `active`.

## 3. New page generation

1. Parse page name, purpose, scene, operations, information, ratio, references, and requested deliverables.
2. Classify controls as direct reuse, state extension, or new candidate.
3. Create new controls as `pending_review` and state why existing controls cannot satisfy the need.
4. Build the UI Tree.
5. Describe layout, proportions, visual focus, operation path, spacing, and information priority.
6. Validate hierarchy and style.
7. Generate only the requested prompt, image, structure, Figma component notes, Unity hierarchy, Unreal UMG hierarchy, or code.
8. Finish with the automatic check report.

## 4. Developer commands

### `控件修正：`

Locate the control, show the old summary, apply the correction, check conflicts, increment the version, append history, deprecate or reject the wrong version, list affected pages, and report revalidation work.

### `确认控件：`

Require an exact component ID. Set it to `active`, record `confirmed_by: developer`, append history, and validate the profile.

### `拒绝控件：`

Require an exact component ID and reason. Set it to `rejected`, append history, find affected pages, and prohibit future reuse.
