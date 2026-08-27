import os
import shutil
import hashlib
import argparse

inbox_dir = "/Users/olesiarasing/Obsidian/_Inbox"
projects_dir = "/Users/olesiarasing/Obsidian/01-Projects"
resources_dir = "/Users/olesiarasing/Obsidian/03-Resources"
CONFLICTS_DIR = os.path.join(inbox_dir, "_Conflicts")

# Mapping rules based on keywords
MAPPING = {
    # Project mappings (to go to 01-Projects/<Project-Name>/)
    "LexFlow": ["lexflow", "kit_v2", "rebuild_plan", "fable", "deploy"],
    "Alena-Krot-Med-Expert": ["alena", "krot", "cosmetologa", "med_expert"],
    "Studio-Romanelli": ["romanelli", "Romanelli"],
    "AVibe-CRM": ["avibe", "preventivo"],
    "aLEXy": ["alexy", "aLEXy"],
    "Carrozzeria-2DI": ["carrozzeria", "Carrozzeria", "2di", "2DI"],
    "Avvocato-Pagliano": ["pagliano", "Pagliano"],
    "Genova-Family-Mediation": ["genova", "Genova", "mediatori", "Mediatori"],
    
    # Resource mappings (to go to 03-Resources/<Category>/)
    "AI-Models-and-Prompts": ["model", "Model", "claude", "Claude", "deepseek", "DeepSeek", "nemotron", "gemma", "qwen", "llama", "Laguna", "laguna"],
    "Hermes-Setup-and-MCP": ["hermes", "Hermes", "AGENT_RULES", "setup", "Setup", "runbook", "Runbook", "skill", "Skill", "mcp", "MCP"],
}

def clean_name(name):
    # Standardize string for keyword checking
    return name.lower().replace("_", "-").replace(" ", "-")

def get_destination(filename):
    cleaned = clean_name(filename)
    
    # Check Project keywords first
    for project_name, keywords in MAPPING.items():
        if project_name in ["AI-Models-and-Prompts", "Hermes-Setup-and-MCP"]:
            continue
        for kw in keywords:
            if clean_name(kw) in cleaned:
                return os.path.join(projects_dir, project_name)
                
    # Check Resource keywords second
    for category_name, keywords in MAPPING.items():
        if category_name in ["AI-Models-and-Prompts", "Hermes-Setup-and-MCP"]:
            for kw in keywords:
                if clean_name(kw) in cleaned:
                    return os.path.join(resources_dir, category_name)
                    
    # Default fallback
    return os.path.join(resources_dir, "Reference-General")

def file_hash(filepath):
    """SHA-256 content hash of a file."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def flag_for_review(src_path, dry_run, reason):
    """Move a colliding item to _Inbox/_Conflicts/ instead of deleting anything.
    Returns True if the item was (or would be) removed from its source."""
    label = os.path.basename(src_path)
    msg = f"[FLAG] `{label}`: {reason}. Moving to `_Inbox/_Conflicts/` for review (no deletion)."
    print(msg)
    if not dry_run:
        os.makedirs(CONFLICTS_DIR, exist_ok=True)
        target = os.path.join(CONFLICTS_DIR, label)
        # Avoid clobbering an existing flagged copy
        if os.path.exists(target):
            stem, ext = os.path.splitext(label)
            n = 2
            while os.path.exists(os.path.join(CONFLICTS_DIR, f"{stem} ({n}){ext}")):
                n += 1
            target = os.path.join(CONFLICTS_DIR, f"{stem} ({n}){ext}")
        shutil.move(src_path, target)
    return True

def safe_dest_collision(src_path, dest_path, dry_run):
    """Handle a destination collision per the decision matrix (Part C):
    - identical content  -> auto-fix: drop the source duplicate, keep the destination
    - different content  -> FLAG ONLY: never delete, move source to _Conflicts
    Returns True if the source was resolved (removed from its original location)."""
    label = os.path.basename(src_path)
    if os.path.isdir(dest_path):
        # Directory collision: never rmtree — always flag
        return flag_for_review(src_path, dry_run, f"destination directory already exists at `{dest_path}`")
    if os.path.isfile(src_path) and os.path.isfile(dest_path):
        if file_hash(src_path) == file_hash(dest_path):
            msg = f"[DEDUP] `{label}` byte-identical to existing `{dest_path}`; removing source duplicate."
            print(msg)
            if not dry_run:
                os.remove(src_path)
            return True
        return flag_for_review(src_path, dry_run, f"different content vs existing `{dest_path}`")
    return flag_for_review(src_path, dry_run, f"unexpected collision at `{dest_path}`")

def organize(dry_run=False):
    mode_tag = "[DRY-RUN] " if dry_run else ""
    print(f"{mode_tag}Starting Inbox Organization...")
    
    # Process files/directories in _Inbox root
    for item in os.listdir(inbox_dir):
        item_path = os.path.join(inbox_dir, item)
        if item.startswith('.'):
            continue
        if item == "_Conflicts":
            continue
            
        # Handle the special projects-made-by-hermes folder separately
        if item == "projects-made-by-hermes":
            hermes_projects_path = item_path
            for sub_item in os.listdir(hermes_projects_path):
                sub_item_path = os.path.join(hermes_projects_path, sub_item)
                if sub_item.startswith('.'):
                    continue
                # All these belong to LexFlow project
                target_lexflow_dir = os.path.join(projects_dir, "LexFlow")
                dest_path = os.path.join(target_lexflow_dir, sub_item)
                if os.path.exists(dest_path):
                    safe_dest_collision(sub_item_path, dest_path, dry_run)
                    continue
                if not dry_run:
                    os.makedirs(target_lexflow_dir, exist_ok=True)
                    shutil.move(sub_item_path, target_lexflow_dir)
                print(f"{mode_tag}Moved Hermes-made item `{sub_item}` directly to `01-Projects/LexFlow/`")
            if not dry_run:
                # Remove the now-empty wrapper folder (if still present)
                if os.path.isdir(hermes_projects_path) and not os.listdir(hermes_projects_path):
                    os.rmdir(hermes_projects_path)
            continue

        # For normal items, determine logical path
        dest_folder = get_destination(item)
        dest_path = os.path.join(dest_folder, item)
        
        # Move safely — never delete a differing destination
        if os.path.exists(dest_path):
            safe_dest_collision(item_path, dest_path, dry_run)
            continue
        if not dry_run:
            os.makedirs(dest_folder, exist_ok=True)
            shutil.move(item_path, dest_folder)
        print(f"{mode_tag}Organized `{item}` -> `{os.path.basename(dest_folder)}/`")

    print(f"{mode_tag}Inbox Organization Completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Organize _Inbox into 01-Projects/03-Resources (collision-safe).')
    parser.add_argument('--dry-run', action='store_true', help='Preview actions without moving or deleting anything.')
    args = parser.parse_args()
    organize(dry_run=args.dry_run)
