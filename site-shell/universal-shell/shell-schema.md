# Shell Data Schema — Formal Reference

**Version:** 1.0  
**Format:** JSON (embedded in `<script id="shell-data" type="application/json">`)  
**Consumes:** `shell.js` — all rendering is data-driven from this schema

---

## Root Object

```typescript
interface ShellData {
  page: PageInfo;           // Required. Article metadata
  domains?: Domain[];       // Domain coverage for classification
  verification?: Verification; // All verification/proof metrics
  mtl?: MTLEntry[];         // Math Translation Layer equations
  audio?: AudioTrack[];     // Audio dock source configuration
  audit?: Audit;            // Final Audit three-column content
}
```

---

## page (required)

```typescript
interface PageInfo {
  title: string;            // Article title
  subtitle?: string;        // Article subtitle
  author?: string;          // Author name
  series: string;           // Series code: "MDA" | "GTQ" | "Convergence" | "Logos" | "OPS"
  series_name?: string;     // Human-readable series name
  series_home?: string;     // URL to series index
  slug?: string;            // URL-safe identifier
  date?: string;            // Publication date
  prev?: NavLink;           // Previous article
  next?: NavLink;           // Next article
}

interface NavLink {
  title: string;
  url: string;
}
```

**Example:**
```json
{
  "page": {
    "title": "The Measurement That Collapsed Reality",
    "subtitle": "When observation becomes the force that binds matter to meaning.",
    "author": "David Lowe",
    "series": "GTQ",
    "series_name": "Genesis to Quantum",
    "series_home": "/genesis-to-quantum/",
    "slug": "gtq-01-measurement",
    "date": "June 2026",
    "prev": { "title": "Series Introduction", "url": "/genesis-to-quantum/" },
    "next": { "title": "Free Will", "url": "/genesis-to-quantum/gtq-02.html" }
  }
}
```

---

## domains

```typescript
interface Domain {
  name: string;             // Display name: "Theology", "Physics", etc.
  key: string;              // Machine key: "theology", "physics", etc.
  pct: number;              // Coverage percentage (0-100)
  color: string;            // Hex color for visual indicators
}
```

**Standard palette:**
| Domain | Key | Color |
|--------|-----|-------|
| Theology | `theology` | `#d4af37` |
| Physics | `physics` | `#7cc7ff` |
| Mathematics | `mathematics` | `#ff7d90` |
| Cross-Domain | `cross-domain` | `#3bb39a` |
| Evidence | `evidence` | `#7fc77f` |
| Consciousness | `consciousness` | `#a78bfa` |
| Information Theory | `information` | `#e8a040` |
| Speculative | `speculative` | `#aeb8d6` |

**Example:**
```json
{
  "domains": [
    { "name": "Theology", "key": "theology", "pct": 28, "color": "#d4af37" },
    { "name": "Physics", "key": "physics", "pct": 22, "color": "#7cc7ff" },
    { "name": "Cross-Domain", "key": "cross-domain", "pct": 15, "color": "#3bb39a" },
    { "name": "Evidence", "key": "evidence", "pct": 15, "color": "#7fc77f" }
  ]
}
```

---

## verification

```typescript
interface Verification {
  axioms: AxiomMetrics;
  laws: LawMetrics;
  chi: ChiMetrics;
  fruits: FruitsMetrics;
  isomorphisms: IsomorphismMetrics;
  claims: ClaimMetrics;
  proofs: Proof[];
}

interface AxiomMetrics {
  tested: number;           // Axioms tested in this article
  total?: number;           // Total available (default: 188)
}

interface LawMetrics {
  active: number[];         // Active law numbers [1-10]
}

interface ChiMetrics {
  raw: number;              // Raw chi coherence score
  normalized: number;       // Normalized 0-10
}

interface FruitsMetrics {
  score: number;            // Fruits score 0-9
}

interface IsomorphismMetrics {
  count: number;            // Total cross-domain bridges
  physics_processes: number; // Physics processes detected
  trinity_mappings: number;  // Trinity mappings found
  meq_variables: number;    // Master Equation variables engaged (0-10)
}

interface ClaimMetrics {
  total: number;            // Total claims extracted
  load_bearing: number;     // Load-bearing claims
  kill_conditions: number;  // Falsification conditions
  contradictions: number;   // Contradictions found (0 if none)
}

interface Proof {
  id: string;               // Unique identifier
  title: string;            // Proof title
  status: "verified" | "partial" | "pending";
  summary: string;          // Plain-text summary
  url?: string;             // Link to Proof Explorer
}
```

**Example:**
```json
{
  "verification": {
    "axioms": { "tested": 94, "total": 188 },
    "laws": { "active": [1, 3, 4, 7, 10] },
    "chi": { "raw": 7.42, "normalized": 8.3 },
    "fruits": { "score": 7 },
    "isomorphisms": {
      "count": 12,
      "physics_processes": 5,
      "trinity_mappings": 3,
      "meq_variables": 8
    },
    "claims": {
      "total": 24,
      "load_bearing": 8,
      "kill_conditions": 3,
      "contradictions": 0
    },
    "proofs": [
      {
        "id": "p1",
        "title": "Observer-Dependence Derivation",
        "status": "verified",
        "summary": "The measurement problem is not epistemic...",
        "url": "/proof-explorer/gtq-01/measurement"
      }
    ]
  }
}
```

---

## mtl

```typescript
interface MTLEntry {
  latex?: string;           // LaTeX source (renders via MathJax)
  named?: string;           // Equation with named variables
  plain?: string;           // Plain-English explanation
  feature?: string;         // Structural feature to highlight
}
```

The `feature` field is for surfacing unique structural properties:
- Multiplicative relationships: "if any term goes to zero, the whole collapses"
- Boundary conditions: "this equation only holds when X > 0"
- Conservation laws: "the total is preserved under transformation"
- Asymmetry: "the spiritual version adds exactly one degree of freedom"

**Example:**
```json
{
  "mtl": [
    {
      "latex": "\\frac{d\\chi}{dt} = G_{\\text{ext}} \\cdot \\eta(K) - \\lambda S(\\chi)",
      "named": "Rate of coherence = External grace times knowledge receptivity minus entropy times coherence",
      "plain": "Coherence changes over time based on external grace times how much knowledge can receive it, minus entropy times a constant.",
      "feature": "Multiplicative: if either G_ext or eta(K) goes to zero, the growth term vanishes entirely."
    }
  ]
}
```

---

## audio

```typescript
interface AudioTrack {
  src: "read" | "debate" | "deep" | "critique";  // Source key
  label: string;        // Display label
  url?: string;         // MP3 URL. Omit = "coming soon"
}
```

**Example:**
```json
{
  "audio": [
    { "src": "read", "label": "Read Aloud", "url": "https://r2.faiththruphysics.com/GTQ-01/read-aloud.mp3" },
    { "src": "debate", "label": "Debate", "url": "https://r2.faiththruphysics.com/GTQ-01/debate.mp3" },
    { "src": "deep", "label": "Deep Dive", "url": "https://r2.faiththruphysics.com/GTQ-01/deep-dive.mp3" },
    { "src": "critique", "label": "Critique" }
  ]
}
```

**Color coding by source:**
| Source | Color | Purpose |
|--------|-------|---------|
| `read` | Gold (#d4af37) | Read-aloud narration |
| `debate` | Purple (#a855f7) | Debate format |
| `deep` | Blue (#4a9eff) | Deep dive technical |
| `critique` | Teal (#2dd4bf) | Critical analysis |

---

## audit

```typescript
interface Audit {
  right: string[];       // What we got right
  overstated: string[];  // What we overstated
  wrong: string[];       // What we got wrong
}
```

**Example:**
```json
{
  "audit": {
    "right": [
      "The measurement formalism is standard quantum mechanics.",
      "The Master Equation derivation holds at 6.35σ.",
      "The isomorphism between Yukawa potential and agapē is formally complete."
    ],
    "overstated": [
      "The consciousness bridge is suggestive but not yet rigorously closed.",
      "We used 'proof' where 'high-confidence inference' would be more honest."
    ],
    "wrong": [
      "The initial entropy calculation was off by a factor of 2 — corrected in v4.",
      "We attributed a source incorrectly; the citation has been fixed."
    ]
  }
}
```

---

## Complete Minimal Example

The smallest valid shell-data block:

```json
{
  "page": {
    "title": "Article Title",
    "series": "GTQ"
  }
}
```

This will render the full shell with placeholder/empty values. All other fields are optional but recommended.

## Complete Full Example

See `shell.html` — the `<script id="shell-data">` block at the top of the body contains a fully populated example for the GTQ-01 article.

---

*POF 2828 | faiththruphysics.com*
