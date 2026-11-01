# GBFans wiki page: Ecto-1A LED Sign Boards

This folder is the source of truth for the GBFans wiki page [Ecto-1A LED Sign Boards](https://www.gbfans.com/wiki/ecto-1a-led-sign-boards). Edit the page here first, then publish to the wiki, so the repository and the wiki never drift apart.

| File | Purpose |
|---|---|
| [`ecto-1a-led-sign-boards.md`](ecto-1a-led-sign-boards.md) | The page content (Markdown, as accepted by the wiki editor) |
| [`page.json`](page.json) | Title, URL, tags, edit summary, bundle name and version |
| [`gbfans_assets.json`](gbfans_assets.json) | Which GBFans asset each image was uploaded as |
| [`bundle_README.txt`](bundle_README.txt) | README placed inside the download zip |
| [`forum_posts.md`](forum_posts.md) | The forum posts and the guidance agreed with AJ Quick |
| [`../plans/`](../plans/) | Numbered pixel-map plans and plain-text pixel maps, from `tools/make_wiki_images.py` |
| [`../../tools/build_wiki.py`](../../tools/build_wiki.py) | Regenerates the plans, checks the page, and builds the preview, the GBFans version and the download zip |

## Conventions

- **Images** are written `![alt](IMG:file.png)` for `docs/images/` or `![alt](IMG:plans/file.png)` for `docs/plans/`. The build swaps in GitHub URLs (for preview) or GBFans asset URLs (for publishing). Use only our own renderings; no film stills or third-party images on the page. The limit is 30 images.
- **Footnotes** use the wiki's syntax: `[^id]` in the text and `[^id]: source` in References. The build fails if a reference has no definition, or the reverse.
- **Status labels:** mark anything not confirmed by a reference as **unconfirmed**, and anything reconstructed as **inferred**. Keep this consistent with [ATTRIBUTION.md](../ATTRIBUTION.md).
- The wiki editor has **no tables**. Use headed lists.

## Updating the page

1. If the animation changed, regenerate it first (`cd src && python -m ecto1a.generate --out ../dist && cd ..`, then `python tools/make_doc_images.py`) and run `python -m pytest -q tests`.
2. Edit `ecto-1a-led-sign-boards.md`. If files changed, bump `bundle_version` in `page.json` and note the change in the revision log below.
3. Run `python tools/build_wiki.py`. It fails on missing images, too many images, or broken footnotes.
4. Upload any images listed in `build/wiki/upload_list.txt` to the wiki page (Upload Image in the editor), and record each new asset id in `gbfans_assets.json`. If an image changed, re-upload it and update its id.
5. Re-run the build, then paste `build/wiki/page_gbfans.md` into the editor's Content, set the tags and edit summary from `page.json`, and save.
6. If the download bundle changed, send the new zip from `build/wiki/` to AJ Quick for hosting, and update the Downloads section once it has a GBFans link.
7. Commit the changes here with the same summary as the wiki edit.

## Revision log

| Date | Version | Change | Wiki status |
|---|---|---|---|
| 2026-11-01 | v10.1 | First draft: hardware, messages, fonts, sequence, inferred effects, plans, build guide, downloads, open questions, credits and references. Downloads link directly to the `.jt` files, the attribution PDF, every image file, and the porting code on GitHub | Drafted in the editor, **not yet saved** |
