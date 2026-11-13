#!/usr/bin/env python3
"""case_tools.py v2 - deterministic helpers for the Case Swarm (private use). Standard library only.
  init <name>                         create case folder layout
  hash <case_dir> | verify <case_dir> SHA-256 manifest of 00_originals
  parse-wa <case_dir> [--rename "You=Name"]...   WhatsApp export (.zip/.txt) in 00_originals -> 04_analysis/messages.csv
  count <case_dir> [lexicon.json]     literal / synonym / ambiguous counts
  citecheck <file.md>                 every substantive line must cite [M12] or [S1:M12]
  archive <case_dir>                  ONLY if ANALYSIS_COMPLETE exists
Never modifies or deletes originals."""
import sys, csv, re, json, hashlib, shutil, subprocess, tarfile, zipfile, datetime as dt
from pathlib import Path
from collections import defaultdict

DIRS = ["00_originals","01_sources","02_transcripts_A","02_transcripts_B","03_merged","04_analysis",
        "05_summary","06_deliverables","07_audit","08_archive"]
STOP = set("the a an and or but to of in on at is it i you he she we they me my your this that for with was are be "
           "и в не на я он она мы вы они что это с по а но да нет "
           "il lo la le un una e o ma di da in su per con è sono che non mi ti si".split())

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

def norm(t):
    t = re.sub(r"[^\w\s']", " ", (t or "").lower(), flags=re.UNICODE)
    return re.sub(r"\s+", " ", t).strip()

def cmd_init(name):
    root = Path(f"case_{name}_{dt.date.today()}"); [(root / d).mkdir(parents=True, exist_ok=True) for d in DIRS]
    print(root)

def cmd_hash(case):
    case = Path(case); rows = []
    for p in sorted((case / "00_originals").rglob("*")):
        if p.is_file() and p.name != "manifest.csv": rows.append((str(p.relative_to(case / "00_originals")), p.stat().st_size, sha(p)))
    with open(case / "00_originals/manifest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["path", "bytes", "sha256"]); w.writerows(rows)
    print(f"{len(rows)} files hashed")

def cmd_verify(case):
    case = Path(case); bad = []
    for r in csv.DictReader(open(case / "00_originals/manifest.csv", encoding="utf-8")):
        p = case / "00_originals" / r["path"]
        if not p.exists() or sha(p) != r["sha256"]: bad.append(r["path"])
    print("OK: all originals match" if not bad else f"MISMATCH: {bad}"); return not bad

WA = [re.compile(r"^\[(\d{1,2}[./]\d{1,2}[./]\d{2,4}),?\s+(\d{1,2}[:.]\d{2}(?:[:.]\d{2})?)\]\s+([^:]+?):\s(.*)$"),
      re.compile(r"^(\d{1,2}[./]\d{1,2}[./]\d{2,4}),?\s+(\d{1,2}[:.]\d{2}(?:[:.]\d{2})?)\s+-\s+([^:]+?):\s(.*)$")]
SYS = re.compile(r"^\[?\d{1,2}[./]\d{1,2}[./]\d{2,4},?\s+\d{1,2}[:.]\d{2}")
def cmd_parse_wa(case, renames):
    case = Path(case); out = []; n = 0; sidx = 0; ren = dict(x.split("=", 1) for x in renames)
    for p in sorted((case / "00_originals").rglob("*")):
        if p.suffix.lower() not in (".zip", ".txt"): continue
        if p.suffix.lower() == ".zip":
            with zipfile.ZipFile(p) as z:
                names = [x for x in z.namelist() if x.lower().endswith(".txt")]
                if not names: continue
                text = z.read(names[0]).decode("utf-8", "replace")
        else: text = p.read_text(encoding="utf-8", errors="replace")
        sidx += 1; sid = f"S{sidx}"; cur = None
        for line in text.replace("\u200e", "").replace("\u202f", " ").splitlines():
            m = next((r.match(line) for r in WA if r.match(line)), None)
            if m:
                n += 1; d, t, who, body = m.groups(); who = ren.get(who.strip(), who.strip())
                cur = {"msg_id": f"M{n}", "source_id": sid, "sender": who, "text_original": body, "timestamp": f"{d} {t}",
                       "recipient": "", "source_type": "whatsapp", "language": "", "translation": "", "transcription_confidence": "exact",
                       "transcriber_diff": "n", "authenticity_flag": "", "notes": p.name}
                out.append(cur)
            elif SYS.match(line): cur = None   # system line (encryption notice, joined, etc.): skipped
            elif cur is not None and line.strip(): cur["text_original"] += "\n" + line
    f = case / "04_analysis/messages.csv"
    with open(f, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["msg_id","source_id","sender","text_original","timestamp","recipient","source_type","language","translation","transcription_confidence","transcriber_diff","authenticity_flag","notes"])
        w.writeheader(); w.writerows(out)
    print(f"{len(out)} messages from {sidx} sources -> {f}. Check senders and date format (dd/mm vs mm/dd) manually.")

def cmd_count(case, lex_path=None):
    case = Path(case); msgs = list(csv.DictReader(open(case / "04_analysis/messages.csv", encoding="utf-8")))
    lex = json.load(open(lex_path, encoding="utf-8")) if lex_path else {"clusters": {}, "ambiguous": []}
    lit = defaultdict(list); clu = defaultdict(lambda: defaultdict(list)); amb = defaultdict(list); out = []
    for m in msgs:
        t = norm(m["text_original"]); toks = t.split(); who = m["sender"]; src = m["source_id"]
        if not re.search(r"\w", m["text_original"] or ""): amb[(who, src, "[emoji/symbol-only]")].append(m["msg_id"]); continue
        for n in range(1, 6):
            for i in range(len(toks) - n + 1):
                g = toks[i:i + n]
                if all(x in STOP for x in g): continue
                lit[(who, src, " ".join(g))].append(m["msg_id"])
        for cname, members in lex["clusters"].items():
            for mem in members:
                k = len(re.findall(rf"(?<!\w){re.escape(norm(mem))}(?!\w)", t))
                for _ in range(k): clu[(who, src, cname)][mem].append(m["msg_id"])
        for a in lex["ambiguous"]:
            if re.search(rf"(?<!\w){re.escape(norm(a))}(?!\w)", t): amb[(who, src, a)].append(m["msg_id"])
    def emit(scope, who, src, key, typ, ids, detail=""):
        out.append({"scope": scope, "participant": who, "source_id": src, "phrase_or_cluster": key, "type": typ,
                    "count": len(ids), "msg_ids": " ".join(sorted(set(ids))), "members_detail": detail})
    tot_lit = defaultdict(list)
    for (who, src, g), ids in lit.items():
        if len(ids) >= 2: emit("file", who, src, g, "literal", ids); tot_lit[(who, g)] += ids
    for (who, g), ids in tot_lit.items(): emit("overall", who, "ALL", g, "literal", ids)
    tot_clu = defaultdict(lambda: defaultdict(list))
    for (who, src, c), mem in clu.items():
        allids = [i for v in mem.values() for i in v]
        emit("file", who, src, c, "synonym_cluster", allids, json.dumps({k: len(v) for k, v in mem.items()}, ensure_ascii=False))
        for k, v in mem.items(): tot_clu[(who, c)][k] += v
    for (who, c), mem in tot_clu.items():
        allids = [i for v in mem.values() for i in v]
        emit("overall", who, "ALL", c, "synonym_cluster", allids, json.dumps({k: len(v) for k, v in mem.items()}, ensure_ascii=False))
    for (who, src, a), ids in amb.items(): emit("file", who, src, a, "ambiguous_NOT_COUNTED", ids)
    path = case / "04_analysis/phrase_counts.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["scope", "participant", "source_id", "phrase_or_cluster", "type", "count", "msg_ids", "members_detail"])
        w.writeheader(); w.writerows(out)
    q = ["# Ambiguous items - please clarify\n"] + [f"- {who} / {src}: '{a}' x{len(ids)} ({' '.join(sorted(set(ids)))}) - meaning?" for (who, src, a), ids in amb.items()]
    (case / "05_summary").mkdir(exist_ok=True); (case / "05_summary/ambiguous_questions.md").write_text("\n".join(q) + "\n", encoding="utf-8")
    print(f"{len(out)} rows -> {path}")

CITE = re.compile(r"\[(?:[A-Za-z0-9_\-]+:)?M\d+\]")
def cmd_citecheck(f):
    bad = [(i, l) for i, l in enumerate(Path(f).read_text(encoding="utf-8").splitlines(), 1)
           if len(l.strip()) > 40 and not l.lstrip().startswith(("#", "|", "```", ">")) and not CITE.search(l)]
    for i, l in bad: print(f"line {i} uncited: {l[:70]}")
    print("citecheck PASS" if not bad else f"citecheck FAIL ({len(bad)} lines)"); return not bad

def cmd_archive(case):
    case = Path(case)
    if not (case / "ANALYSIS_COMPLETE").exists(): sys.exit("Refused: create file ANALYSIS_COMPLETE first (user confirmation).")
    if not cmd_verify(case): sys.exit("Refused: originals do not match manifest.")
    out = case / "08_archive"; out.mkdir(exist_ok=True); name = f"{case.name}_originals"
    if shutil.which("zstd"):
        tar = out / f"{name}.tar"
        with tarfile.open(tar, "w") as t: t.add(case / "00_originals", arcname="00_originals")
        subprocess.run(["zstd", "--ultra", "-22", "-T0", "-q", "-f", str(tar), "-o", str(tar) + ".zst"], check=True); tar.unlink(); arc = Path(str(tar) + ".zst"); how = "tar + zstd --ultra -22"
    else:
        arc = out / f"{name}.tar.xz"
        with tarfile.open(arc, "w:xz", preset=9) as t: t.add(case / "00_originals", arcname="00_originals")
        how = "tar + xz -9 (zstd not found)"
    idx = (f"# Archive index\nCase: {case.name}\nDate: {dt.date.today()}\nArchive: {arc.name}\nMethod: {how}\n"
           f"Archive SHA-256: {sha(arc)}\nRestore: extract the archive, then run: python case_tools.py verify <case_dir>\n"
           f"Originals NOT deleted. Deleting loose originals requires the typed phrase CONFIRM DELETE.\n")
    (out / "archive_index.md").write_text(idx, encoding="utf-8"); print(idx)

if __name__ == "__main__":
    a = sys.argv[1:]; c = a[0] if a else ""
    if c == "init": cmd_init(a[1])
    elif c == "hash": cmd_hash(a[1])
    elif c == "verify": sys.exit(0 if cmd_verify(a[1]) else 1)
    elif c == "parse-wa": cmd_parse_wa(a[1], [a[i+1] for i, x in enumerate(a) if x == "--rename"])
    elif c == "count": cmd_count(a[1], a[2] if len(a) > 2 else None)
    elif c == "citecheck": sys.exit(0 if cmd_citecheck(a[1]) else 1)
    elif c == "archive": cmd_archive(a[1])
    else: print(__doc__)
