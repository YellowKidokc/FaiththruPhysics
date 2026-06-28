import base64, pathlib
# Base64 of the patched worker - generated from the content David pasted
b64 = open(r"D:\GitHub\faiththruphysics-site\workers\audio-pipeline\b64.txt").read().strip()
out = pathlib.Path(r"D:\GitHub\faiththruphysics-site\workers\audio-pipeline\src\index.js")
out.write_bytes(base64.b64decode(b64))
print(f"Wrote {out.stat().st_size} bytes to {out}")
