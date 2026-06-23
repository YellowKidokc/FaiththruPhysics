"""
Deduplicate and inventory all Excel/CSV files for the Moral Decline of America data package.
Searches known locations, deduplicates by filename+size, copies unique files to staging folder.
"""
import os
import hashlib
import shutil
import json
from collections import defaultdict

# All known locations with moral decline data
SEARCH_PATHS = [
    r"C:\Users\lowes\Documents\1900-2025 The Moral Decay of America",
    r"O:\_Theophysics_v4\00_ARCHIVE\__DATA\Cross_Domain_Heavy\06_History_AW\02_Evidence\01_Evidence_Bundles\1900-2025_The_Moral_Decay_of_America",
    r"O:\_Theophysics_v4\00_ARCHIVE\__DATA\Cross_Domain_Heavy\06_History_AW\02_Evidence",
    r"O:\_Theophysics_v4\00_ARCHIVE\__DATA\Cross_Domain_Heavy",
    r"O:\_Theophysics_v4\__DATA",
    r"C:\Users\lowes\Documents",
]

EXTENSIONS = {'.xlsx', '.xls', '.csv'}
STAGING = r"C:\temp\moral_decline_data_package"

def file_hash(path, block_size=65536):
    """Get MD5 hash of file contents for true dedup."""
    h = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            while True:
                data = f.read(block_size)
                if not data:
                    break
                h.update(data)
        return h.hexdigest()
    except Exception as e:
        return f"ERROR:{e}"

def find_all_data_files():
    """Walk all search paths and collect every Excel/CSV file."""
    all_files = []
    seen_paths = set()

    for base in SEARCH_PATHS:
        if not os.path.exists(base):
            print(f"SKIP (not found): {base}")
            continue
        print(f"Scanning: {base}")
        count = 0
        for root, dirs, files in os.walk(base):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in EXTENSIONS:
                    full = os.path.join(root, f)
                    norm = os.path.normcase(os.path.normpath(full))
                    if norm not in seen_paths:
                        seen_paths.add(norm)
                        try:
                            size = os.path.getsize(full)
                        except:
                            size = 0
                        all_files.append({
                            'name': f,
                            'path': full,
                            'size': size,
                            'ext': ext,
                            'source': base
                        })
                        count += 1
        print(f"  Found {count} new files")

    return all_files

def deduplicate(all_files):
    """Group by filename+size, then hash to confirm true duplicates."""
    # Group by (name, size)
    groups = defaultdict(list)
    for f in all_files:
        key = (f['name'].lower(), f['size'])
        groups[key].append(f)

    unique = []
    dupes = []
    hash_checked = 0

    for key, group in groups.items():
        if len(group) == 1:
            unique.append(group[0])
        else:
            # Multiple files with same name+size - hash them
            hashes = {}
            for f in group:
                h = file_hash(f['path'])
                hash_checked += 1
                if h not in hashes:
                    hashes[h] = f
                    unique.append(f)
                else:
                    dupes.append({
                        'duplicate': f['path'],
                        'kept': hashes[h]['path'],
                        'hash': h
                    })

    return unique, dupes, hash_checked

def copy_to_staging(unique_files):
    """Copy unique files to flat staging folder, handling name collisions."""
    os.makedirs(STAGING, exist_ok=True)

    used_names = {}
    copied = 0
    errors = []

    for f in sorted(unique_files, key=lambda x: x['name'].lower()):
        name = f['name']
        base, ext = os.path.splitext(name)

        # Handle name collisions (different content, same filename)
        dest_name = name
        counter = 1
        while dest_name.lower() in used_names:
            dest_name = f"{base}_{counter}{ext}"
            counter += 1

        used_names[dest_name.lower()] = f['path']
        dest = os.path.join(STAGING, dest_name)

        try:
            shutil.copy2(f['path'], dest)
            f['staged_name'] = dest_name
            copied += 1
        except Exception as e:
            errors.append({'file': f['path'], 'error': str(e)})
            f['staged_name'] = f"ERROR: {e}"

    return copied, errors

def main():
    print("=" * 60)
    print("MORAL DECLINE DATA PACKAGE - DEDUP & STAGE")
    print("=" * 60)

    # Step 1: Find all files
    print("\n--- STEP 1: Finding all data files ---")
    all_files = find_all_data_files()
    print(f"\nTotal files found: {len(all_files)}")

    # Step 2: Deduplicate
    print("\n--- STEP 2: Deduplicating ---")
    unique, dupes, hash_checked = deduplicate(all_files)
    print(f"Hash checks performed: {hash_checked}")
    print(f"Unique files: {len(unique)}")
    print(f"Duplicates removed: {len(dupes)}")

    # Step 3: Copy to staging
    print(f"\n--- STEP 3: Copying to {STAGING} ---")
    copied, errors = copy_to_staging(unique)
    print(f"Files copied: {copied}")
    if errors:
        print(f"Copy errors: {len(errors)}")
        for e in errors:
            print(f"  ERROR: {e['file']} -> {e['error']}")

    # Step 4: Summary
    print("\n--- SUMMARY ---")
    print(f"Total found:      {len(all_files)}")
    print(f"Duplicates:       {len(dupes)}")
    print(f"Unique files:     {len(unique)}")
    print(f"Successfully staged: {copied}")

    # Breakdown by extension
    ext_counts = defaultdict(int)
    ext_sizes = defaultdict(int)
    for f in unique:
        ext_counts[f['ext']] += 1
        ext_sizes[f['ext']] += f['size']

    print("\nBy type:")
    for ext in sorted(ext_counts.keys()):
        size_mb = ext_sizes[ext] / (1024*1024)
        print(f"  {ext}: {ext_counts[ext]} files ({size_mb:.1f} MB)")

    total_mb = sum(ext_sizes.values()) / (1024*1024)
    print(f"  TOTAL: {sum(ext_counts.values())} files ({total_mb:.1f} MB)")

    # Save manifest
    manifest_path = os.path.join(STAGING, "_MANIFEST.json")
    manifest = {
        'total_found': len(all_files),
        'duplicates_removed': len(dupes),
        'unique_files': len(unique),
        'files': [
            {
                'staged_name': f.get('staged_name', ''),
                'original_name': f['name'],
                'original_path': f['path'],
                'size_bytes': f['size'],
                'extension': f['ext'],
                'source_location': f['source']
            }
            for f in sorted(unique, key=lambda x: x['name'].lower())
        ],
        'duplicates': dupes[:20]  # First 20 dupes for reference
    }

    with open(manifest_path, 'w', encoding='utf-8') as mf:
        json.dump(manifest, mf, indent=2, ensure_ascii=False)
    print(f"\nManifest saved to: {manifest_path}")

    # Print first 30 files as preview
    print("\n--- FILE PREVIEW (first 30) ---")
    for f in sorted(unique, key=lambda x: x['name'].lower())[:30]:
        size_kb = f['size'] / 1024
        print(f"  {f.get('staged_name', f['name'])} ({size_kb:.0f} KB)")

    if len(unique) > 30:
        print(f"  ... and {len(unique) - 30} more")

    print("\nDONE.")

if __name__ == '__main__':
    main()
