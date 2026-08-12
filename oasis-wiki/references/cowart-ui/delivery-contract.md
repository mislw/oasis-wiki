# Delivery Contract

The delivery plan has four sections:

- `widgets`: UMG hierarchy, source bounds, semantic layer, and native/widget class.
- `bindings`: data keys and their UI targets. Each dynamic node must have a refresh owner.
- `operations`: button trigger, action, and authoritative owner from the UI specification.
- `acceptance`: editor hierarchy, visual comparison, input, refresh, reconnect, and PIE checks.

`ready_for_editor` is false when a node names `reuse_of` that is absent or not `active` in the component profile. This is a review block, not permission to replace the component with a new design.

The plan does not prove that a WidgetBlueprint was created. Only a later editor readback plus PIE verifies the implementation.
