# RedCliff UI 交付

Use this only after the bitmap is approved and the UI Tree has been reviewed. It creates an implementation contract; it never creates, edits, saves, or imports UMG assets, Lua files, `.uasset`, or `.umap` files.

## Workflow

1. Read `references/cowart-ui/delivery-contract.md` before generating a plan.
2. Require a UI Tree produced from a validated `ui-spec.json` and the resolved user-level component profile.
3. Build and validate the delivery plan:

```powershell
python scripts/cowart-ui/delivery/build_delivery_plan.py --ui-tree <ui-tree.json> --profile <profile.json> --output <delivery-plan.json>
python scripts/cowart-ui/delivery/validate_delivery_plan.py <delivery-plan.json>
```

4. Report unconfirmed controls instead of treating them as reusable. `ready_for_editor` remains false until every `reuse_of` reference is `active`.
5. After the developer explicitly authorizes editor mutation, route to `oasis-wiki` MCP UI and feature-development workflows. Read current WidgetBlueprint/Lua patterns before creating assets, then use the plan as the authoritative mapping.
6. Verify the delivered page with hierarchy readback, visible editor inspection, and PIE behavior. A valid plan is not runtime proof.

## Native Mapping

- `text`, `counter`, `input`: native `TextBlock` or input widgets.
- `button`: native `Button` plus a text/image child and operation binding.
- `progress`: native `ProgressBar`.
- `background`, `panel`, `card`, `icon`, `badge`: UMG containers/images using reviewed layer assets.
- `grid`, `row`, `slot`: layout containers; dynamic content needs a refresh owner and data binding.

Never bake text, values, timers, counters, hit areas, or selection states into exported PNGs.
