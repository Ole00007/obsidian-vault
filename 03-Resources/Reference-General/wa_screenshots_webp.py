#!/usr/bin/env python3
"""WhatsApp screenshot test: WebP at 80-89% size reduction. Phases: preview | commit"""
import sys, io, json, zipfile, datetime as dt
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / "Pictures" / "Screenshots"
OUT = Path("wa_test_out"); OUT.mkdir(exist_ok=True)
DAY = (dt.date.today() - dt.timedelta(days=1))
LO, HI, MIN_W = 0.80, 0.89, 720

def is_wa_shot(p):
    n = p.name.lower()
    d = dt.date.fromtimestamp(p.stat().st_mtime)
    return p.suffix.lower() in {".png", ".jpg", ".jpeg"} and "whatsapp" in n and "screenshot" in n and d == DAY

def encode(img, q, scale):
    im = img if scale == 1 else img.resize((int(img.width*scale), int(img.height*scale)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "WEBP", quality=q, method=6); return b.getvalue()

def fit(path):
    orig = path.stat().st_size
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    for scale in (1.0, 0.9, 0.8, 0.7, 0.6):
        if img.width*scale < MIN_W and scale != 1.0: break
        lo, hi, best = 10, 95, None
        while lo <= hi:                       # highest quality still reaching >=80% reduction
            q = (lo+hi)//2; data = encode(img, q, scale); red = 1 - len(data)/orig
            if red >= LO: best = (q, scale, data, red); lo = q+1
            else: hi = q-1
        if best: return orig, best
    return orig, None

files = sorted(p for p in SRC.rglob("*") if p.is_file() and is_wa_shot(p))
rows = []
for p in files:
    orig, best = fit(p)
    if not best: rows.append({"file": p.name, "orig": orig, "status": "cannot reach 80% without hurting readability"}); continue
    q, s, data, red = best
    (OUT/(p.stem+".webp")).write_bytes(data)
    rows.append({"file": p.name, "orig": orig, "new": len(data), "reduction": round(red*100, 1), "q": q, "scale": s,
                 "status": "ok" if red <= HI else "ok (above 89%: lower than needed; q capped)"})
json.dump(rows, open(OUT/"plan.json", "w"), indent=1)

if sys.argv[1] == "preview":
    print(f"{len(files)} screenshots dated {DAY}. Open 1-2 .webp files in {OUT}/ and compare with the originals.")
    for r in rows: print(r)
elif sys.argv[1] == "commit":
    ok = [r for r in rows if "new" in r]
    z = OUT/f"whatsapp_screens_{DAY}.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED) as zf:   # WebP is already compressed
        for r in ok: zf.write(OUT/(Path(r["file"]).stem+".webp"), Path(r["file"]).stem+".webp")
    if not ok: print("nothing to zip"); sys.exit(0)
    o = sum(r["orig"] for r in ok); n = z.stat().st_size
    print(f"originals {o/1e6:.2f} MB -> zip {n/1e6:.2f} MB, saved {(o-n)/1e6:.2f} MB ({(1-n/o)*100:.1f}%)")
