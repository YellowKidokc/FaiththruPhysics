#!/usr/bin/env python3
"""Remove the legacy embedded reader-mode-bar component from MDA-003
so it does not duplicate the new MTL top bar."""
from pathlib import Path
import re

ROOT = Path("D:/GitHub/faiththruphysics-site")
path = ROOT / "mda/02-method-and-metrics/MDA-003-measuring-moral-health.html"

text = path.read_text(encoding="utf-8")

# Remove style block
pattern = r'<!-- BEGIN:COMPONENT:style:reader-mode-bar -->.*?<!-- END:COMPONENT:style:reader-mode-bar -->\s*'
text = re.sub(pattern, '', text, count=1, flags=re.S)

# Remove HTML block
pattern = r'<!-- BEGIN:COMPONENT:reader-mode:reader-mode-bar -->.*?<!-- END:COMPONENT:reader-mode:reader-mode-bar -->\s*'
text = re.sub(pattern, '', text, count=1, flags=re.S)

# Remove script block
pattern = r'<!-- BEGIN:COMPONENT:script:reader-mode-bar -->.*?<!-- END:COMPONENT:script:reader-mode-bar -->\s*'
text = re.sub(pattern, '', text, count=1, flags=re.S)

path.write_text(text, encoding="utf-8")
print(f"Removed legacy reader-mode bar from {path}")
