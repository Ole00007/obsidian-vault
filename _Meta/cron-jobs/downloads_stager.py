# Evening Downloads Stage and Deduplication Script
# Scheduled to run daily at 6:00 PM (18:00)

import os
import shutil
import glob
import hashlib
import argparse
from datetime import datetime

DOWNLOADS_DIR = os.path.expanduser('~/Downloads')
VAULT_INBOX = os.path.expanduser('~/Obsidian/_Inbox')
CONFLICTS_DIR = os.path.join(VAULT_INBOX, '_Conflicts')
DAILY_NOTES_DIR = os.path.expanduser('~/Obsidian/05-Daily')

# Target document file extensions to ingest
ALLOWED_EXTENSIONS = ('.md', '.pdf', '.docx', '.xlsx', '.csv', '.txt')

# Sensitive/excluded name patterns — NEVER staged, regardless of extension.
# Covers credentials, secrets, keys, and git/version-control files (Part A exclusion list).
EXCLUDE_PATTERNS = (
    'credential', 'secret', 'password', 'passwd', 'token',
    'apikey', 'api_key', '.env', '.pem', '.key', '.git', '.ssh',
)

def is_excluded(filename):
    low = filename.lower()
    return any(pat in low for pat in EXCLUDE_PATTERNS)

def get_or_create_daily_note():
    today = datetime.now().strftime('%Y-%m-%d')
    note_path = os.path.join(DAILY_NOTES_DIR, f"{today}.md")
    os.makedirs(DAILY_NOTES_DIR, exist_ok=True)
    if not os.path.exists(note_path):
        with open(note_path, 'w') as f:
            f.write(f"---\ntitle: Daily Log {today}\ncreated: {today}\ntags: [daily-notes]\nstatus: active\n---\n\n# Daily Note - {today}\n\n## Daily Staging Log\n")
    return note_path

def log_to_daily_note(message):
    note_path = get_or_create_daily_note()
    with open(note_path, 'a') as f:
        f.write(f"- {message}\n")

def file_hash(filepath):
    """SHA-256 content hash of a file."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def check_vault_for_duplicates(filename):
    # Scan Projects, Areas, Archive, and Inbox for existing copies
    paths_to_check = [
        os.path.expanduser('~/Obsidian/01-Projects'),
        os.path.expanduser('~/Obsidian/02-Areas'),
        os.path.expanduser('~/Obsidian/04-Archive'),
        os.path.expanduser('~/Obsidian/_Inbox')
    ]
    for base_path in paths_to_check:
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                if filename in files:
                    return os.path.join(root, filename)
    return None

def run_staging(dry_run=False):
    mode_tag = "[DRY-RUN] " if dry_run else ""
    print(f"{mode_tag}Starting daily staging job...")
    if not dry_run:
        os.makedirs(VAULT_INBOX, exist_ok=True)
    
    # Grab files updated/created in downloads
    files_to_check = glob.glob(os.path.join(DOWNLOADS_DIR, '*'))
    staged_count = 0
    conflict_count = 0
    skipped_count = 0
    excluded_count = 0

    for file_path in files_to_check:
        if os.path.isdir(file_path):
            continue
        
        filename = os.path.basename(file_path)
        if not filename.endswith(ALLOWED_EXTENSIONS):
            continue
            
        # Ignore hidden/system files
        if filename.startswith('.'):
            continue

        # Part A exclusion list — never stage sensitive/credential files
        if is_excluded(filename):
            excluded_count += 1
            continue

        # Check for duplicates inside Projects, Areas, Archive, or Inbox
        duplicate_path = check_vault_for_duplicates(filename)
        
        if duplicate_path:
            # Same filename exists in vault — compare CONTENT, not just name
            if file_hash(file_path) == file_hash(duplicate_path):
                # Byte-identical: not a real conflict, skip silently
                skipped_count += 1
                continue
            # Content differs: real conflict, stage under _Conflicts
            if not dry_run:
                os.makedirs(CONFLICTS_DIR, exist_ok=True)
                conflict_target = os.path.join(CONFLICTS_DIR, filename)
                shutil.copy2(file_path, conflict_target)
            msg = f"[CONFLICT] Different content for `{filename}` vs vault at `{duplicate_path}`. Would stage copy in `_Inbox/_Conflicts/` for review."
            print(f"{mode_tag}{msg}")
            if not dry_run:
                log_to_daily_note(msg)
            conflict_count += 1
        else:
            # Clean copy to Inbox root
            if not dry_run:
                inbox_target = os.path.join(VAULT_INBOX, filename)
                shutil.copy2(file_path, inbox_target)
            msg = f"[STAGED] Would stage `{filename}` from Downloads to `_Inbox/`."
            print(f"{mode_tag}{msg}")
            if not dry_run:
                log_to_daily_note(msg)
            staged_count += 1
            
    print(f"{mode_tag}Job completed. Staged: {staged_count}, Conflicts Flagged: {conflict_count}, Skipped (identical): {skipped_count}, Excluded: {excluded_count}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stage new Downloads into Obsidian _Inbox (copy-only, non-destructive).')
    parser.add_argument('--dry-run', action='store_true', help='Preview actions without copying or logging anything.')
    args = parser.parse_args()
    run_staging(dry_run=args.dry_run)
