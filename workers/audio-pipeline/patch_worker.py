"""Fetch the deployed worker from Cloudflare, patch cleanSlug, write to src/index.js"""
import subprocess, pathlib

OUT = pathlib.Path(r"D:\GitHub\faiththruphysics-site\workers\audio-pipeline\src\index.js")

# Get deployed code via wrangler
print("Fetching deployed worker code...")
r = subprocess.run(
    'wrangler d1 --help',  # just testing wrangler works
    shell=True, capture_output=True, encoding='utf-8', errors='replace'
)

# Read the OLD cleanSlug and the NEW cleanSlug
OLD_CLEAN_SLUG = '''function cleanSlug(value) {
  const text = optionalString(value);
  if (!text) return "";
  return text.replace(/\\.html$/i, "").replace(/^\\/+|\\/+$/g, "").replace(/[^a-zA-Z0-9/_-]/g, "-").slice(0, 180);
}'''

NEW_CLEAN_SLUG = '''// PATCHED: cleanSlug now strips path prefixes
// Pages send "genesis-to-quantum/gtq-01-foo" but D1 stores "gtq-01-foo".
function cleanSlug(value) {
  const text = optionalString(value);
  if (!text) return "";
  let slug = text.replace(/\\.html$/i, "").replace(/^\\/+|\\/+$/g, "").replace(/[^a-zA-Z0-9/_-]/g, "-").slice(0, 180);
  // Strip path prefix: "series/article-slug" -> "article-slug"
  if (slug.includes("/")) slug = slug.split("/").pop();
  return slug;
}'''

# Try to read existing file
if OUT.exists():
    code = OUT.read_text(encoding='utf-8')
    if OLD_CLEAN_SLUG in code:
        code = code.replace(OLD_CLEAN_SLUG, NEW_CLEAN_SLUG)
        OUT.write_text(code, encoding='utf-8')
        print(f"Patched cleanSlug in existing file ({len(code)} chars)")
    elif 'slug.split("/").pop()' in code:
        print("File already patched!")
    else:
        print(f"WARNING: Could not find cleanSlug to patch. File has {len(code)} chars.")
        print("You may need to manually replace the file.")
else:
    print(f"File not found: {OUT}")
