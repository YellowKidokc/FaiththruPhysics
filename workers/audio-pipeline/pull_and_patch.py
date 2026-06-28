"""Pull the deployed worker from Cloudflare, patch cleanSlug, save locally."""
import subprocess, re
from pathlib import Path

OUT = Path(r"D:\GitHub\faiththruphysics-site\workers\audio-pipeline\src\index.js")

# Pull current deployed code via wrangler
print("Pulling deployed worker code from Cloudflare...")
r = subprocess.run(
    'npx wrangler versions view --name faith-audio-pipeline -x',
    shell=True, capture_output=True, encoding='utf-8', errors='replace'
)

# Alternative: just fetch from the worker's source via API
# The code was already deployed, so let's pull it with wrangler download
r2 = subprocess.run(
    'npx wrangler versions download --name faith-audio-pipeline --outdir D:\\GitHub\\faiththruphysics-site\\workers\\audio-pipeline\\src\\_pull',
    shell=True, capture_output=True, encoding='utf-8', errors='replace'
)
print(r2.stdout[-500:] if r2.stdout else "no stdout")
print(r2.stderr[-500:] if r2.stderr else "no stderr")
