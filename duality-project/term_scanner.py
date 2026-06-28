#!/usr/bin/env python3
"""
Duality Project - Term Coherence Scanner
Run with:  python term_scanner.py
Requires:  Python 3.8+, tkinter (built-in)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, re, json, threading, html as htmllib

# ─────────────────────────────────────────────────────────────────────────────
#  TERM REGISTRY  (risk: 4=critical  3=high  2=medium  1=low)
# ─────────────────────────────────────────────────────────────────────────────
TERMS = [
    # CLAIM STRENGTH
    {"term":"science proves",       "cat":"Claim Strength","risk":4,"q":"Directly claims scientific proof. What specific science? What specific evidence? Add proof-type annotation."},
    {"term":"physics proves",       "cat":"Claim Strength","risk":4,"q":"Claims physics as proof authority. Is this literal empirical physics or a cross-domain bridge? Label clearly."},
    {"term":"mathematically proves","cat":"Claim Strength","risk":4,"q":"Mathematical proof requires formal axioms and derivation. Is this formal proof or informal analogy?"},
    {"term":"not an analogy",       "cat":"Claim Strength","risk":4,"q":"Directly denies analogy status. What ontological claim replaces it? What argument justifies this?"},
    {"term":"not analogy",          "cat":"Claim Strength","risk":4,"q":"Denying analogy raises the claim to literal or ontological. What standard justifies this?"},
    {"term":"not metaphor",         "cat":"Claim Strength","risk":4,"q":"Denying metaphor raises the claim to literal or ontological. What evidence or argument justifies this?"},
    {"term":"ontological identity", "cat":"Claim Strength","risk":4,"q":"Strongest possible bridge claim - stronger than analogy, metaphor, or isomorphism. What argument supports this?"},
    {"term":"irrefutable",          "cat":"Claim Strength","risk":4,"q":"Claims no possible refutation. What standard of refutation is being rejected? Who is the intended skeptic?"},
    {"term":"undeniable",           "cat":"Claim Strength","risk":4,"q":"Absolute epistemic claim. What would falsify this? What audience is this addressing?"},
    {"term":"identical",            "cat":"Claim Strength","risk":4,"q":"Strongest equivalence claim. Numerically identical or qualitatively? Formal identity or analogy? Specify."},
    {"term":"proves",               "cat":"Claim Strength","risk":4,"q":"What type of proof? Logical deduction? Empirical evidence? Narrative demonstration? Add proof-type annotation."},
    {"term":"proof",                "cat":"Claim Strength","risk":4,"q":"Formal math proof? Empirical evidence? Argument? Theological demonstration? Specify type and standard."},
    {"term":"proven",               "cat":"Claim Strength","risk":4,"q":"Past-tense proof claim. What was proved, by what method, to what standard?"},
    {"term":"demonstrates",         "cat":"Claim Strength","risk":3,"q":"Softer than 'proves' but still claims evidential weight. What is shown and by what evidence type?"},
    {"term":"establishes",          "cat":"Claim Strength","risk":3,"q":"Claims settled fact. Established by argument? Narrative? Theology? Empiricism? Specify."},
    {"term":"confirms",             "cat":"Claim Strength","risk":3,"q":"Implies pre-existing expectation now validated. What confirms what, by what method?"},
    {"term":"verified",             "cat":"Claim Strength","risk":3,"q":"Verification implies testable criteria. Was this verified empirically, logically, or narratively?"},
    {"term":"inevitable",           "cat":"Claim Strength","risk":3,"q":"Removes contingency. Logical necessity? Theological providence? Narrative framing? State the modal basis."},
    {"term":"impossible",           "cat":"Claim Strength","risk":3,"q":"Absolute modal claim. Logical impossibility? Physical? Theological? State the standard."},
    {"term":"shows",                "cat":"Claim Strength","risk":2,"q":"'Shows' still carries claim weight. Does it demonstrate by evidence, suggest, or illustrate? Be explicit."},
    {"term":"reveals",              "cat":"Claim Strength","risk":2,"q":"Theological revelation? Evidence-based disclosure? Narrative uncovering? Specify the mode."},
    {"term":"implies",              "cat":"Claim Strength","risk":2,"q":"Logical implication (formal) or conversational implication (informal)? Does the claim hold under both readings?"},
    {"term":"must",                 "cat":"Claim Strength","risk":2,"q":"Modal necessity. Logical must? Physical must? Theological must? Specify the modality."},
    {"term":"cannot",               "cat":"Claim Strength","risk":2,"q":"Modal impossibility. Logical? Physical constraint? Theological claim? State the basis."},
    {"term":"necessary",            "cat":"Claim Strength","risk":2,"q":"Logically necessary (formal) or just important/required in context? State the sense."},
    {"term":"certain",              "cat":"Claim Strength","risk":2,"q":"Epistemic certainty. Certain by what standard? What would challenge this certainty?"},
    # CORE FRAMEWORK
    {"term":"coherence",     "cat":"Core Framework","risk":3,"q":"Physical coherence (quantum/optics)? Logical coherence? Moral coherence? Theological integration? Narrative device? Scope required."},
    {"term":"decoherence",   "cat":"Core Framework","risk":3,"q":"Quantum decoherence (physics)? Moral fragmentation? System disorder? DP framework term? State the domain."},
    {"term":"discoherence",  "cat":"Core Framework","risk":2,"q":"DP-coined term. How does it differ from standard 'decoherence'? Is it defined on this page?"},
    {"term":"entropy",       "cat":"Core Framework","risk":3,"q":"Thermodynamic entropy (Clausius/Boltzmann)? Information entropy (Shannon)? Moral decay metaphor? Narrative disorder? State the domain."},
    {"term":"negentropy",    "cat":"Core Framework","risk":3,"q":"Schrödinger sense (physics)? Information sense? Moral flourishing metaphor? Narrative restoration? Scope required."},
    {"term":"signal",        "cat":"Core Framework","risk":2,"q":"Information-theoretic signal? Electromagnetic signal? Metaphorical signal? Theological communication?"},
    {"term":"noise",         "cat":"Core Framework","risk":2,"q":"Information-theoretic noise? Moral confusion? Narrative interference? Metaphor for opposition to Truth?"},
    {"term":"truth",         "cat":"Core Framework","risk":2,"q":"Propositional truth? Theological Truth (Logos/John 14:6)? Scientific truth? Narrative truth? Moral alignment?"},
    {"term":"alignment",     "cat":"Core Framework","risk":2,"q":"Moral alignment? Theological alignment with God? AI alignment metaphor? System coherence property?"},
    {"term":"misalignment",  "cat":"Core Framework","risk":2,"q":"Same domain question as alignment. State whether moral, theological, technical, or narrative."},
    {"term":"collapse",      "cat":"Core Framework","risk":3,"q":"Quantum wavefunction collapse (physics)? Narrative collapse? Moral collapse? System failure? Scope required."},
    {"term":"drift",         "cat":"Core Framework","risk":1,"q":"Physical drift? Moral drift? Theological apostasy metaphor? Narrative direction change?"},
    {"term":"decay",         "cat":"Core Framework","risk":2,"q":"Physical decay (radioactive, thermodynamic)? Moral decay? Narrative deterioration? State the domain."},
    {"term":"restoration",   "cat":"Core Framework","risk":1,"q":"Theological restoration? Narrative repair? Historical restoration? System reset? State the domain."},
    {"term":"reconciliation","cat":"Core Framework","risk":1,"q":"Theological reconciliation (2 Cor 5:18)? Social/relational reconciliation? System realignment?"},
    {"term":"completion",    "cat":"Core Framework","risk":1,"q":"Eschatological completion? Narrative completion? Formal completion? System fullness?"},
    {"term":"terminal",      "cat":"Core Framework","risk":2,"q":"DP-coined 'terminal justice/decoherence'? Medical terminal? Narrative endpoint? Is the coined sense defined here?"},
    {"term":"order",         "cat":"Core Framework","risk":1,"q":"Physical order? Moral order? Social order? Divine order? Narrative structure? State the domain."},
    {"term":"disorder",      "cat":"Core Framework","risk":1,"q":"Physical, moral, social, psychological, or narrative disorder? State the domain."},
    # THEOLOGICAL
    {"term":"God",           "cat":"Theological","risk":3,"q":"Theological personal God (YHWH)? System variable (DP engine)? Narrative character? Philosophical concept? State the frame."},
    {"term":"Christ",        "cat":"Theological","risk":3,"q":"Historical person? Theological title (Messiah)? Narrative agent (Template)? Formal analogy? State the frame."},
    {"term":"Jesus",         "cat":"Theological","risk":3,"q":"Historical person? Theological subject? Narrative agent? Are claims here historical or theological? Be explicit."},
    {"term":"Logos",         "cat":"Theological","risk":3,"q":"Johannine theological Logos (John 1)? Greek philosophical logos? DP formal structure metaphor? State the frame."},
    {"term":"Holy Spirit",   "cat":"Theological","risk":3,"q":"Literal Trinitarian theology? Narrative metaphor? DP simulation/network analogy (DP-10)? State the frame."},
    {"term":"Trinity",       "cat":"Theological","risk":3,"q":"Standard Trinitarian theology? Formal analogy? Architectural model? Is the scope labeled?"},
    {"term":"Atonement",     "cat":"Theological","risk":3,"q":"Standard penal substitution? DP Law-5 coherence-release model? Narrative event? Label the model clearly."},
    {"term":"Resurrection",  "cat":"Theological","risk":3,"q":"Literal historical event claim? Theological doctrine? Narrative device? Formal analogy to restoration pattern?"},
    {"term":"sin",           "cat":"Theological","risk":2,"q":"Theological sin (hamartia)? Moral failure? System error? Narrative opposition to coherence? State the frame."},
    {"term":"grace",         "cat":"Theological","risk":2,"q":"Theological grace (unmerited divine favor)? Narrative gift? System property? State the frame."},
    {"term":"salvation",     "cat":"Theological","risk":2,"q":"Standard theology? Formal coherence restoration? Narrative rescue? Metaphysical claim? Label the scope."},
    {"term":"judgment",      "cat":"Theological","risk":2,"q":"Divine eschatological judgment? Moral evaluation? Legal verdict? Narrative climax? State the type."},
    {"term":"covenant",      "cat":"Theological","risk":2,"q":"Biblical covenant theology? DP formal/narrative contract analog? State the frame."},
    {"term":"second death",  "cat":"Theological","risk":4,"q":"DP-21 frames 'second death' as absolute self-enclosure. Is this labeled as theological/narrative model vs empirical claim?"},
    {"term":"hell",          "cat":"Theological","risk":3,"q":"Traditional theology? DP 'self-enclosure' model? Narrative location? Formal terminal state? Label the frame clearly."},
    {"term":"Satan",         "cat":"Theological","risk":2,"q":"Theological being? Narrative character? System variable (Omega-Null/Chrome Agent)? Archetype? State the frame."},
    {"term":"wrath",         "cat":"Theological","risk":3,"q":"Divine wrath (theology)? Narrative force of consequence? System enforcement? Emotional reaction? State the frame."},
    {"term":"incarnation",   "cat":"Theological","risk":2,"q":"Standard Christological doctrine? DP 'Incarnation Protocol' narrative device? Cross-domain model? Label the layer."},
    {"term":"apostasy",      "cat":"Theological","risk":2,"q":"Standard theological apostasy? DP 'Apostasy Bug' narrative frame (DP-16)? Social description? State the layer."},
    # PHYSICS / SCIENCE
    {"term":"quantum",       "cat":"Physics/Science","risk":3,"q":"Literal quantum mechanics? Metaphor? Does this imply scientific validation for a non-physics claim? Scope required."},
    {"term":"entanglement",  "cat":"Physics/Science","risk":3,"q":"Specific quantum phenomenon (physics)? Relational metaphor? Does it imply nonlocal divine connection without physics basis?"},
    {"term":"observer",      "cat":"Physics/Science","risk":3,"q":"Quantum mechanical observer (measurement problem)? Narrative agent? Theological watcher? State the frame."},
    {"term":"superposition", "cat":"Physics/Science","risk":3,"q":"Quantum superposition (specific physics concept)? Metaphor for coexisting states? Scope required."},
    {"term":"wavefunction",  "cat":"Physics/Science","risk":4,"q":"Precise physics object (ψ). Is this literal quantum mechanics or metaphor? Label clearly."},
    {"term":"nonlocal",      "cat":"Physics/Science","risk":4,"q":"Precise quantum mechanics term. Using it outside physics transfers quantum authority. What is the actual claim?"},
    {"term":"resonance",     "cat":"Physics/Science","risk":3,"q":"Physical resonance (specific Hz relationship)? Spiritual/emotional resonance metaphor? Scope prevents authority transfer."},
    {"term":"frequency",     "cat":"Physics/Science","risk":3,"q":"Literal wave frequency (Hz)? Spiritual frequency metaphor? Scope required."},
    {"term":"field",         "cat":"Physics/Science","risk":3,"q":"Physics field (EM, gravitational, quantum)? Theological concept? Narrative metaphor? State the domain."},
    {"term":"dimension",     "cat":"Physics/Science","risk":3,"q":"Mathematical dimension? Physical spacetime dimension? Metaphor for scope/depth? If higher-D claim, require justification."},
    {"term":"singularity",   "cat":"Physics/Science","risk":3,"q":"Black hole singularity (physics)? Mathematical singularity? Theological/narrative boundary point? State the domain."},
    {"term":"energy",        "cat":"Physics/Science","risk":3,"q":"Thermodynamic/kinetic/electromagnetic energy (physics)? Vitality/capacity metaphor? The word carries physics authority."},
    {"term":"symmetry",      "cat":"Physics/Science","risk":3,"q":"Mathematical symmetry? Noether's theorem symmetry (physics)? Aesthetic symmetry? Theological balance?"},
    {"term":"relativity",    "cat":"Physics/Science","risk":3,"q":"Einstein's relativity (physics)? General relativism/context-dependence? Do not conflate these."},
    {"term":"spacetime",     "cat":"Physics/Science","risk":3,"q":"Einsteinian spacetime (physics)? Metaphorical container for experience? Label clearly."},
    {"term":"measurement",   "cat":"Physics/Science","risk":3,"q":"Quantum measurement (wavefunction collapse)? General evaluation/assessment? Does it imply quantum authority?"},
    {"term":"thermodynamics","cat":"Physics/Science","risk":3,"q":"Literal physics? Invoked to lend authority to a non-physics claim? Label the scope."},
    {"term":"photon",        "cat":"Physics/Science","risk":2,"q":"Literal physics photon? Metaphor for divine light? Scope required."},
    {"term":"gravity",       "cat":"Physics/Science","risk":2,"q":"Physical gravity? Metaphor for attraction/weight/importance? State the domain."},
    {"term":"interference",  "cat":"Physics/Science","risk":2,"q":"Wave interference (physics)? Relational/narrative interference? Constructive/destructive as metaphor?"},
    {"term":"amplitude",     "cat":"Physics/Science","risk":2,"q":"Wave amplitude (physics)? Magnitude/scope (general)? State the domain."},
    {"term":"phase",         "cat":"Physics/Science","risk":2,"q":"Wave phase (physics)? Phase transition? Narrative stage/period? State the domain."},
    {"term":"uncertainty",   "cat":"Physics/Science","risk":2,"q":"Heisenberg uncertainty principle (physics)? General epistemic uncertainty? Do not conflate these."},
    # MATH / FORMAL
    {"term":"theorem",       "cat":"Math/Formal","risk":4,"q":"Formal mathematical theorem (requires axioms + derivation)? Narrative/conceptual claim labeled as theorem?"},
    {"term":"axiom",         "cat":"Math/Formal","risk":3,"q":"Formal mathematical axiom (unprovable primitive)? Informal assumed starting premise? Label the sense."},
    {"term":"equation",      "cat":"Math/Formal","risk":3,"q":"Actual mathematical equation with defined variables? Informal model? Metaphor? Specify."},
    {"term":"invariant",     "cat":"Math/Formal","risk":3,"q":"Formally defined mathematical invariant? Qualitative claim about what doesn't change? Specify."},
    {"term":"model",         "cat":"Math/Formal","risk":3,"q":"Formal mathematical model? Conceptual framework? Narrative device? Metaphor? Scope required."},
    {"term":"isomorphism",   "cat":"Math/Formal","risk":4,"q":"Formal mathematical isomorphism (requires bijective structure-preserving map)? Or structural analogy? Formal use needs proof."},
    {"term":"isomorphic",    "cat":"Math/Formal","risk":4,"q":"Same question as isomorphism. If informal, replace with 'structurally analogous to' or label explicitly."},
    # BRIDGE TERMS
    {"term":"same law",      "cat":"Bridge Terms","risk":4,"q":"Claims the same law operates across domains. What law? What formal justification? Structural analogy or ontological claim?"},
    {"term":"same equation", "cat":"Bridge Terms","risk":4,"q":"Formal mathematical equivalence across domains. Is this literal (with derivation) or analogical? Label clearly."},
    {"term":"isomorphic to", "cat":"Bridge Terms","risk":4,"q":"Mathematical isomorphism is precise. Formally proved isomorphism or structural analogy? The difference matters publicly."},
    {"term":"maps to",       "cat":"Bridge Terms","risk":2,"q":"What kind of mapping? Structural analogy, formal function mapping, metaphor, or ontological claim? Specify."},
    {"term":"corresponds to","cat":"Bridge Terms","risk":2,"q":"Correspondence: analogy, structural similarity, formal mapping? Which is meant?"},
    {"term":"parallels",     "cat":"Bridge Terms","risk":2,"q":"Narrative parallel, formal analogy, or ontological claim? Specify the type of parallel."},
    {"term":"mirrors",       "cat":"Bridge Terms","risk":2,"q":"Metaphorical mirror, structural analogy, formal reflection, or typological fulfillment?"},
    {"term":"analogy",       "cat":"Bridge Terms","risk":2,"q":"Is the analogy clearly labeled as analogy, or implicitly elevated to something stronger elsewhere in the text?"},
    {"term":"archetype",     "cat":"Bridge Terms","risk":2,"q":"Jungian psychological? Platonic formal? Theological typology? Narrative template? State the frame."},
    {"term":"metaphor",      "cat":"Bridge Terms","risk":1,"q":"Is the metaphor clearly labeled as metaphor, or implicitly elevated to something stronger?"},
    # SIMULATION / CODE
    {"term":"simulation",    "cat":"Simulation/Code","risk":2,"q":"Literal computation? DP narrative device? Theological metaphor? Formal systems model? State the layer."},
    {"term":"algorithm",     "cat":"Simulation/Code","risk":2,"q":"Literal computation? Narrative device? Metaphor for process/law? State the layer."},
    {"term":"protocol",      "cat":"Simulation/Code","risk":2,"q":"Literal network protocol? DP story-path narrative device? Theological procedure? State the layer."},
    {"term":"recursive",     "cat":"Simulation/Code","risk":2,"q":"Formal recursion (computation)? Self-referential in a narrative/informal sense? State the layer."},
    {"term":"patch",         "cat":"Simulation/Code","risk":1,"q":"Literal software patch? DP narrative/theological device (Atonement-as-patch)? State the layer."},
    {"term":"download",      "cat":"Simulation/Code","risk":1,"q":"Literal data download? DP theological metaphor (Incarnation, Pentecost, DP-10)? State the layer."},
    # GOOD / EVIL
    {"term":"evil",          "cat":"Good/Evil","risk":2,"q":"Moral theology? Narrative opposition? Social diagnosis? Metaphysical claim? Psychological description? State the domain."},
    {"term":"good",          "cat":"Good/Evil","risk":1,"q":"Moral theology? Narrative characterization? Social evaluation? Formal coherence property? State the domain."},
    {"term":"darkness",      "cat":"Good/Evil","risk":1,"q":"Narrative symbol? Theological metaphor? Moral category? Physical darkness? State the domain."},
    {"term":"void",          "cat":"Good/Evil","risk":2,"q":"DP concept of absolute absence (Omega-Null)? Narrative emptiness? Formal zero-state? Mathematical void?"},
    {"term":"parasite",      "cat":"Good/Evil","risk":3,"q":"Biological metaphor? Narrative characterization? DP formal claim about evil's ontological nature? Social diagnosis?"},
    {"term":"corruption",    "cat":"Good/Evil","risk":2,"q":"Moral/theological corruption? Narrative decay? Social/political corruption? Formal system degradation?"},
    # JUSTICE / DEBT
    {"term":"debt",          "cat":"Justice/Debt","risk":3,"q":"Moral debt (Law 5 framework)? Financial debt metaphor? Relational debt? Theological guilt/sin? Name the type."},
    {"term":"scapegoat",     "cat":"Justice/Debt","risk":3,"q":"Levitical theology? Girardian mimetic theory? Social mechanism? Narrative archetype? Domain matters for the claim."},
    {"term":"substitute",    "cat":"Justice/Debt","risk":3,"q":"Penal substitutionary atonement (theology)? Narrative stand-in? Formal replacement agent in a system?"},
    {"term":"mediator",      "cat":"Justice/Debt","risk":2,"q":"Legal/theological mediator (1 Tim 2:5)? Narrative bridge agent? Formal system intermediary?"},
    {"term":"forgiveness",   "cat":"Justice/Debt","risk":2,"q":"Theological forgiveness? Relational forgiveness? System-level cost absorption (Law 5)? Narrative healing?"},
    {"term":"restitution",   "cat":"Justice/Debt","risk":3,"q":"Formal justice? Theological restoration? Narrative repair? DP Law-5 cost-payment? State the frame."},
    {"term":"sacrifice",     "cat":"Justice/Debt","risk":2,"q":"Levitical sacrifice (theology)? Narrative self-giving? Social cost? Formal system input? State the frame."},
    {"term":"atonement",     "cat":"Justice/Debt","risk":3,"q":"Standard penal substitution? DP Law-5 coherence-release model? Narrative event? Formal system claim? Label the model."},
    # ABSOLUTE / TOTALIZING
    {"term":"always",        "cat":"Absolute","risk":2,"q":"Logical universal (true in all cases)? Narrative pattern? Theological claim? Are there known exceptions?"},
    {"term":"never",         "cat":"Absolute","risk":2,"q":"Logical universal? Narrative pattern? Theological absolute? Are there known exceptions?"},
    {"term":"infinite",      "cat":"Absolute","risk":3,"q":"Mathematical infinity (∞)? Theological infinity of God? Narrative hyperbole? State the domain."},
    {"term":"absolute",      "cat":"Absolute","risk":3,"q":"Formal mathematical absolute? Theological absolute (God)? Rhetorical intensifier? State the domain."},
    {"term":"perfect",       "cat":"Absolute","risk":2,"q":"Theological perfection (divine attribute)? Narrative ideal? Formal completeness? Rhetorical claim?"},
    {"term":"eternal",       "cat":"Absolute","risk":2,"q":"Theological eternity (outside time)? Philosophical timelessness? Narrative permanence? State the domain."},
    {"term":"universal",     "cat":"Absolute","risk":2,"q":"Formally universal (all cases proved)? Culturally widespread? Theologically cosmic? Rhetorical?"},
    {"term":"zero",          "cat":"Absolute","risk":2,"q":"Mathematical zero? 'Zero entropy' (formal/narrative)? DP Omega-Null metaphor? State the domain."},
    {"term":"all",           "cat":"Absolute","risk":1,"q":"Logical all-quantifier (proved for all cases)? Narrative all? Rhetorical all? Is the scope actually universal?"},
    {"term":"every",         "cat":"Absolute","risk":1,"q":"Same question as 'all.' Is 'every' a proved universal or rhetorical emphasis?"},
    {"term":"only",          "cat":"Absolute","risk":1,"q":"'Only' claims exclusivity. Is this exclusive by logic, theology, narrative, or rhetorical emphasis?"},
    # PSYCHOLOGICAL
    {"term":"neuroplasticity","cat":"Psychological","risk":3,"q":"Literal neuroscience claim? Metaphor for habit/sanctification (DP-11)? Scope required to avoid scientific overclaim."},
    {"term":"consciousness", "cat":"Psychological","risk":3,"q":"Neuroscience consciousness? Phenomenological? Theological soul-concept? Narrative awareness? State the frame."},
    {"term":"trauma",        "cat":"Psychological","risk":2,"q":"Clinical psychological trauma? Narrative wound? Theological wound? Social harm? State the domain."},
    {"term":"addiction",     "cat":"Psychological","risk":2,"q":"Clinical addiction (psychology)? Narrative compulsion? Theological bondage to sin? State the domain."},
    {"term":"identity",      "cat":"Psychological","risk":2,"q":"Psychological identity (self-concept)? Mathematical identity? Ontological identity? Theological identity in Christ?"},
]

SORTED_TERMS = sorted(TERMS, key=lambda t: len(t["term"]), reverse=True)
RISK_LABELS  = {4:"Critical", 3:"High", 2:"Medium", 1:"Low"}
RISK_COLORS  = {4:"#ef4444",  3:"#f97316", 2:"#eab308", 1:"#22c55e"}

# ─────────────────────────────────────────────────────────────────────────────
#  HTML EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────

BLOCK_TAGS = r"p|h[1-6]|li|blockquote|td|th|figcaption|dt|dd"
BLOCK_RE   = re.compile(rf"<({BLOCK_TAGS})(\s[^>]*)?>", re.IGNORECASE)
SKIP_RE    = re.compile(r"<(script|style|nav|footer|noscript|head)[\s\S]*?</\1>", re.IGNORECASE)
TAG_RE     = re.compile(r"<[^>]+>")

def extract_elements(html_text):
    """Return list of {tag, text, inner_html, outer_html} for content elements."""
    # Blank out non-content zones (preserving positions in working copy)
    working = SKIP_RE.sub(lambda m: " " * len(m.group()), html_text)
    elements = []
    for m in BLOCK_RE.finditer(working):
        tag = m.group(1).lower()
        cs  = m.end()
        close_re = re.compile(rf"</{re.escape(tag)}>", re.IGNORECASE)
        cm = close_re.search(working, cs)
        if not cm:
            continue
        inner = html_text[cs : cm.start()]
        outer = html_text[m.start() : cm.end()]
        text  = htmllib.unescape(TAG_RE.sub(" ", inner))
        text  = re.sub(r"\s+", " ", text).strip()
        if len(text) >= 8:
            elements.append({"tag": tag, "text": text, "inner_html": inner, "outer_html": outer})
    return elements

# ─────────────────────────────────────────────────────────────────────────────
#  SCANNER
# ─────────────────────────────────────────────────────────────────────────────

def get_sentence(text, idx, length):
    start, end = 0, len(text)
    for i in range(idx - 1, -1, -1):
        if text[i] in ".!?":
            start = i + 1
            break
    for i in range(idx + length, len(text)):
        if text[i] in ".!?":
            end = i + 1
            break
    return text[start:end].strip()

def scan_file(filepath):
    try:
        with open(filepath, encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
    except Exception:
        return []

    fname    = os.path.basename(filepath)
    elements = extract_elements(raw)
    seen     = set()
    results  = []

    for el in elements:
        text = el["text"]
        for td in SORTED_TERMS:
            key = td["term"] + "||" + el["inner_html"][:100]
            if key in seen:
                continue
            pat = re.compile(r"\b" + re.escape(td["term"]) + r"\b", re.IGNORECASE)
            m   = pat.search(text)
            if m:
                seen.add(key)
                results.append({
                    "file":       fname,
                    "filepath":   filepath,
                    "term":       td["term"],
                    "matched":    m.group(),
                    "cat":        td["cat"],
                    "risk":       td["risk"],
                    "question":   td["q"],
                    "sentence":   get_sentence(text, m.start(), len(m.group())),
                    "inner_html": el["inner_html"],
                    "tag":        el["tag"],
                })
    return results

# ─────────────────────────────────────────────────────────────────────────────
#  COLORS
# ─────────────────────────────────────────────────────────────────────────────
BG    = "#0f0f0f"
BG1   = "#141414"
BG2   = "#1c1c1c"
BG3   = "#242424"
BORD  = "#2a2a2a"
FG    = "#e2e2e2"
FG2   = "#999999"
FG3   = "#555555"
GOLD  = "#d4af37"
TEAL  = "#2dd4bf"
RED   = "#ef4444"
ORG   = "#f97316"
YLW   = "#eab308"
GRN   = "#22c55e"

# ─────────────────────────────────────────────────────────────────────────────
#  GUI
# ─────────────────────────────────────────────────────────────────────────────

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("DP Term Coherence Scanner")
        self.root.configure(bg=BG)
        self.root.geometry("1300x840")
        self.root.minsize(900, 600)

        self.folder_path   = None
        self.all_findings  = []
        self.file_findings = {}   # fname -> list
        self._displayed    = []   # currently shown in tree
        self._current      = None # currently selected finding

        self._style()
        self._build()

    # ── STYLES ───────────────────────────────────────────────
    def _style(self):
        s = ttk.Style()
        s.theme_use("clam")

        s.configure("TFrame",         background=BG)
        s.configure("TLabel",         background=BG,  foreground=FG,  font=("Segoe UI", 10))
        s.configure("TLabelframe",    background=BG,  foreground=FG2)
        s.configure("TLabelframe.Label", background=BG, foreground=FG3, font=("Segoe UI", 9))
        s.configure("TSeparator",     background=BORD)

        s.configure("TButton",        background=BG2, foreground=FG, borderwidth=1,
                    relief="flat", font=("Segoe UI", 10), padding=(8,4))
        s.map("TButton",
              background=[("active", BG3), ("disabled", BG1)],
              foreground=[("disabled", FG3)])

        s.configure("Gold.TButton",   background=GOLD, foreground="#000",
                    font=("Segoe UI", 10, "bold"), padding=(10,5))
        s.map("Gold.TButton",         background=[("active","#c9a020"),("disabled","#7a6010")])

        s.configure("Treeview",       background=BG1, foreground=FG,
                    fieldbackground=BG1, borderwidth=0, rowheight=24,
                    font=("Segoe UI", 10))
        s.configure("Treeview.Heading", background=BG2, foreground=FG2,
                    relief="flat", font=("Segoe UI", 9, "bold"))
        s.map("Treeview",
              background=[("selected", BG3)],
              foreground=[("selected", GOLD)])

        s.configure("TEntry",         fieldbackground=BG2, foreground=FG,
                    insertcolor=FG, borderwidth=1)
        s.configure("TCombobox",      fieldbackground=BG2, foreground=FG,
                    background=BG2, arrowcolor=FG2, borderwidth=1)
        s.map("TCombobox",            fieldbackground=[("readonly", BG2)])

        s.configure("Vertical.TScrollbar",   background=BG2, troughcolor=BG,
                    borderwidth=0, arrowsize=11)
        s.configure("Horizontal.TScrollbar", background=BG2, troughcolor=BG,
                    borderwidth=0, arrowsize=11)

    # ── BUILD UI ─────────────────────────────────────────────
    def _build(self):
        root = self.root

        # ── Header ──────────────────────────────────────────
        hdr = tk.Frame(root, bg=BG1, height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        hi  = tk.Frame(hdr, bg=BG1)
        hi.pack(fill="both", expand=True, padx=18, pady=6)

        tk.Label(hi, text="Duality Project", bg=BG1, fg=GOLD,
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        tk.Label(hi, text=" | Term Coherence Scanner", bg=BG1, fg=FG3,
                 font=("Segoe UI", 10)).pack(side="left")

        bf = tk.Frame(hi, bg=BG1)
        bf.pack(side="right")
        self.export_btn = ttk.Button(bf, text="Export JSON", command=self.export_json)
        self.export_btn.pack(side="right", padx=(4,0))
        self.export_btn.state(["disabled"])
        self.scan_btn = ttk.Button(bf, text="Scan All Files", style="Gold.TButton",
                                   command=self.scan_all)
        self.scan_btn.pack(side="right", padx=(4,0))
        self.scan_btn.state(["disabled"])
        ttk.Button(bf, text="Open Folder", command=self.open_folder).pack(side="right")

        # ── Status bar ──────────────────────────────────────
        sb = tk.Frame(root, bg=BG2, height=24)
        sb.pack(fill="x")
        sb.pack_propagate(False)
        self.status_var = tk.StringVar(value='No folder selected. Click "Open Folder".')
        tk.Label(sb, textvariable=self.status_var, bg=BG2, fg=FG2,
                 font=("Segoe UI", 9), anchor="w", padx=16).pack(fill="both", expand=True)

        # ── Stats bar ───────────────────────────────────────
        stats = tk.Frame(root, bg=BG1, height=32)
        stats.pack(fill="x")
        stats.pack_propagate(False)
        si = tk.Frame(stats, bg=BG1)
        si.pack(side="left", padx=16, fill="y")
        self.sv = {}
        for label, color, key in [
            ("Critical", RED, "crit"), ("High", ORG, "high"),
            ("Medium",   YLW, "med"),  ("Low",  GRN, "low"),
            ("Total",    FG,  "tot"),
        ]:
            f = tk.Frame(si, bg=BG1)
            f.pack(side="left", padx=6)
            v = tk.StringVar(value="0")
            self.sv[key] = v
            tk.Label(f, textvariable=v, bg=BG1, fg=color,
                     font=("Segoe UI", 13, "bold")).pack(side="left")
            tk.Label(f, text=" " + label, bg=BG1, fg=FG3,
                     font=("Segoe UI", 9)).pack(side="left")

        tk.Frame(root, bg=BORD, height=1).pack(fill="x")

        # ── Body: vertical paned ────────────────────────────
        body = tk.PanedWindow(root, orient="vertical", bg=BG,
                              sashwidth=5, sashrelief="flat")
        body.pack(fill="both", expand=True)

        # Top pane: horizontal - file list | findings
        top = tk.PanedWindow(body, orient="horizontal", bg=BG,
                             sashwidth=5, sashrelief="flat")

        # ── File list ───────────────────────────────────────
        ff = tk.Frame(top, bg=BG1, width=210)
        ff.pack_propagate(False)
        tk.Label(ff, text="FILES", bg=BG1, fg=FG3, font=("Segoe UI", 9, "bold"),
                 anchor="w", padx=12, pady=5).pack(fill="x")
        tk.Frame(ff, bg=BORD, height=1).pack(fill="x")
        fscroll = ttk.Scrollbar(ff, orient="vertical")
        fscroll.pack(side="right", fill="y")
        self.file_lb = tk.Listbox(ff, bg=BG1, fg=FG2, selectbackground=BG3,
                                  selectforeground=GOLD, borderwidth=0,
                                  highlightthickness=0, font=("Segoe UI", 9),
                                  activestyle="none", yscrollcommand=fscroll.set)
        self.file_lb.pack(fill="both", expand=True)
        fscroll.config(command=self.file_lb.yview)
        self.file_lb.bind("<<ListboxSelect>>", self._on_file_select)
        top.add(ff, minsize=160)

        # ── Findings panel ──────────────────────────────────
        rp = tk.Frame(top, bg=BG)
        top.add(rp, minsize=400)

        # Filter bar
        fbar = tk.Frame(rp, bg=BG2, height=36)
        fbar.pack(fill="x")
        fbar.pack_propagate(False)
        fi = tk.Frame(fbar, bg=BG2)
        fi.pack(side="left", padx=10, fill="y")

        tk.Label(fi, text="Search:", bg=BG2, fg=FG3,
                 font=("Segoe UI", 9)).pack(side="left")
        self.search_v = tk.StringVar()
        self.search_v.trace_add("write", lambda *_: self._apply_filters())
        ttk.Entry(fi, textvariable=self.search_v, width=18).pack(side="left", padx=(3,10))

        tk.Label(fi, text="Risk:", bg=BG2, fg=FG3,
                 font=("Segoe UI", 9)).pack(side="left")
        self.risk_v = tk.StringVar(value="All")
        rc = ttk.Combobox(fi, textvariable=self.risk_v, width=9, state="readonly",
                          values=["All","Critical","High","Medium","Low"])
        rc.pack(side="left", padx=(3,10))
        rc.bind("<<ComboboxSelected>>", lambda _: self._apply_filters())

        tk.Label(fi, text="Category:", bg=BG2, fg=FG3,
                 font=("Segoe UI", 9)).pack(side="left")
        self.cat_v = tk.StringVar(value="All")
        self.cat_cb = ttk.Combobox(fi, textvariable=self.cat_v, width=16, state="readonly")
        self.cat_cb.pack(side="left", padx=(3,0))
        self.cat_cb.bind("<<ComboboxSelected>>", lambda _: self._apply_filters())

        # Treeview
        tvf = tk.Frame(rp, bg=BG)
        tvf.pack(fill="both", expand=True)
        vsc = ttk.Scrollbar(tvf, orient="vertical")
        vsc.pack(side="right", fill="y")
        hsc = ttk.Scrollbar(tvf, orient="horizontal")
        hsc.pack(side="bottom", fill="x")

        self.tree = ttk.Treeview(tvf,
            columns=("risk","term","cat","sentence","file"),
            show="headings", selectmode="browse",
            yscrollcommand=vsc.set, xscrollcommand=hsc.set)
        for col, label, w, stretch in [
            ("risk",     "Risk",     68,  False),
            ("term",     "Term",     130, False),
            ("cat",      "Category", 130, False),
            ("sentence", "Sentence", 480, True),
            ("file",     "File",     190, False),
        ]:
            self.tree.heading(col, text=label, anchor="w",
                              command=lambda c=col: self._sort_by(c))
            self.tree.column(col, width=w, minwidth=50, stretch=stretch)
        self.tree.pack(fill="both", expand=True)
        vsc.config(command=self.tree.yview)
        hsc.config(command=self.tree.xview)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.tag_configure("r4", foreground=RED)
        self.tree.tag_configure("r3", foreground=ORG)
        self.tree.tag_configure("r2", foreground=YLW)
        self.tree.tag_configure("r1", foreground=GRN)

        body.add(top, minsize=260)

        # ── Edit / detail panel ─────────────────────────────
        ep = tk.Frame(body, bg=BG1)
        body.add(ep, minsize=170)

        # Term + file labels
        eh = tk.Frame(ep, bg=BG1)
        eh.pack(fill="x", padx=14, pady=(8,0))
        self.eterm = tk.Label(eh, text="Select a finding to edit",
                              bg=BG1, fg=FG2, font=("Segoe UI", 11, "bold"))
        self.eterm.pack(side="left")
        self.efile = tk.Label(eh, text="", bg=BG1, fg=FG3,
                              font=("Segoe UI", 9, "italic"))
        self.efile.pack(side="left", padx=10)

        # Question label (teal)
        self.eq = tk.Label(ep, text="", bg=BG1, fg=TEAL,
                           font=("Segoe UI", 9), wraplength=1100,
                           justify="left", anchor="w", padx=14)
        self.eq.pack(fill="x", pady=(3,0))

        # Sentence (italic)
        self.esent = tk.Label(ep, text="", bg=BG1, fg=FG2,
                              font=("Segoe UI", 9, "italic"), wraplength=1100,
                              justify="left", anchor="w", padx=14)
        self.esent.pack(fill="x", pady=(2,5))

        tk.Frame(ep, bg=BORD, height=1).pack(fill="x")

        # Editor
        ef = tk.Frame(ep, bg=BG1)
        ef.pack(fill="both", expand=True, padx=14, pady=(6,0))
        tk.Label(ef, text="Element HTML (editable):", bg=BG1, fg=FG3,
                 font=("Segoe UI", 8)).pack(anchor="w")
        self.editor = tk.Text(ef, bg=BG2, fg=FG, insertbackground=FG,
                              font=("Courier New", 10), height=4,
                              wrap="word", borderwidth=0,
                              highlightthickness=1, highlightbackground=BORD,
                              highlightcolor=GOLD, relief="flat", state="disabled")
        self.editor.pack(fill="both", expand=True, pady=(3,0))

        # Save bar
        sbar = tk.Frame(ep, bg=BG1)
        sbar.pack(fill="x", padx=14, pady=6)
        ttk.Button(sbar, text="Save to File", style="Gold.TButton",
                   command=self.save_edit).pack(side="left")
        ttk.Button(sbar, text="Clear", command=self._clear_edit).pack(side="left", padx=6)
        self.save_lbl = tk.Label(sbar, text="", bg=BG1, fg=FG2,
                                 font=("Segoe UI", 9))
        self.save_lbl.pack(side="left", padx=8)

        # Sash positions
        self.root.update_idletasks()
        try:
            body.sash_place(0, 0, 580)
        except Exception:
            pass

    # ── ACTIONS ──────────────────────────────────────────────

    def open_folder(self):
        path = filedialog.askdirectory(title="Select Duality Project Folder")
        if not path:
            return
        self.folder_path = path
        html_files = [f for f in os.listdir(path)
                      if f.endswith(".html") and f != "term-scanner.html"]
        self._status(f'Folder: {os.path.basename(path)} - {len(html_files)} HTML files found. Click "Scan All Files".')
        self.scan_btn.state(["!disabled"])

    def scan_all(self):
        if not self.folder_path:
            return
        files = sorted(f for f in os.listdir(self.folder_path)
                       if f.endswith(".html") and f != "term-scanner.html")
        if not files:
            self._status("No HTML files found in folder.")
            return

        self.scan_btn.state(["disabled"])
        self.all_findings  = []
        self.file_findings = {}
        self.tree.delete(*self.tree.get_children())
        self.file_lb.delete(0, "end")
        self._clear_edit()
        self._status("Scanning...")

        def worker():
            for i, fname in enumerate(files):
                self.root.after(0, self._status,
                    f"Scanning {i+1}/{len(files)}: {fname}...")
                fp = os.path.join(self.folder_path, fname)
                ff = scan_file(fp)
                self.all_findings.extend(ff)
                self.file_findings[fname] = ff
            self.root.after(0, self._scan_done)

        threading.Thread(target=worker, daemon=True).start()

    def _scan_done(self):
        n = len(self.all_findings)
        f = len(self.file_findings)
        self._status(f"Done - {n} flags across {f} files.")
        self.scan_btn.state(["!disabled"])
        self.export_btn.state(["!disabled"])
        # Populate category combo
        cats = ["All"] + sorted(set(x["cat"] for x in self.all_findings))
        self.cat_cb["values"] = cats
        self.cat_v.set("All")
        # Populate file list
        self.file_lb.delete(0, "end")
        self.file_lb.insert("end", f"All files  ({n})")
        for fname in sorted(self.file_findings):
            self.file_lb.insert("end", f"  {fname}  ({len(self.file_findings[fname])})")
        self.file_lb.selection_set(0)
        self._apply_filters()

    def _apply_filters(self, file_filter=None):
        q    = self.search_v.get().strip().lower()
        risk = self.risk_v.get()
        cat  = self.cat_v.get()

        src = self.file_findings.get(file_filter, self.all_findings) if file_filter else self.all_findings

        out = []
        for f in src:
            if risk != "All" and RISK_LABELS[f["risk"]] != risk:
                continue
            if cat != "All" and f["cat"] != cat:
                continue
            if q:
                hay = (f["term"] + " " + f["sentence"] + " " + f["file"] + " " + f["cat"]).lower()
                if q not in hay:
                    continue
            out.append(f)

        self._render(out)

    def _render(self, findings):
        self.tree.delete(*self.tree.get_children())
        self._displayed = findings
        c = {4:0, 3:0, 2:0, 1:0}
        for i, f in enumerate(findings):
            c[f["risk"]] += 1
            sent = f["sentence"][:110] + ("..." if len(f["sentence"]) > 110 else "")
            self.tree.insert("", "end", iid=str(i), tags=(f"r{f['risk']}",),
                values=(RISK_LABELS[f["risk"]], f["term"], f["cat"], sent, f["file"]))
        self.sv["crit"].set(str(c[4]))
        self.sv["high"].set(str(c[3]))
        self.sv["med"].set(str(c[2]))
        self.sv["low"].set(str(c[1]))
        self.sv["tot"].set(str(len(findings)))

    def _sort_by(self, col):
        col_map = {"risk": lambda f: f["risk"], "term": lambda f: f["term"],
                   "cat":  lambda f: f["cat"],  "file": lambda f: f["file"],
                   "sentence": lambda f: f["sentence"]}
        if col in col_map:
            self._displayed = sorted(self._displayed, key=col_map[col])
            self._render(self._displayed)

    def _on_file_select(self, _evt):
        sel = self.file_lb.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx == 0:
            self._apply_filters()
        else:
            fname = sorted(self.file_findings.keys())[idx - 1]
            self._apply_filters(file_filter=fname)

    def _on_tree_select(self, _evt):
        sel = self.tree.selection()
        if not sel:
            return
        f = self._displayed[int(sel[0])]
        self._current = f
        color = RISK_COLORS[f["risk"]]
        self.eterm.config(text=f'[{RISK_LABELS[f["risk"]]}]  {f["term"]}', fg=color)
        self.efile.config(text=f'{f["file"]} | <{f["tag"]}>')
        self.eq.config(text="?  " + f["question"])
        self.esent.config(text='"' + f["sentence"] + '"')
        self.editor.config(state="normal")
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", f["inner_html"])
        self.save_lbl.config(text="", fg=FG2)

    def save_edit(self):
        if not self._current:
            messagebox.showinfo("No selection", "Select a finding in the table first.")
            return
        f        = self._current
        new_html = self.editor.get("1.0", "end-1c")
        orig     = f["inner_html"]
        if new_html == orig:
            self.save_lbl.config(text="No changes made.", fg=FG2)
            return
        try:
            with open(f["filepath"], encoding="utf-8") as fh:
                raw = fh.read()
        except Exception as e:
            self.save_lbl.config(text=f"Read error: {e}", fg=RED)
            return
        idx = raw.find(orig)
        if idx == -1:
            self.save_lbl.config(
                text="[!] Could not locate element - file may have changed. Re-scan.", fg=ORG)
            return
        new_raw = raw[:idx] + new_html + raw[idx + len(orig):]
        try:
            with open(f["filepath"], "w", encoding="utf-8") as fh:
                fh.write(new_raw)
        except Exception as e:
            self.save_lbl.config(text=f"Write error: {e}", fg=RED)
            return
        f["inner_html"] = new_html  # update in memory
        self.save_lbl.config(text="Saved successfully", fg=GRN)

    def _clear_edit(self):
        self._current = None
        self.eterm.config(text="Select a finding to edit", fg=FG2)
        self.efile.config(text="")
        self.eq.config(text="")
        self.esent.config(text="")
        self.editor.config(state="normal")
        self.editor.delete("1.0", "end")
        self.editor.config(state="disabled")
        self.save_lbl.config(text="")

    def export_json(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="dp-scan-results.json")
        if not path:
            return
        data = [{k: v for k, v in f.items() if k not in ("filepath","inner_html")}
                for f in self.all_findings]
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        messagebox.showinfo("Exported",
            f"Saved {len(data)} findings to:\n{os.path.basename(path)}")

    def _status(self, msg):
        self.status_var.set(msg)
        self.root.update_idletasks()


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap(default="")
    except Exception:
        pass
    app = App(root)
    root.mainloop()
