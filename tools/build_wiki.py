#!/usr/bin/env python3
"""Build everything the GBFans wiki page needs from the repository.

    python tools/build_wiki.py            # regenerate plans, check the page, build outputs

Outputs (in build/wiki/, not committed):
  page_preview.md   page source with images pointing at GitHub (for previewing in the editor)
  page_gbfans.md    page source with images pointing at uploaded GBFans assets
                    (only images listed in docs/wiki/gbfans_assets.json; others stay on GitHub)
  upload_list.txt   images that still need uploading to the wiki page
  <bundle>.zip      the download bundle for hosting on GBFans

Image placeholders in the page source are written IMG:<file> (docs/images/<file>)
or IMG:plans/<file> (docs/plans/<file>).
"""
import json, os, re, shutil, subprocess, sys, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WIKI = os.path.join(ROOT, "docs", "wiki")
OUT = os.path.join(ROOT, "build", "wiki")
RAW = "https://raw.githubusercontent.com/rmbrumback-lab/ecto-1a-led-sign/main/docs/"
PH = re.compile(r"IMG:([^)\s]+)")


def local(ph):
    return os.path.join(ROOT, "docs", ph if ph.startswith("plans/") else "images/" + ph)


def main():
    page = json.load(open(os.path.join(WIKI, "page.json")))
    assets = json.load(open(os.path.join(WIKI, "gbfans_assets.json")))["assets"]
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "make_wiki_images.py")], check=True)

    src = open(os.path.join(ROOT, page["source"])).read()
    phs = PH.findall(src)
    missing = [p for p in phs if not os.path.exists(local(p))]
    if missing:
        sys.exit(f"missing images: {missing}")
    if len(phs) > page["image_limit"]:
        sys.exit(f"{len(phs)} images exceeds the wiki limit of {page['image_limit']}")
    refs = set(re.findall(r"\[\^([\w-]+)\](?!:)", src))
    defs = set(re.findall(r"^\[\^([\w-]+)\]:", src, re.M))
    if refs - defs or defs - refs:
        sys.exit(f"footnotes without definitions: {refs - defs}; unused definitions: {defs - refs}")

    os.makedirs(OUT, exist_ok=True)
    raw = lambda p: RAW + (p if p.startswith("plans/") else "images/" + p)
    open(os.path.join(OUT, "page_preview.md"), "w").write(PH.sub(lambda m: raw(m.group(1)), src))
    gb = lambda p: f"/api/assets/{assets[p]}/url?size=medium" if p in assets else raw(p)
    open(os.path.join(OUT, "page_gbfans.md"), "w").write(PH.sub(lambda m: gb(m.group(1)), src))
    todo = [p for p in dict.fromkeys(phs) if p not in assets]
    open(os.path.join(OUT, "upload_list.txt"), "w").write("\n".join(todo) + ("\n" if todo else ""))

    name = f"{page['bundle_name']}_{page['bundle_version']}"
    stage = os.path.join(OUT, name)
    shutil.rmtree(stage, ignore_errors=True)
    d = lambda *p: os.path.join(ROOT, *p)
    layout = {
        "coolled_16x96": [d("dist", "Ecto-1A_GB2_16x96.jt")],
        "coolled_16x96/two_part": [d("dist", "two_part", f"Ecto-1A_GB2_16x96_Part{i}.jt") for i in (1, 2)],
        "frames_80x7": sorted(os.path.join(d("dist", "frames_80x7"), f) for f in os.listdir(d("dist", "frames_80x7"))),
        "data": [d("dist", f) for f in ("ecto1a_spritesheet_80x7.png", "ecto1a_frames.json",
                                        "ecto1a_playlist.json", "ecto1a_frames.h")]
                + [d("dist", "two_part", f) for f in ("ecto1a_full_frames.json", "ecto1a_full_playlist.json")],
        "plans": sorted(os.path.join(d("docs", "plans"), f) for f in os.listdir(d("docs", "plans"))),
        "fonts": [d("docs", "images", f"font_{n}.png") for n in ("bold_wide", "bold_narrow", "thin")],
        "preview": [d("dist", "ecto1a_80x7.gif"), d("dist", "ecto1a_96x16_panel.gif"),
                    d("dist", "two_part", "ecto1a_96x16_full.gif")],
    }
    for sub, files in layout.items():
        os.makedirs(os.path.join(stage, sub), exist_ok=True)
        for f in files:
            shutil.copy2(f, os.path.join(stage, sub))
    readme = open(os.path.join(WIKI, "bundle_README.txt")).read().replace("{version}", page["bundle_version"])
    open(os.path.join(stage, "README.txt"), "w").write(readme)
    zpath = os.path.join(OUT, name + ".zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(stage):
            for f in sorted(files):
                p = os.path.join(base, f)
                z.write(p, os.path.relpath(p, OUT))
    shutil.rmtree(stage)
    print(f"page OK: {len(phs)} images, {len(defs)} footnotes; {len(todo)} images still to upload")
    print("built", os.path.relpath(OUT, ROOT), "->", ", ".join(sorted(os.listdir(OUT))))


if __name__ == "__main__":
    main()
