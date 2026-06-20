#!/usr/bin/env python3
"""
MTL Overlay Uploader — dead-simple desktop tool for reviewed equation translations.

Double-click this file to open it (Windows will run it with pythonw.exe, no console).

What it does:
  1. You pick an MDA article HTML file.
  2. It finds every .equation-block and extracts the math inside.
  3. You type an everyday meaning and a readable word-equation for each.
  4. It writes the records to shared/data/mtl-overlay-translations.json.

The MTL overlay (mtl-overlay.js) then shows your reviewed translations instead of
its heuristic guesses. Nothing else needs to change in the HTML.
"""
import json
import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
SITE_ROOT = Path(__file__).resolve().parent.parent
OVERLAY_JSON = SITE_ROOT / "shared" / "data" / "mtl-overlay-translations.json"

# ═══════════════════════════════════════════════════════════════════════════════
# NORMALIZATION — must match src/browser/overlay.ts normalizeForLookup()
# ═══════════════════════════════════════════════════════════════════════════════
_REPLACEMENTS = [
    (re.compile(r"\\chi|\u03c7|𝜒", re.I), "chi"),
    (re.compile(r"\\iiint|\u222d|\\iint|\u222b|\\int", re.I), "int"),
    (re.compile(r"\\cdot|⋅|·|\*"), ""),
    (re.compile(r"\\,|\\left|\\right|\\text|\\mathrm"), ""),
    (re.compile(r"\\geq|≥"), "ge"),
    (re.compile(r"\\leq|≤"), "le"),
    (re.compile(r"\\neq|≠"), "ne"),
    (re.compile(r"\\propto|∝"), "propto"),
    (re.compile(r"\\to|→"), "to"),
    (re.compile(r"\\Delta|Δ"), "delta"),
    (re.compile(r"\\Phi|Φ"), "phi"),
    (re.compile(r"\\Psi|Ψ"), "psi"),
    (re.compile(r"\\sigma|σ"), "sigma"),
    (re.compile(r"\\gamma|γ"), "gamma"),
    (re.compile(r"\\mu|μ"), "mu"),
    (re.compile(r"\\nu|ν"), "nu"),
    (re.compile(r"\\rho|ρ"), "rho"),
    (re.compile(r"\\Lambda|Λ"), "lambda"),
    (re.compile(r"\\Theta|Θ"), "theta"),
    (re.compile(r"\\hbar|ℏ"), "hbar"),
    (re.compile(r"\\pi|π"), "pi"),
]


def normalize_for_lookup(source: str) -> str:
    normalized = source
    for pattern, replacement in _REPLACEMENTS:
        normalized = pattern.sub(replacement, normalized)
    normalized = re.sub(r"\\[A-Za-z]+", "", normalized)
    normalized = re.sub(r"[^A-Za-z0-9]+", "", normalized)
    return normalized.lower()


# ═══════════════════════════════════════════════════════════════════════════════
# EQUATION EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

def find_math_inside(text: str) -> str | None:
    """Return the first display or inline math string found inside text."""
    for pat in (r"\\\[(.*?)\\\]", r"\$\$(.*?)\$\$", r"\\\((.*?)\\\)", r"\$(.*?)\$"):
        m = re.search(pat, text, re.S)
        if m:
            return m.group(1).strip()
    return None


def extract_equations(html: str, article_id: str):
    """Return list of {id, latex, key} dicts from .equation-block divs."""
    found = []
    seen_keys = set()

    for idx, m in enumerate(re.finditer(r'<div class="equation-block"[^>]*>(.*?)</div>', html, re.S), start=1):
        latex = find_math_inside(m.group(1))
        if latex and len(latex) > 1:
            key = normalize_for_lookup(latex)
            # Avoid duplicates from identical equations
            if key in seen_keys:
                continue
            seen_keys.add(key)
            found.append({
                "id": f"{article_id}-EQ-{idx:03d}",
                "latex": latex,
                "key": key,
            })

    return found


# ═══════════════════════════════════════════════════════════════════════════════
# CATALOG IO
# ═══════════════════════════════════════════════════════════════════════════════

def load_catalog() -> list:
    if OVERLAY_JSON.exists():
        data = json.loads(OVERLAY_JSON.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    return []


def save_catalog(catalog: list):
    OVERLAY_JSON.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")


def catalog_by_key(catalog: list) -> dict:
    return {entry["key"]: entry for entry in catalog if "key" in entry}


# ═══════════════════════════════════════════════════════════════════════════════
# TKINTER UI
# ═══════════════════════════════════════════════════════════════════════════════

class MtlUploaderApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("MTL Overlay Uploader")
        self.root.geometry("950x750")
        self.root.configure(bg="#0f0f0f")

        self.file_path: Path | None = None
        self.equations: list = []
        self.entries: dict = {}

        self._build_styles()
        self._build_header()
        self._build_file_row()
        self._build_equation_list()
        self._build_footer()

    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#0f0f0f")
        style.configure("TLabel", background="#0f0f0f", foreground="#e5e3df", font=("Inter", 10))
        style.configure("TButton", font=("Inter", 10, "bold"), padding=6)

    def _build_header(self):
        tk.Label(
            self.root,
            text="MTL Overlay — Article Uploader",
            bg="#0f0f0f",
            fg="#f59e0b",
            font=("JetBrains Mono", 16, "bold"),
        ).pack(pady=(16, 6))

        tk.Label(
            self.root,
            text="Pick an MDA article. Edit Meaning and Visual for each equation, then save.",
            bg="#0f0f0f",
            fg="#888",
            font=("Inter", 10),
        ).pack()

        tk.Label(
            self.root,
            text="The overlay will use these reviewed translations instead of its automatic guess.",
            bg="#0f0f0f",
            fg="#666",
            font=("Inter", 9),
        ).pack(pady=(0, 8))

    def _build_file_row(self):
        row = tk.Frame(self.root, bg="#0f0f0f")
        row.pack(fill=tk.X, padx=20, pady=12)

        self.file_label = tk.Label(
            row,
            text="No file selected",
            bg="#1a1a1a",
            fg="#666",
            font=("JetBrains Mono", 9),
            anchor="w",
            padx=10,
            pady=6,
        )
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(
            row,
            text="Choose HTML file",
            command=self._choose_file,
            bg="#f59e0b",
            fg="#0f0f0f",
            font=("Inter", 10, "bold"),
            borderwidth=0,
            padx=12,
            pady=6,
            cursor="hand2",
        ).pack(side=tk.RIGHT, padx=(10, 0))

    def _build_equation_list(self):
        self.canvas = tk.Canvas(self.root, bg="#0f0f0f", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#0f0f0f")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", width=910)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=10)

    def _build_footer(self):
        footer = tk.Frame(self.root, bg="#0f0f0f")
        footer.pack(fill=tk.X, padx=20, pady=(0, 16))

        self.status_label = tk.Label(
            footer,
            text="Ready",
            bg="#0f0f0f",
            fg="#666",
            font=("JetBrains Mono", 9),
            anchor="w",
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(
            footer,
            text="Save translations",
            command=self._save,
            bg="#22c55e",
            fg="#0f0f0f",
            font=("Inter", 10, "bold"),
            borderwidth=0,
            padx=16,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.RIGHT)

    def _choose_file(self):
        path = filedialog.askopenfilename(
            title="Select an MDA article HTML file",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            initialdir=SITE_ROOT / "mda",
        )
        if not path:
            return

        self.file_path = Path(path)
        self.file_label.config(text=str(self.file_path), fg="#e5e3df")
        self._load_equations()

    def _load_equations(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.entries = {}

        html = self.file_path.read_text(encoding="utf-8")
        article_id = self.file_path.stem
        self.equations = extract_equations(html, article_id)

        if not self.equations:
            tk.Label(
                self.scroll_frame,
                text="No equations found in this file.\nMake sure equations are inside <div class=\"equation-block\"> with \\[...\\] math.",
                bg="#0f0f0f",
                fg="#666",
                font=("Inter", 11),
                justify="center",
            ).pack(pady=40)
            self.status_label.config(text="No equations found")
            return

        catalog = load_catalog()
        by_key = catalog_by_key(catalog)

        for idx, eq in enumerate(self.equations, start=1):
            existing = by_key.get(eq["key"], {})

            card = tk.Frame(self.scroll_frame, bg="#1a1a1a", padx=14, pady=14)
            card.pack(fill=tk.X, pady=8, padx=4)
            card.configure(highlightbackground="#333", highlightthickness=1)

            header = tk.Frame(card, bg="#1a1a1a")
            header.pack(fill=tk.X)

            tk.Label(
                header,
                text=f"Equation {idx}",
                bg="#1a1a1a",
                fg="#f59e0b",
                font=("JetBrains Mono", 10, "bold"),
                anchor="w",
            ).pack(side=tk.LEFT)

            tk.Label(
                header,
                text=f"key: {eq['key']}",
                bg="#1a1a1a",
                fg="#555",
                font=("JetBrains Mono", 8),
                anchor="e",
            ).pack(side=tk.RIGHT)

            latex_box = scrolledtext.ScrolledText(
                card,
                height=2,
                bg="#0f0f0f",
                fg="#e5e3df",
                font=("JetBrains Mono", 9),
                wrap=tk.WORD,
                state=tk.NORMAL,
                padx=8,
                pady=6,
            )
            latex_box.insert(tk.END, eq["latex"])
            latex_box.config(state=tk.DISABLED)
            latex_box.pack(fill=tk.X, pady=(8, 12))

            self.entries[eq["key"]] = {
                "equation": eq["latex"],
            }

            grid = tk.Frame(card, bg="#1a1a1a")
            grid.pack(fill=tk.X)
            grid.columnconfigure(1, weight=1)

            # Meaning
            tk.Label(
                grid,
                text="Meaning\n(everyday)",
                bg="#1a1a1a",
                fg="#888",
                font=("Inter", 9, "bold"),
                width=12,
                anchor="nw",
                justify="left",
            ).grid(row=0, column=0, sticky="nw", pady=6)

            meaning_txt = tk.Text(
                grid,
                height=3,
                bg="#0f0f0f",
                fg="#e5e3df",
                font=("Inter", 9),
                wrap=tk.WORD,
                borderwidth=1,
                relief=tk.FLAT,
                highlightbackground="#333",
                highlightthickness=1,
                padx=8,
                pady=6,
            )
            meaning_txt.insert(tk.END, existing.get("meaning", "Type the everyday meaning here..."))
            meaning_txt.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=6)
            self.entries[eq["key"]]["meaning"] = meaning_txt

            # Visual / word equation
            tk.Label(
                grid,
                text="Visual /\nword equation",
                bg="#1a1a1a",
                fg="#888",
                font=("Inter", 9, "bold"),
                width=12,
                anchor="nw",
                justify="left",
            ).grid(row=1, column=0, sticky="nw", pady=6)

            visual_txt = tk.Text(
                grid,
                height=3,
                bg="#0f0f0f",
                fg="#e5e3df",
                font=("Inter", 9),
                wrap=tk.WORD,
                borderwidth=1,
                relief=tk.FLAT,
                highlightbackground="#333",
                highlightthickness=1,
                padx=8,
                pady=6,
            )
            visual_txt.insert(tk.END, existing.get("visual", "Type a readable symbol-by-symbol version here..."))
            visual_txt.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=6)
            self.entries[eq["key"]]["visual"] = visual_txt

        self.status_label.config(text=f"Found {len(self.equations)} equation(s)")
        self.canvas.yview_moveto(0)

    def _save(self):
        if not self.file_path or not self.equations:
            messagebox.showwarning("Nothing to save", "Select a file with equations first.")
            return

        catalog = load_catalog()
        by_key = catalog_by_key(catalog)

        updated = 0
        for eq in self.equations:
            key = eq["key"]
            widgets = self.entries[key]

            meaning = widgets["meaning"].get("1.0", tk.END).strip()
            visual = widgets["visual"].get("1.0", tk.END).strip()

            # Skip placeholder text
            if "Type the everyday meaning" in meaning:
                meaning = ""
            if "Type a readable symbol-by-symbol" in visual:
                visual = ""

            record = {
                "key": key,
                "equation": widgets["equation"],
                "meaning": meaning,
                "visual": visual,
            }

            if key in by_key:
                by_key[key].update(record)
            else:
                catalog.append(record)
                by_key[key] = record

            updated += 1

        save_catalog(catalog)

        self.status_label.config(text=f"Saved {updated} translation(s)")
        messagebox.showinfo(
            "Saved",
            f"Saved {updated} reviewed translation(s) to:\n\n"
            f"{OVERLAY_JSON}\n\n"
            "The overlay will now use these instead of its automatic guesses.",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = MtlUploaderApp(root)
    root.mainloop()
