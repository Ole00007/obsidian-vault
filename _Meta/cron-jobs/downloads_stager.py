#!/usr/bin/env python3
"""
downloads_stager.py  -  Daily Downloads -> Obsidian _Inbox stager.

Scans ~/Downloads for files modified within a recency window (default 24h),
then for each candidate:
  - content already anywhere in the VAULT -> leave alone        (SKIP identical-vault)
  - not yet in _Inbox                     -> copy2() into _Inbox (STAGED)
  - in _Inbox, identical                  -> leave as-is         (SKIP identical)
  - in _Inbox, differs                    -> copy2() the Downloads copy into
                                             _Inbox/_Conflicts/   (CONFLICT)

IDENTITY IS WHOLE-VAULT, NOT INBOX-ONLY (2026-09-23 fix).
The old check compared the Downloads file only against the same-named file in
_Inbox. A download already filed under 03-Resources/ (or any other folder) was
therefore re-staged, and the _Conflicts sweeper then quarantined a byte-identical
copy -- that single mechanism produced 100% of one week's false-positive
quarantines. Now the file's md5 is matched against an index of the entire vault
(excluding _Trash/, .git/ and _Inbox/_Conflicts/) and skipped as
[IDENTICAL-VAULT] when a copy already exists.

System junk (.DS_Store, Thumbs.db) and files outside the window are excluded.
Idempotent: safe to run repeatedly. A JSON manifest is written to the profile
logs dir on every real run.
"""
import os
import sys
import json
import shutil
import hashlib
import datetime
import argparse

HOME = os.path.expanduser("~")
DOWNLOADS = os.path.join(HOME, "Downloads")
VAULT = os.path.join(HOME, "Obsidian")
INBOX = os.path.join(VAULT, "_Inbox")
CONFLICTS = os.path.join(INBOX, "_Conflicts")
EXCLUDE = {".DS_Store", "Thumbs.db", "Desktop.ini"}

# Directories that must NOT count as "already in the vault" for identity purposes:
# _Trash/ is the 30-day quarantine (pruned), and _Inbox/_Conflicts/ is where
# duplicates are parked for review -- neither is a durable home for a file.
INDEX_SKIP_DIRS = {".git", "_Trash", "_Conflicts"}

# Sensitive-name exclusion -- NEVER staged, regardless of extension.
# RESTORED 2026-09-23: the live script had regressed to a version WITHOUT this
# list (the vault backup still had it), so a Google OAuth client-secret JSON
# sitting in ~/Downloads was a staging candidate -> the vault is auto-committed
# and pushed, so it would have been published. Never remove this list.
EXCLUDE_PATTERNS = (
    "credential", "secret", "password", "passwd", "token",
    "apikey", "api_key", "api-key", ".env", ".pem", ".key", ".git", ".ssh",
    "client_secret", "google_token", "oauth", "service_account",
    "id_rsa", "id_ed25519", "id_ecdsa", ".p12", ".pfx", ".keystore",
    ".sqlite", ".db", "wallet", "recovery",
)


def is_sensitive(name):
    """True when the filename looks like a credential/secret bearing file."""
    low = name.lower()
    return any(pat in low for pat in EXCLUDE_PATTERNS)


def md5(path, chunk=1 << 16):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def build_vault_index():
    """md5 -> first path for every durable file in the vault.

    Built lazily (only when there is at least one staging candidate) so idle
    runs stay cheap. Skips .git/, _Trash/ and _Inbox/_Conflicts/.
    """
    index = {}
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in INDEX_SKIP_DIRS]
        for fn in files:
            if fn in EXCLUDE:
                continue
            p = os.path.join(root, fn)
            try:
                index.setdefault(md5(p), p)
            except OSError:
                pass
    return index


def main(argv=None):
    ap = argparse.ArgumentParser(description="Stage recent Downloads into Obsidian _Inbox.")
    ap.add_argument("--hours", type=float, default=24.0, help="recency window in hours")
    ap.add_argument("--dry-run", action="store_true", help="report intent without writing")
    ap.add_argument(
        "--log-dir",
        default=os.path.join(HOME, ".hermes", "profiles", "memory-curator", "logs"),
    )
    args = ap.parse_args(argv)

    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(hours=args.hours)
    dry = args.dry_run

    if not dry:
        os.makedirs(CONFLICTS, exist_ok=True)
        os.makedirs(args.log_dir, exist_ok=True)

    report = {
        "run_at": now.isoformat(timespec="seconds"),
        "window_hours": args.hours,
        "dry_run": dry,
        "staged": [],
        "skipped_identical": [],
        "skipped_identical_vault": [],
        "conflicts": [],
        "excluded": [],
        "excluded_sensitive": [],
        "errors": [],
    }

    if not os.path.isdir(DOWNLOADS):
        report["errors"].append(f"Downloads dir not found: {DOWNLOADS}")
        print(json.dumps(report, indent=2))
        return report

    # Lazy whole-vault identity index: built on the first staging candidate only.
    vault_index = None

    for name in sorted(os.listdir(DOWNLOADS)):
        if name in EXCLUDE:
            report["excluded"].append(name)
            continue
        if is_sensitive(name):
            # Credential-looking file: never staged, never logged by name into
            # the daily note beyond a count. This is the guard that keeps the
            # public vault repo free of secrets.
            report["excluded_sensitive"].append(name)
            continue
        src = os.path.join(DOWNLOADS, name)
        if not os.path.isfile(src):
            continue
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(src))
        if mtime < cutoff:
            continue  # outside recency window -> not a candidate for today

        dest = os.path.join(INBOX, name)
        try:
            src_md5 = md5(src)
        except OSError as e:
            report["errors"].append(f"{name}: read error {e}")
            continue

        # 1) Already filed ANYWHERE in the vault? Then this download is a
        #    re-download of known content -> do not stage, do not flag.
        if vault_index is None:
            vault_index = build_vault_index()
        twin = vault_index.get(src_md5)
        if twin:
            report["skipped_identical_vault"].append(
                {"name": name, "twin": os.path.relpath(twin, HOME)}
            )
            continue

        # 2) New content.
        if not os.path.exists(dest):
            if not dry:
                shutil.copy2(src, dest)
            report["staged"].append(name)
            continue

        try:
            dest_md5 = md5(dest)
        except OSError as e:
            report["errors"].append(f"{name}: dest read error {e}")
            dest_md5 = None

        if dest_md5 == src_md5:
            report["skipped_identical"].append(name)
        else:
            cpath = os.path.join(CONFLICTS, name)
            if os.path.exists(cpath):
                try:
                    if md5(cpath) != src_md5:
                        cpath = os.path.join(
                            CONFLICTS, f"{name}.{now:%Y%m%d-%H%M%S}"
                        )
                except OSError:
                    pass
            if not dry:
                shutil.copy2(src, cpath)
            report["conflicts"].append(
                {
                    "name": name,
                    "inbox_md5": dest_md5,
                    "downloads_md5": src_md5,
                    "conflict_copy": os.path.relpath(cpath, HOME),
                }
            )

    if not dry:
        logp = os.path.join(args.log_dir, f"downloads_stager_{now:%Y-%m-%d}.json")
        try:
            # merge with prior runs today if present
            if os.path.exists(logp):
                with open(logp) as f:
                    prior = json.load(f)
                if isinstance(prior, list):
                    prior.append(report)
                else:
                    prior = [prior, report]
                data = prior
            else:
                data = [report]
            with open(logp, "w") as f:
                json.dump(data, f, indent=2)
            report["manifest"] = logp
        except OSError as e:
            report["errors"].append(f"manifest write error: {e}")

    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    main()
