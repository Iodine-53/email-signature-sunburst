# Email Signature #6 — "Sunburst" (yellow/teal corporate)

Pixel-matched HTML email signature built from a Fiverr mockup (600x194).

- `signature.html` — source of truth, relative `slices/` paths
- `signature-hosted.html` — absolute catbox.moe image URLs, ready to paste into an email client
- `signature-standalone.html` — fully self-contained (base64 images), zero remote requests
- `slices/` — e6_bg.png (all static artwork), e6_photo.png, 4 social glyphs
- `icon-hosting.md` — image URL map + artwork sources
- `compare.py` — headless-Chrome render + diff vs reference

Layout: baked background PNG + absolutely-positioned live Arial text — no graphic ever shares a row with live text, so no banding on font substitution.

Colors: yellow `#FFC01B`, teal `#003F5E`, divider navy `#0C283E`, name navy `#0A1628`.

Icons: Flaticon UIcons Brands — https://www.flaticon.com/uicons
