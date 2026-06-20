---
title: "De Revolutionibus Veritatis | Book II: The Lock"
source_type: "html_rip"
html_path: "revolution-of-truth\drv-02-the-lock.html"
---

## I. Introduction

Eugene Wigner's celebrated paper "The Unreasonable Effectiveness of Mathematics in the Natural Sciences" (1960) posed a question that remains unanswered in contemporary philosophy of mathematics: Why do abstract mathematical structures, developed without reference to physical reality, consistently and precisely describe that reality? This paper provides a definitive answer. The effectiveness is not unreasonable but inevitable, once you understand what mathematical truth is and where it comes from.

We proceed in five stages: establishing the information-theoretic foundations; deriving the properties of mathematical truth through twenty axioms; demonstrating that these properties necessitate an external ground with specific characteristics; addressing all major objections; and presenting testable predictions.

### Central Claim

Mathematical truth is grounded in a necessary, eternal, universal, immaterial, coherent, and morally good source. This source is functionally identical to the Logos of classical theology. This conclusion is not asserted but *derived* from first principles using information theory.

## II. Information-Theoretic Foundations

### 2.1 Shannon Entropy

The first tool you need is Shannon entropy. For a discrete random variable \(X\) with possible values \(\{x_1, x_2, \ldots, x_n\}\) and probability mass function \(P(X)\), Shannon entropy \(H(X)\) is defined as:

Definition 1 — Shannon Entropy
$$H(X) = -\sum_i P(x_i) \log_2 P(x_i)$$

Shannon entropy measures the average information content or uncertainty in a random variable. Maximum entropy occurs when all outcomes are equally likely—maximum uncertainty. Minimum entropy occurs when one outcome has probability 1—no uncertainty at all. This distinction matters enormously when we get to physical law.

### 2.2 Kolmogorov Complexity

The second tool is Kolmogorov complexity. For a string \(x\) and a universal Turing machine \(U\), the Kolmogorov complexity \(K(x)\) is the length of the shortest program \(p\) such that \(U(p) = x\):

Definition 2 — Kolmogorov Complexity
$$K(x) = \min\{|p| : U(p) = x\}$$

Kolmogorov complexity measures the intrinsic information content of a string, independent of any probability distribution. A string is random—incompressible—if \(K(x) \approx |x|\). It is structured—compressible—if \(K(x) \ll |x|\).

### 2.3 The Compression-Entropy Bridge

Theorem 1 — Compression-Entropy Bridge
$$K(x) \approx H(X) \text{ for random strings}$$
                $$K(x) \ll H(X) \text{ for structured strings}$$

Random strings have no exploitable patterns; their shortest description is the string itself. Structured strings have patterns that allow compression below their raw length.

### The Critical Observation

The physical universe exhibits \(K \ll H\). Physical laws are compressions—short equations that describe vast amounts of phenomena. The existence of any physical law means the universe is not random but is compressed information. This observation is foundational to everything that follows.

### 2.4 Chaitin's Incompleteness Theorem

The third tool is the most decisive. For any formal system \(F\), there exists a constant \(c\) such that \(F\) cannot prove \(K(x) > |F| + c\) for any string \(x\):

Theorem 2 — Chaitin's Incompleteness
$$\forall F, \exists c : F \nvdash K(x) > |F| + c$$

Corollary 1 — Mathematical Truth Cannot Self-Ground
$$\text{Ground}(\text{Math}) \notin \text{Math}$$

This is the formal statement that mathematical truth requires an external ground. No formal system can fully capture or justify the truths it uses. The ground of mathematics must be meta-mathematical. Everything that follows flows from this single, non-negotiable fact.

## III. The Axiom Chain

Twenty axioms, organized into six levels. Each axiom is individually undeniable—its negation leads to absurdity, self-refutation, or the collapse of rational discourse. Together, they derive the existence and properties of the ground of mathematical truth.

### Level 1: Existence (A1–A3)

A1 — Existence

Mathematical truths exist that are non-contingently true.

$$\exists\, T_m : \text{True}(T_m) \wedge \neg\text{Contingent}(T_m)$$

If no mathematical truths existed, then "no mathematical truths exist" would itself be a mathematical truth, yielding a contradiction. The denial of A1 is self-refuting.

A2 — Temporal Independence

Mathematical truths held at all times prior to human existence and will hold after.

$$\forall t : \text{True}(T_m, t) \text{ with } I(T_m; t) = 0$$

If mathematical truths only became true when humans evolved, then physical laws could not have operated for 13.8 billion years before us. Stars could not have formed. The universe could not exist in its present state. Denial leads to empirical absurdity.

A3 — Necessity

Mathematical truths are necessarily true; their negations are impossible.

$$\square(2+2=4) \wedge \neg\Diamond(2+2=5)$$

If \(2+2=5\) were possible in some world, logical inference would be arbitrary and could not be trusted. But we cannot even state that possibility without presupposing the validity of logic. The denial is self-undermining.

### Level 2: Properties (A4–A7)

A4 — Universality

Mathematical truth is location-invariant.

$$I(T_m; \text{position}) = 0$$

If mathematical truth varied by location, physics would be different in different places. GPS would not work. Rockets could not navigate. No coherent universe could exist with location-dependent mathematics.

A5 — Eternality

Mathematical truth does not change over time.

$$\frac{d}{dt} K(T_m) = 0$$

If \(2+2=4\) today but might equal 5 tomorrow, scientific knowledge would be impossible. Every experiment would be meaningless. Science presupposes A5.

A6 — Immateriality

Mathematical truth has no spatial location, mass, or physical properties.

$$\neg\exists x : \text{Location}(T_m) = x \wedge \text{Mass}(T_m) = 0$$

If mathematical truth were physical, destroying its location would destroy the truth. But no physical destruction can make \(2+2 \neq 4\). Mathematical truth is immune to physical intervention.

A7 — Coherence

No true mathematical statement contradicts another true mathematical statement.

$$\forall T_1, T_2 \in T_m : \neg(T_1 \wedge \neg T_1)$$

By the principle of explosion (ex falso quodlibet), a contradiction implies everything. If mathematics were internally contradictory, every statement would be provable, and mathematics would be trivial and useless.

Checkpoint Alpha — The Emergent Profile

From axioms A1–A7, you have established that mathematical truth is: existent, necessary, eternal, universal, immaterial, and coherent. This profile matches no physical object in the universe.

But it is precisely isomorphic to the classical divine attributes: Being (exists), Aseity (necessary), Eternality, Omnipresence (universal), Spirituality (immaterial), and Integrity (coherent).

These properties were derived from the analysis of mathematical truth alone—not from theological premises. The theological identification comes after the logical derivation.

### Level 3: Origin (A8–A11)

A8 — Sufficient Reason

Mathematical truth requires grounding; brute facts are explanatorily unacceptable.

$$K(T_m \mid \text{Ground}) < K(T_m) \Rightarrow \exists\, \text{Ground}(T_m)$$

The Principle of Sufficient Reason is presupposed by all rational inquiry. To ask "why?" is to presuppose that explanations exist. If mathematical truths were brute facts requiring no explanation, then nothing would require explanation, and science would be impossible.

A9 — Not From Nothing

Nothing cannot produce something.

$$K(\emptyset) = 0 \Rightarrow \text{Output}(\emptyset) = \emptyset$$

"Nothing" has zero information content by definition. An output requires information. Zero information cannot produce non-zero information. This is not a metaphysical claim but an information-theoretic necessity.

A10 — Not From Chaos

Random processes cannot produce structured output.

$$K(T_m) \ll |T_m| \Rightarrow \neg\text{Random}(\text{Ground})$$

Random processes produce maximum entropy. But mathematical truth is highly structured—compressible. The Kolmogorov complexity of mathematical truths is vastly less than their raw description length. This structure cannot emerge from randomness; it requires a structured source.

A11 — Not From Deception

Truth cannot originate from a deceptive source.

$$\neg\text{Deceptive}(T_m) \Rightarrow \neg\text{Deceptive}(\text{Ground})$$

Deception is defined as divergence between appearance and reality: \(\text{Deception}(X) \iff \text{Appears}(X,Y) \wedge \neg\text{Is}(X,Y)\). Mathematical truth involves no such divergence—\(2+2\) appears to equal 4 and actually does equal 4. If the source of mathematical truth were deceptive, its outputs could not reliably be non-deceptive. But mathematical truths are non-deceptive. Therefore the source must be non-deceptive.

Critical Transition — From Logic to Morality

A11 is the keystone of this entire argument. Being non-deceptive is a moral property. Truthfulness is a virtue; deception is a vice. This is not a contested philosophical claim—it is a cultural and ethical universal. Deception is wrong in every moral framework that has ever existed.

By A11, the ground of mathematical truth must be non-deceptive. By the universality of the moral status of truthfulness, the ground must possess a moral virtue. You have derived a moral property from information-theoretic analysis of mathematical truth.

**Corollary 2:** The ground of mathematical truth is morally good—at least with respect to truthfulness.

### Level 4: Source Properties (A12–A15)

The ground of mathematical truth must share the properties of what it grounds, or it could not confer those properties. A source cannot confer properties it does not possess. A local source cannot produce universal output. A temporal source cannot produce eternal output. A material source cannot produce immaterial output. An incoherent source cannot produce coherent output.

A12 — Source Universality

The source of universal truth must itself be universal.

A13 — Source Eternality

The source of eternal truth must itself be eternal.

A14 — Source Immateriality

The source of immaterial truth must itself be immaterial.

A15 — Source Coherence

The source of coherent truth must itself be coherent.

### Level 5: The Moral Dimension (A16–A18)

A16 — Truth as Value

Truth is inherently valuable; falsehood is inherently disvaluable.

Even the relativist who claims "there is no objective truth" intends that statement to be objectively true. The value of truth is presupposed by every assertion, every argument, every inquiry.

A17 — Deception as Wrong

Deception is morally wrong.

This is a cultural universal. Every known moral system condemns deception. Even the liar must pretend truthfulness, implicitly acknowledging the normative force of truth.

A18 — Mathematical-Moral Unity

The source of mathematical truth and the source of moral truth are identical.

By A11, the ground of mathematical truth must be non-deceptive—a moral property. By parsimony (Occam's razor), we should not multiply entities beyond necessity. If the ground of mathematical truth has moral properties, it is more parsimonious to identify it with the ground of morality than to posit two separate grounds.

### Level 6: Identification (A19–A20)

A19 — The Logos

The ground of mathematical and moral truth is the Logos—a unified, rational, moral source.

The term "Logos" (\(\lambda\acute{o}\gamma o\varsigma\)) precisely captures what has been derived: rational structure (mathematical truth) unified with moral order. The term predates Christianity, appearing in Heraclitus, the Stoics, and Philo before its Christian appropriation.

A20 — The Identification

The Logos is functionally identical to the God of classical theism.

The Logos, as derived, possesses: necessary existence, eternality, universality (omnipresence), immateriality (spirituality), coherence (integrity), rationality, and moral goodness. This is the complete profile of the God of classical theism. Since the properties are identical, either they refer to the same entity, or there exist two entities with identical profiles—which violates the identity of indiscernibles.

## IV. The Is-Ought Bridge

Hume's guillotine claims that "ought" cannot be derived from "is"—that no amount of factual description can logically entail a normative prescription. This paper dissolves that problem by demonstrating that information theory is inherently normative.

### 4.1 Shannon's Channel Coding Theorem

Channel Coding Theorem
$$R < C \Rightarrow \exists \text{ code with } P_e \to 0$$

This theorem tells you what you *should* do: keep your transmission rate below channel capacity if you want reliable communication. It is a mathematical theorem that entails a prescription. The "ought" is built into the mathematics.

### 4.2 Kolmogorov Optimality

Kolmogorov Optimality
$$K(x) = \min\{|p| : U(p) = x\}$$

The definition of Kolmogorov complexity defines the *best* (shortest) description. "Best" is a normative term. The definition itself embeds an ought.

### The Dissolution

Information theory contains built-in "oughts": you ought to compress efficiently, transmit below capacity, minimize description length, and not deceive (produce divergence between signal and reality). These are not human conventions. They are mathematical necessities. The is-ought gap is bridged by the inherent normativity of information itself.

**Information is normative, and normativity is informational.**

**Sections I-III**
The paper builds the axiom chain from information-theoretic constraints rather than theological assumptions.

**Section IV**
The bridge appears when information theory turns out to contain built-in prescriptions about fidelity, compression, and truthfulness.

**What comes next**
The remaining sections pressure-test the chain, propose empirical hooks, and connect the formal derivation to human moral experience.

## V. Objections and Responses

### O1: The Platonic Objection

*Mathematical truths exist in a Platonic realm of abstract objects. They require no ground beyond their own abstract existence.*

The Platonic realm must answer to A8 (Sufficient Reason). Why does this realm exist rather than not? Positing abstract objects does not explain them. Moreover, Platonism faces the epistemological objection (Benacerraf 1973): how do concrete minds access abstract objects? This account provides that epistemic connection—human minds access mathematical truth because both are grounded in the same rational source.

### O2: The Fictionalist Challenge

*Mathematical statements are useful fictions, not literally true.*

Fictionalism cannot account for the applicability of mathematics. Sherlock Holmes cannot predict the trajectory of rockets or the behavior of electrons. If mathematical statements were fictions, their systematic applicability would be an inexplicable miracle. Moreover, the fictionalist must explain the constraints on mathematical fiction—why can't we consistently "make up" that \(2+2=5\)?

### O3: The Evolutionary Debunking Argument

*Our mathematical intuitions evolved for survival, not truth-tracking.*

Self-undermining. If our cognitive faculties are unreliable, then so is the reasoning that produced this objection. It saws off the branch it sits on.

### O4: The Naturalistic Objection

*Mathematics can be grounded in physical structures—in brains, computation, physical regularities.*

By A6, mathematical truth is immaterial. No physical structure can ground something that has no physical properties. By A2, mathematical truth predates all physical structures. No temporal physical entity can ground an eternal truth.

### O5: The Multiverse Objection

*Perhaps mathematical truths vary across universes.*

This equivocates between mathematical truth and physical law. Physical constants might vary; mathematical truths cannot. \(2+2=4\) is necessary (A3)—there is no possible world in which it is false.

### O6: The Conceivability Objection

*I can conceive of mathematical truths existing without a divine ground.*

Conceivability does not imply metaphysical possibility. We can conceive of water not being H₂O, but this is metaphysically impossible given the nature of water.

### O7: The "Which God?" Objection

*This only establishes the existence of a Logos, not the God of any specific religion.*

Correct as stated. This argument establishes properties. Which religion correctly identifies this ground is a further question. However, the Johannine identification of Jesus Christ with the Logos (John 1:1–14) is a direct claim that the specific entity derived here is the Christian God. See Book IV — The Key for the full analysis.

### O8: The Euthyphro Dilemma

False dilemma resolved by divine simplicity. Mathematical truths flow from God's nature—neither arbitrarily willed nor externally constraining. They are expressions of the divine Logos.

### O9: The Parsimony Objection

Occam's razor says not to multiply entities beyond necessity. This paper argues the ground is *necessary*. One unified ground is more parsimonious than separate, unrelated explanations.

### O10: The Coherence Objection

The coherence of the derived Ground is guaranteed by A7 and A15. Apparent paradoxes arise from informal formulations, not from the rigorously derived Logos.

## VI. Testable Predictions and Experimental Protocols

- P1 — Landauer Confirmation Confirmed Information erasure requires minimum energy \(E = k_B T \ln 2\). Status: CONFIRMED (Bérut et al., 2012).
- P2 — Measurement-Information Coupling Testable Quantum measurement energy scales with information gain: \(\Delta E = k_B T \cdot \Delta H\).
- P3 — Consciousness-Collapse Correlation Testable Conscious observation correlates with wavefunction collapse probability: \(P(\text{collapse}) = f(\Phi)\).
- P4 — Moral-Mathematical Neural Correlation Testable Brain regions active during mathematical cognition overlap with regions active during moral cognition.
- P5 — Coherence Amplification Supported Collective intentionality amplifies local coherence: \(\chi_{\text{collective}} = N^\alpha \cdot \chi_{\text{individual}}\), where \(\alpha > 1\). GCP data, 6σ deviations.
- P6 — Compression-Applicability Correlation Testable The applicability of a mathematical theory to physics correlates with its Kolmogorov complexity: lower \(K(\text{theory})\) implies higher applicability.

## VII. The Law Written on Hearts

Romans 2:15 states that Gentiles "show the work of the law written in their hearts." This paper provides a formal mechanism for this theological claim.

Let \(f : \text{Human} \to T_m\) denote the access function by which humans recognize mathematical truths. Let \(T_m \subset \text{Logos}\) denote the grounding relation established by this paper.

The Access Relation
$$f : \text{Human} \to T_m \wedge T_m \subset \text{Logos} \Rightarrow f : \text{Human} \to \text{Logos}$$

By transitivity, humans have direct cognitive access to the Logos through the mathematical faculty. This faculty is universal, pre-linguistic, non-arbitrary, and normative—exactly the properties of divinely inscribed moral law as described in the theological tradition.

## VIII. Conclusion

The Complete Argument — Formal Summary

$$\exists\, T_m : \square T_m \wedge \text{Universal}(T_m) \wedge \text{Eternal}(T_m) \wedge \text{Coherent}(T_m)$$

$$K(T_m \mid \text{Ground}) < K(T_m) \Rightarrow \exists\, \text{Ground}(T_m)$$

$$\text{Ground} \neq \emptyset \wedge \neg\text{Random}(\text{Ground}) \wedge \neg\text{Deceptive}(\text{Ground})$$

$$\neg\text{Deceptive} = \text{Truthful} = \text{Moral Property}$$

$$\therefore \text{Ground}(T_m) = \text{Moral}$$

$$f : \text{Human} \to T_m \wedge T_m \subset \text{Logos} \Rightarrow f : \text{Human} \to \text{Logos}$$

$$\text{Physics} = \text{Applied } T_m \Rightarrow \text{Physics is Moral}$$

$$\therefore \text{Universe is Moral Order} \quad \blacksquare$$

> "This most beautiful system of equations, constants, and laws, could only proceed from the counsel and dominion of a truthful and moral Being." — Adapted from Newton's Principia

## Appendix A: Complete Axiom Index

ID | Level | Statement | A1 | 1: Existence | Mathematical truths exist non-contingently | A2 | 1: Existence | Mathematical truths are temporally independent | A3 | 1: Existence | Mathematical truths are necessarily true | A4 | 2: Properties | Mathematical truth is universal (location-invariant) | A5 | 2: Properties | Mathematical truth is eternal (time-invariant) | A6 | 2: Properties | Mathematical truth is immaterial | A7 | 2: Properties | Mathematical truth is coherent | A8 | 3: Origin | Mathematical truth requires grounding | A9 | 3: Origin | The ground cannot be nothing | A10 | 3: Origin | The ground cannot be chaos | A11 | 3: Origin | The ground cannot be deceptive | A12 | 4: Source | The source of universal truth is universal | A13 | 4: Source | The source of eternal truth is eternal | A14 | 4: Source | The source of immaterial truth is immaterial | A15 | 4: Source | The source of coherent truth is coherent | A16 | 5: Moral | Truth is inherently valuable | A17 | 5: Moral | Deception is morally wrong | A18 | 5: Moral | Mathematical and moral truth share a common ground | A19 | 6: Identity | The ground is the Logos | A20 | 6: Identity | The Logos is functionally identical to God

## References

- Benacerraf, P. (1973). "Mathematical Truth." *The Journal of Philosophy*, 70(19), 661–679.
- Bérut, A., et al. (2012). "Experimental verification of Landauer's principle." *Nature*, 483(7388), 187–189.
- Chaitin, G. J. (1982). "Gödel's theorem and information." *International Journal of Theoretical Physics*, 21(12), 941–954.
- Field, H. (1980). *Science Without Numbers*. Princeton University Press.
- Gödel, K. (1931). "Über formal unentscheidbare Sätze." *Monatshefte für Mathematik und Physik*, 38(1), 173–198.
- Kolmogorov, A. N. (1965). "Three approaches to the quantitative definition of information." *Problems of Information Transmission*, 1(1), 1–7.
- Shannon, C. E. (1948). "A mathematical theory of communication." *Bell System Technical Journal*, 27(3), 379–423.
- Tononi, G. (2008). "Consciousness as integrated information." *The Biological Bulletin*, 215(3), 216–242.
- Wigner, E. P. (1960). "The unreasonable effectiveness of mathematics." *Communications on Pure and Applied Mathematics*, 13(1), 1–14.
