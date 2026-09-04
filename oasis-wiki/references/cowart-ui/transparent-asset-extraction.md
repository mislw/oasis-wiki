# Transparent UI Asset Extraction Rules

Use this reference when a reviewed flattened game UI must be separated into a complete mother background, reusable controls, child icons, decorative layers, or developer-confirmed visual text assets.

These rules govern visual extraction and component-library evidence. They do not authorize WidgetBlueprint changes and do not change runtime bindings.

## Core Composition Contract

Recomposition uses:

```text
one complete mother background
+ transparent or intentionally translucent controls
+ native runtime controls
```

Do not reconstruct a page by joining multiple rectangular background crops. The mother background is one full-page bitmap and remains the only source of page scenery, corner illustration, paper texture, or other continuous environmental art.

A foreground control must not carry a duplicate rectangle of the mother background. A visible seam, differently colored paper patch, repeated scenery, or abrupt rectangular region is evidence that the control still contains baked background pixels.

## Continuous Mother-Background Edge Repair

Use these rules for continuous borders, rails, bands, paper edges, scenery, and other mother-background features that cross behind foreground controls.

1. Diagnose layer ownership before editing. Compare the mother background alone with the final recomposition. If the mother background is clean but the recomposition is defective, inspect foreground bounds and alpha instead of modifying the background again.
2. Rebuild the complete affected span from one continuous source. Never accumulate adjacent local horizontal patches to repair a continuous feature. When an approved source has unobstructed rows before foreground bounds begin, restore those full rows across the entire span and feather only vertically into reconstructed content.
3. Treat foreground bounds as ownership boundaries. Verify the exact row or column where title art, panels, or decoration begin. Do not copy source pixels containing foreground decoration into `background.root`.
4. Map screenshot feedback to output pixels when possible. Account for integer nearest-neighbor preview zoom, then inspect the exact marked crop, an enlarged full-span detail, the mother background alone, and the final recomposition.
5. Treat metrics as diagnostics, not acceptance. A changed hash, nonzero changed-pixel count, or bounded mask does not prove a visual repair. Reject visible steps, material or color jumps, rectangular tint, repeated patches, and stitch boundaries.
6. If repeated local repairs expose new seams, stop patching. Reconstruct the complete continuous feature from one approved source before trying another local correction.

## Choose The Asset Type

### Complete mother background

Use one complete bitmap for the page background when the visual must remain continuous behind multiple controls.

- Remove every foreground panel, icon, label, button, card, divider, and child control.
- Repair the revealed scenery and texture coherently.
- Keep the original page dimensions.
- Never use a checkerboard, source crop, comparison image, or assembled preview as the mother background.

### Fully transparent foreground

Use an RGBA transparent asset for:

- irregular artwork and character cutouts;
- item icons and child icons;
- glyph-only visual text approved by the developer;
- divider ornaments, flourishes, arrows, badges, and foreground decoration;
- controls whose outer silhouette is not an intentional filled rectangle.

Only the owned visual and its intrinsic outline, glow, or shadow may remain. All unrelated paper, panel fill, scenery, labels, neighboring icons, and source-crop pixels must be transparent.

### Semi-transparent panel or mask

Use a translucent panel when the control intentionally has a paper, glass, fog, veil, or mask body while the mother background should remain visible through it.

- Keep the interior partially transparent.
- The border may be more opaque than the interior when required for structure.
- Preserve intentional material texture without baking page scenery into the panel.
- Record the selected interior and border alpha policy in the catalog or profile.
- Tune alpha from the approved page. Do not treat one project's numeric alpha values as global constants.

### Intentional opaque skin

An opaque rectangle is allowed only when the rectangle itself is the control, such as a solid button, framed card face, inventory slot, or modal surface.

Even then, remove all descendants and unrelated content: text, counters, icons, badges, artwork, parent scenery, and neighboring shadows. Opaque is a semantic decision, not permission to keep a rectangular screenshot crop.

## Text Handling

### Default runtime rule

Dynamic text, values, timers, prices, progress values, counters, editable labels, localization-sensitive copy, and button operations remain Native by default.

Extraction of a transparent text bitmap does not silently replace the runtime contract. Preserve the original binding, refresh owner, localization requirement, and interaction behavior until the reviewed delivery plan explicitly chooses an implementation.

### Developer-confirmed visual text exception

When the developer explicitly identifies a fixed word, title, calligraphic label, or other stylized lettering as a visual asset, it may be extracted as a transparent PNG.

The text asset keeps only:

- the glyph shape;
- antialiased edge pixels;
- an intentional outline, glow, emboss, or soft shadow that belongs to the lettering.

It removes:

- paper, cloud, ribbon, badge, card, or button backing;
- divider lines and frame edges;
- parent texture and scenery;
- neighboring icons and annotations;
- cleanup rectangles used to hide an earlier extraction defect.

Store this as a `pending_review` project-library component, normally with category `text` or a clearly linked text-artwork role.

If the visible text is dynamic, its transparent extraction is visual-reference evidence or a style source unless the developer separately approves a bitmap-font, digit-atlas, or fixed-image implementation. Do not infer that approval from the extraction request.

### Text extraction checks

- Use color/luminance selection, semantic masks, source-background difference, or another method suited to the actual contrast. Do not use one universal threshold for every font.
- Preserve light glyphs on dark surfaces and dark glyphs on light surfaces without retaining the surface.
- Remove long thin components that belong to card borders or divider lines.
- Inspect small punctuation, decimal points, slashes, plus signs, units, and narrow strokes for accidental deletion.
- Add transparent safety padding when glyphs or shadows touch the crop edge.
- When padding changes the bitmap bounds, record the exact page-space placement offset.
- A true calligraphic stroke may reach the visual bound, but an extraction must not be clipped merely because the inferred UI Tree box was too tight.

## Child Icon Handling

Treat a child icon as independent when it can change, move, hide, animate, recolor, or be reused separately from its parent.

The icon asset keeps:

- the complete silhouette;
- intrinsic outline and material detail;
- an intentional cast shadow or glow that moves with the icon.

The icon asset removes:

- the parent card, slot, badge, button, or paper backing;
- child text, counters, arrows, upgrade marks, or status badges that have separate semantics;
- mother-background pixels;
- selection rectangles, browser checkerboards, source annotations, and screenshot borders.

Split compound visuals when their behavior differs. Examples:

- item icon and upgrade arrow;
- item icon and quantity;
- badge skin and badge text;
- button skin and button label;
- portrait and lock overlay.

Keep them together only when the developer confirms that they are one inseparable visual control.

For runtime-native Unreal icons, preserve `texture_asset`, `item_id`, and `reuse_of`. A transparent preview may be stored as `visual_assets.native_preview`, but it must not create a duplicate generated runtime texture or replace the resolved native asset.

In UI Workbench, `visual_assets.native_preview` is the node's only rendered visual. Keep runtime text metadata when needed, but suppress the additional native text layer while the preview is present. Pure interaction or hit-target nodes may retain semantic labels in data, but must not draw those labels on top of their visual parent.

Scenery already owned by the complete mother background must not be emitted again as a Workbench component, hidden overlay, contact-sheet entry, or reusable asset candidate. Preserve any historical cut files on disk, but omit their nodes from the final handoff tree.

### Icon completeness checks

- Compare the extracted silhouette with the approved source at 100% and enlarged scale.
- Inspect thin tips, handles, roofs, horns, hair, smoke, chains, particles, and soft shadows.
- Expand the source region and re-extract when the alpha silhouette touches an edge or a detail is missing.
- Reject colored matte fringes and opaque rectangular halos.
- Use a checkerboard preview and a placement preview over the mother background.

## Parent And Child Residual Rule

After extracting or removing a child, inspect its parent clean layer again.

If removing a text layer exposes a baked label strip, if removing an icon exposes a copied icon shadow, or if removing a divider exposes a paper rectangle, correct the parent layer. Do not hide the defect by restoring an opaque child crop.

The parent owns only its own surface. The child owns only its own visual. Recomposition must work even when either one is temporarily hidden or moved.

Run both movement checks:

1. Hide or move the child. The original location must show a clean parent surface with no child residue.
2. Hide or move the parent. The original location must show only the complete mother background.

## Alpha And Bounds Validation

Every transparent component must be saved as a real RGBA PNG with a meaningful alpha channel.

For each candidate:

- render it over a checkerboard;
- record dimensions and page-space bounds;
- inspect minimum and maximum alpha;
- inspect fully transparent, partially transparent, and fully opaque pixel counts;
- inspect nonzero alpha on all four outer edges;
- verify that transparent RGB residue does not create colored fringes when scaled;
- verify that resizing does not reveal crop seams or clipped shadows.

An irregular asset that is 100% opaque is normally a failed extraction. A semi-transparent panel that is 100% opaque is a failed mask when the approved composition requires the mother background to show through.

## Recomposition Gate

Build the review image only from:

- the complete mother background;
- reviewed clean panel/card/button skins;
- transparent artwork, icons, dividers, and confirmed visual text;
- Native placeholders or runtime previews for remaining dynamic controls.

Never composite `source_crop` files into the review image.

Compare the result with the approved source and inspect:

- abrupt paper or color rectangles;
- visible stitch boundaries;
- duplicated scenery or decoration;
- missing or clipped icon details;
- text with retained backing;
- parent surfaces revealed by transparent children;
- incorrect z-order, placement, scale, or padding offset.

Create individual checker previews and a contact sheet for batches. Keep the full recomposed page as the final visual acceptance artifact.

## Library And Versioning

- Preserve old files and create a versioned sibling for every corrected asset.
- Keep new and corrected assets `pending_review` until explicit developer confirmation.
- Record file path, dimensions, pixel format, SHA-256, version, alpha policy, and correction reason.
- Append profile history rather than rewriting earlier decisions.
- Mark an older page preview `superseded` only after the replacement preview exists and validates.
- Validate every maintained profile and require the asset catalog to report zero missing files.
- Keep source images, checker previews, contact sheets, and assembly previews out of the reusable component role.

## Completion Checklist

Before reporting a component-extraction pass complete:

1. The page uses one complete mother background.
2. Every irregular foreground asset has real transparency.
3. Every translucent panel reveals the mother background without carrying copied scenery.
4. Developer-confirmed visual text contains glyphs only.
5. Dynamic text still has an explicit runtime-native contract unless separately approved otherwise.
6. Child icons are complete and separated from independently controlled badges, text, and overlays.
7. Parent layers contain no child residue.
8. Checker previews and a full recomposition have been visually inspected.
9. Corrected files are versioned and remain `pending_review`.
10. Profiles validate and the catalog has zero missing files.
