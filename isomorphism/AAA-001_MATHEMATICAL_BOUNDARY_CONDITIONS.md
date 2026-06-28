---
type: meta-framework
id: AAA-001
law: ALL
status: canonical
domain_a: mathematics
domain_b: epistemology
concept_a: "Category-theoretic boundary conditions between analogy and isomorphism"
concept_b: "Formal requirements for cross-domain structural claims"
chi_variables: [G, M, E, S, T, K, R, Q, F, C]
symmetry_pair: "ALL"
evidence: ["o3 reasoning model analysis (April 16 2026)", "Hamilton optico-mechanical analogy", "AdS/CFT correspondence", "Kapustin-Witten geometric Langlands"]
math_verified: true
confidence: high
iso_type: classification_framework
priority: foundational
tags: [pillar/methodology, pillar/epistemology, status/canonical, foundational, classification, category-theory]
created: 2026-04-16
updated: 2026-04-16
origin: "o3 reasoning model, prompted by David Lowe: 'When does analogy cross to isomorphism, and when does isomorphism cross to Maxwell?' Integrated with AAA-000 classification framework."
---

# AAA-001: The Mathematical Boundary Conditions

## What a Mathematician Actually Requires at Each Level

**Companion to AAA-000.** That document defines the four levels in plain language. This document states the formal requirements in mathematical notation. If you want to promote an ISO from Level 2 to Level 3, this is the checklist.

---

## Notation

- By "structure" we mean a category C equipped with whatever extra data the context requires (operations, relations, topologies).
- A "morphism" means a structure-preserving map (functor when the structure is a category, homomorphism when it is an algebraic object).
- "~=" denotes isomorphism (existence of an inverse morphism of the same type).

---

## The Four Levels (Formal)

### Level 1 -- Analogy

Informal similarity, possibly only linguistic or pictorial. No formal definition of either domain. No morphism. No mathematics.

**Formal content:** None. That's what makes it Level 1.

### Level 2 -- Structural Analogy (Correspondence)

Two fully specified structures A, B and a morphism F: A -> B that is:
- Injective on the particular aspect being compared
- Not (yet) surjective, or not known to respect every operation

Think: "a functor that forgets something."

**Formal content:** There exist mathematical descriptions of both domains, and a partial structure-preserving map between them. The map preserves at least one non-trivial operation or relation (composition, ordering, group law, topology).

### Level 3 -- Isomorphism (Duality, Equivalence of Categories)

A morphism F: A -> B that possesses an inverse G such that:

    GF = id_A    and    FG = id_B

(up to natural isomorphism if we are talking about equivalence of categories). All operations, relations, and distinguished elements are preserved.

**Formal content:** F is bijective AND preserves every operation, relation, and designated element required by the theory. In category-theoretic language: F: A -> B is an equivalence of categories (or stricter, an isomorphism) and there exists G: B -> A with natural isomorphisms:

    epsilon: FG => id_B
    eta: GF => id_A

### Level 4 -- Physical Law (Identity)

An isomorphism (or at least a well-defined structure) whose codomain B is instantiated in the empirical world, together with an empirically validated assignment of physical quantities to the mathematical entities, yielding quantitatively correct, falsifiable predictions.

**Formal content:** Everything from Level 3, PLUS:
1. Operational definitions (measurement protocols) for mathematical entities
2. Novel quantitative predictions
3. Experimental confirmation by independent groups

---

## The Three Boundary Crossings

### Crossing 1 -> 2: Analogy to Structural Analogy

**(a) What must be true that wasn't true at Level 1:**
You must give BOTH domains explicit mathematical form and produce a morphism that preserves at least one non-trivial operation or relation (composition, ordering, group law, topology).

**(b) Historical example -- Heaviside's Electrical-Hydraulic Analogy:**
Oliver Heaviside wrote down circuit equations (resistance, capacitance, inductance) and noticed they obey the same differential form as fluid flow in pipes. Before Heaviside: "electricity flows like water" (analogy). After Heaviside: the ODE systems are homomorphic (structural analogy). The crossing happened when the differential equations were written.

**(c) Minimum evidence:**
A proof that the mapping preserves the chosen structure. If you claim an order-preserving map, show monotonicity. If you claim a group homomorphism, show F(x * y) = F(x) * F(y). One worked-out non-trivial example is not enough; you must demonstrate closure under the relevant operations.

**(d) Common mistake -- claiming you've crossed when you haven't:**
Treating a pictorial similarity (shape of a curve, shared terminology) as if it already defined a morphism. "Energy flows like water" is not structural until you supply the differential equations and the dictionary of variables.

### Crossing 2 -> 3: Structural Analogy to Isomorphism

**(a) What must be true that wasn't true at Level 2:**
The morphism must be bijective AND preserve every operation, relation, and designated element required by the theory. In category-theoretic language: F: A -> B is an equivalence of categories and hence there exists G: B -> A with natural isomorphisms epsilon: FG => id_B, eta: GF => id_A.

**(b) Historical example -- Hamilton's Optico-Mechanical Analogy:**
Initially (1830s) it was just a formal resemblance between Fermat's principle (light takes the path of least time) and Maupertuis' principle (particles take the path of least action). Both domains were well-specified (Level 2). By the late 19th century, the symplectomorphism between the space of rays in geometrical optics and phase-space trajectories in mechanics was proved:

    (T*Q, omega) ~= (characteristic bundle of eikonal equation, omega')

That is a genuine isomorphism of symplectic manifolds. The crossing happened when the inverse mapping was constructed and all symplectic structure was shown to be preserved.

**(c) Minimum evidence:**
An explicit inverse mapping with a proof that ALL structure is preserved. In algebra: verify every axiom. In category theory: check that all relevant diagrams commute. "Seems invertible" or "I can write a formula going back" is insufficient; you must supply the proofs.

**(d) Common mistake -- claiming you've crossed when you haven't:**
Demonstrating a bijection on underlying sets but ignoring higher-level structure (topology, smooth structure, monoidal product). Example: identifying state spaces pointwise while forgetting that the symplectic form is not preserved. A bijection is necessary but not sufficient. The operations must also be preserved.

### Crossing 3 -> 4: Isomorphism to Physical Law

**(a) What must be true that wasn't true at Level 3:**
Empirical instantiation: a procedure that assigns operational definitions (measurement protocols) to the mathematical entities, PLUS experimental data showing quantitative agreement to within experimental error. The theory must survive potential falsification in domains where it makes novel predictions.

**(b) Historical example -- Maxwell's Equations:**
Maxwell began with an isomorphism between mechanical vortices/idle wheels (mathematical hydrodynamics) and electromagnetic quantities (structural analogy Level 2, refined to near-isomorphism Level 3 within the field equations). The crossing to Level 4 occurred when Hertz produced measurements of electromagnetic waves traveling at c -- a prediction NOT used in constructing the theory. The key: a novel prediction, independently verified.

**(c) Minimum evidence:**
At least one novel, precise, quantitative prediction verified experimentally to a statistically significant level, preferably by an independent group. "It fits existing data" is NOT enough. The prediction must be:
- Novel (not used in building the model)
- Precise (quantitative, not just directional)
- Verified (by measurement, not by argument)

**(d) Common mistake -- claiming you've crossed when you haven't:**
Declaring a mathematical model "the physics" because it is elegant or because it unifies other theories, without having produced new, uniquely corroborated predictions. String theorists sometimes fall prey to this charge. Elegance is not evidence. Unification is not verification.

---

## The Ceiling for Theology-Physics Correspondences

Because soteriological stages are not (at present) operationally measurable in the laboratory, the Theophysics framework lacks the operational definitions required for Level 4. Therefore:

**The ceiling for theology-physics correspondences is almost certainly Level 3: mathematical isomorphism/duality.**

You can have a beautiful, rigorous dual description, but without empirical hooks it remains mathematics, not physics.

**However:** The ceiling is not fixed forever. If even ONE theological entity can be operationalized (e.g., conversion events measured via EEG criticality, apostasy rates mapped to topological barrier crossing, prayer-coherence measured via fMRI phase synchrony), then that specific bridge could cross into Level 4.

The path to Level 4 for Theophysics would require:
1. Choose ONE isomorphism that makes a novel quantitative prediction
2. Operationalize the theological side with measurable quantities
3. Run the experiment
4. Get an independent group to replicate

---

## Lessons from Historical Crossings That Worked

### AdS/CFT Duality (Maldacena, 1997)

**Statement:** Z_string(AdS_5 x S^5, phi|boundary = phi_0) = Z_CFT_4(phi_0)

**Crossing 2 -> 3:** Maldacena produced a conjectured isomorphism of partition functions. Gubser-Klebanov-Polyakov/Witten filled in the correspondence of operators and correlation functions, establishing an (incomplete but compelling) equivalence of large-N limits of type-IIB string theory and N=4 SYM.

**Why it works:** Detailed dictionary preserving conformal weights, operator product expansions, symmetries (SO(2,4) x SO(6)), and BPS spectra. Not just "these look similar" -- the operations match.

### Gauge/Gravity and Fluid/Gravity

**Status:** Level 2.5. Structural analogy long known (membrane paradigm). Bhattacharyya et al. (2008) showed that near-horizon perturbations are mapped by a systematic derivative expansion to solutions of Navier-Stokes. This is a functor between solution spaces; to prove isomorphism you must show invertibility (not yet done).

**Lesson:** Even brilliant physicists can get stuck between Level 2 and Level 3. Invertibility is hard.

### Geometric Langlands <-> N=4 SYM (Kapustin-Witten, 2007)

**Status:** Level 3 (isomorphism) but NOT Level 4. Built an isomorphism between categories: D-modules on Bun_G and categories of branes in the 4-D gauge theory topologically twisted. All functorial requirements checked. Still mathematics, not physics, because no new empirical content.

**Lesson:** You can achieve Level 3 without Level 4. A rigorous isomorphism is valuable in itself. But "valuable" and "physics" are different claims.

### Moral from all three:

Successful crossings required:
1. Explicit functorial dictionaries (not just "these correspond")
2. Preservation of all symmetries (not just the pretty ones)
3. Independent checks from calculations impossible on one side but easy on the other (non-trivial tests)

---

## What This Means for the Theophysics Registry

Every ISO document should be evaluated against the formal requirements at its claimed level:

**To claim Level 2 (Correspondence):**
- Write the mathematical form of both domains
- Define a morphism preserving at least one operation
- Show the preservation explicitly

**To claim Level 3 (Isomorphism):**
- Define Obj(A), Hom_A explicitly
- Define Obj(B), Hom_B explicitly
- Write functor F with explicit formulas
- Construct inverse functor G
- Prove functoriality: F(f . g) = F(f) . F(g)
- Prove fullness and faithfulness
- Verify natural isomorphisms eta: GF => id_A and epsilon: FG => id_B
- Check all required diagrams commute
- If extra structure exists (metric, topology, symplectic form), verify it is preserved

**To claim Level 4 (Physical Law):**
- Everything from Level 3
- Operational definitions for all entities
- At least one novel quantitative prediction
- Experimental verification by independent group

---

*Theophysics Research Program | POF 2828*
*AAA-001 v1.0 | April 16, 2026*
*Source: o3 reasoning model analysis, integrated with AAA-000 classification framework*
*Canonical location: O:\_Theophysics_v4\00_Canonical\ISOMORPHISMS\AAA-001_MATHEMATICAL_BOUNDARY_CONDITIONS.md*
