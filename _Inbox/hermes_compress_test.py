#!/usr/bin/env python3
"""Hermes_Compress_Test: surgical WhatsApp screenshot -> WebP (80-89% smaller), one zip.
Usage: python hermes_compress_test.py scan|preview|commit <SRC_DIR> [--day YYYY-MM-DD]
Originals are NEVER modified, moved or deleted."""
import sys, io, re, csv, json, hashlib, zipfile, datetime as dt
from pathlib import Path
from PIL import Image, ImageOps

phase = sys.argv[1]; SRC = Path(sys.argv[2]).expanduser()
TODAY = dt.date.today()
DAY = dt.date.fromisoformat(sys.argv[sys.argv.index("--day")+1]) if "--day" in sys.argv else TODAY - dt.timedelta(days=1)
WORK = Path.cwd()/f"Hermes_Compress_Test_{TODAY}"; (WORK/"webp").mkdir(parents=True, exist_ok=True)
SEL = WORK/"selection.csv"; LO, HI, MIN_W = 0.80, 0.89, 720
EXT = {".png", ".jpg", ".jpeg"}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1<<20), b""): h.update(c)
    return h.hexdigest()

def name_date(n):
    m = re.search(r"(20\d\d)[-_]?(\d\d)[-_]?(\d\d)", n)
    try: return dt.date(*map(int, m.groups())) if m else None
    except ValueError: return None

def classify(p):
    n = p.name.lower(); st = p.stat()
    d_name = name_date(p.name); d_mod = dt.date.fromtimestamp(st.st_mtime)
    d = d_name or d_mod; wa = "whatsapp" in n
    if wa and d == DAY: tier, why = "A", "WhatsApp in name + date matches"
    elif wa: tier, why = "X-other-day", f"WhatsApp but dated {d}"
    elif d == DAY and "screenshot" in n or d == DAY and "screen shot" in n: tier, why = "B", "generic screenshot, date matches, WhatsApp NOT verified"
    else: tier, why = "X-ignore", "not WhatsApp / wrong date"
    return tier, why, d_name, d_mod

def encode(img, q, s):
    im = img if s == 1 else img.resize((int(img.width*s), int(img.height*s)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "WEBP", quality=q, method=6); return b.getvalue()

def fit(path):
    orig = path.stat().st_size
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    for s in (1.0, 0.9, 0.8, 0.7, 0.6):
        if s != 1.0 and img.width*s < MIN_W: break
        lo, hi, best = 10, 95, None
        while lo <= hi:
            q = (lo+hi)//2; data = encode(img, q, s); red = 1 - len(data)/orig
            if red >= LO: best = (q, s, data, red); lo = q+1
            else: hi = q-1
        if best: return orig, best
    return orig, None

if phase == "scan":
    rows = []
    for p in sorted(SRC.iterdir()):
        if p.is_file() and p.suffix.lower() in EXT:
            t, why, dn, dm = classify(p)
            rows.append({"file": p.name, "tier": t, "reason": why, "date_in_name": dn or "", "date_modified": dm,
                         "size_bytes": p.stat().st_size, "include": "yes" if t == "A" else "no"})
    with open(SEL, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()) if rows else None
        if w: w.writeheader(); w.writerows(rows)
    for lab in ("A", "B", "X-other-day", "X-ignore"):
        print(f"\n== Tier {lab}: {sum(r['tier']==lab for r in rows)} files")
        for r in [r for r in rows if r["tier"] == lab][:15]: print("  ", r["file"], "|", r["reason"])
    print(f"\nEdit {SEL} (include=yes/no) or tell Admy which Tier B files to add. Nothing converted yet.")

elif phase in ("preview", "commit"):
    rows = list(csv.DictReader(open(SEL, encoding="utf-8"))); res = []
    for r in rows:
        if r["include"].strip().lower() != "yes": continue
        p = SRC/r["file"]; orig, best = fit(p)
        if not best: res.append({**r, "status": "cannot reach 80% without hurting readability"}); continue
        q, s, data, red = best; out = WORK/"webp"/(p.stem+".webp"); out.write_bytes(data)
        res.append({"file": r["file"], "orig_bytes": orig, "webp_bytes": len(data), "reduction_pct": round(red*100, 1),
                    "quality": q, "scale": s, "sha256_original": sha(p), "status": "ok" if red <= HI else "ok (>89%: tiny source)"})
    ok = [x for x in res if "webp_bytes" in x]
    if phase == "preview":
        for i, x in enumerate(ok[:2], 1):
            a = Image.open(SRC/x["file"]).convert("RGB"); b = Image.open(WORK/"webp"/(Path(x["file"]).stem+".webp")).convert("RGB")
            h = min(1400, a.height); a = a.crop((0, 0, a.width, h)); b = b.resize(a.size).crop((0, 0, a.width, h))
            c = Image.new("RGB", (a.width*2+20, h), "white"); c.paste(a, (0, 0)); c.paste(b, (a.width+20, 0))
            c.save(WORK/f"sample_{i}_original_left_webp_right.png")
        print(f"Preview ready in {WORK}. Per-file results:"); [print("  ", x) for x in res]
    else:
        if not ok: print("nothing to zip"); sys.exit(0)
        o = sum(x["orig_bytes"] for x in ok); w_ = sum(x["webp_bytes"] for x in ok)
        with open(WORK/"manifest.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=ok[0].keys()); w.writeheader(); w.writerows(ok)
        z = Path.cwd()/f"Hermes_Compress_Test_{TODAY}.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED) as zf:
            for x in ok: zf.write(WORK/"webp"/(Path(x["file"]).stem+".webp"), "webp/"+Path(x["file"]).stem+".webp")
            zf.write(WORK/"manifest.csv", "manifest.csv")
            rep = (f"# Hermes Compress Test {TODAY}\nSource day: {DAY}\nFiles: {len(ok)}\nOriginals: {o/1e6:.2f} MB\n"
                   f"WebP total: {w_/1e6:.2f} MB (saved {(1-w_/o)*100:.1f}%)\nZip: {z.stat().st_size/1e6:.2f} MB\n"
                   f"Originals untouched at {SRC}\n")
            zf.writestr("report.md", rep)
        print(rep)
