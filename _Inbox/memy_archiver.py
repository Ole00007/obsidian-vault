#!/usr/bin/env python3
"""memy_archiver.py - ONE file for Memy's temporary ARCHIVER role (trial, 2026-11-06).
Contains: model config, role brief + approval gates, personal-archive policy, and the
compression engine. Usage:
  python memy_archiver.py brief | config | policy      (print instructions/data, no side effects)
  python memy_archiver.py scan|preview|commit <SRC_DIR> [--day YYYY-MM-DD]
Originals are NEVER modified, moved or deleted."""
import sys, json

MODEL_CONFIG_YAML = """model:
  provider: openrouter
  default: z-ai/glm-5.2:free
fallback_providers:
  - provider: openrouter
    model: nvidia/nemotron-3.5-lightning:free
  - provider: openrouter
    model: minimax/minimax-m3:free
"""

ROLE_BRIEF = """ROLE (temporary, additive): You remain Memy, memory curator. For this job you also act as ARCHIVER.
Oversight and control: Admy (CEO). Do not store this role as a standing rule until Admy says FIX AS RULE.
Permission: read ~/Desktop top level only; write only to ./Hermes_Compress_Test_<date>/ and one zip beside it. Admy can revoke at any time with REVOKE ARCHIVER ACCESS; stop immediately.
Safety: never modify/move/delete originals; never read, OCR or send image content to any model;
use only this file's scan/preview/commit; free tier ~50 requests/day, 20/min -> plan 10-20 requests,
one shell command per phase, never loop per file through the model.
GATE 1: run scan; show groups A (WhatsApp in name + target-day date), B (generic screenshot, unverified, excluded
by default), X-other-day, X-ignore with counts; list Tier A name/date(name+modified)/size/reason; flag date
mismatches. STOP until Admy says APPROVE SELECTION (optionally naming Tier B files).
GATE 2: run preview; WebP 80-89% smaller (highest quality reaching >=80%); show 1-2 samples + per-file table;
report files that cannot reach 80% without hurting readability. STOP until APPROVE COMPRESSION.
GATE 3: run commit; ONE zip Hermes_Compress_Test_<date>.zip (webp/, manifest.csv with SHA-256 of originals,
report.md). Report originals MB, zip MB, MB and % saved. Do not delete originals.
FINAL: report model used, whether a fallback fired, requests spent, surprises. Admy decides FIX AS RULE / REVERT ROLE."""

POLICY = {
  "scope": "personal archive only; goal = save space and money; legal retention rules not applied",
  "recompress_ok": ["personal photos", "screenshots", "reference scans", "drafts", "downloads", "media"],
  "never_recompress": ["signed files (.p7m .p7s .sig, signed PDF/XML)", "contracts", "tax", "invoices", "ID", "medical", "court filings"],
  "originals": "dedup backup (restic/borg) + SHA-256 manifest; cold archives tar+zstd --ultra -22 -T0; zstd -3 for already-compressed data",
  "documents": "plain optimised PDF (not PDF/A): ocrmypdf --optimize 3 for scans; ghostscript /ebook + qpdf for native; JBIG2 lossless only",
  "images": "WebP q80 (lossless for text-heavy); previews optional, off by default",
  "video": "H.265 CRF 26-28 or AV1 via ffmpeg MCP (ffmpeg-mcp-lite, dubnium0/ffmpeg-mcp)",
  "audio": "Opus 24-32 kbps speech, 64-96 kbps music",
  "archives": "fast restore: tar+zstd -22; smallest/slow: xz -9e or 7z LZMA2; restore is CPU-time only locally; add par2",
  "embeddings": "search index only, never a substitute for the original",
  "fallback_paid": "DeepSeek V4 Flash (~$0.05 in / $0.16 out per 1M tokens)",
}

if len(sys.argv) > 1 and sys.argv[1] in ("brief", "config", "policy"):
    print({"brief": ROLE_BRIEF, "config": MODEL_CONFIG_YAML, "policy": json.dumps(POLICY, indent=2)}[sys.argv[1]])
    sys.exit(0)

import io, re, csv, hashlib, zipfile, datetime as dt
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
    elif d == DAY and ("screenshot" in n or "screen shot" in n): tier, why = "B", "generic screenshot, date matches, WhatsApp NOT verified"
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
    if rows:
        with open(SEL, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
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
            h = min(1400, a.height); a = a.crop((0, 0, a.width, h)); b = b.resize((a.width, a.height)).crop((0, 0, a.width, h))
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
