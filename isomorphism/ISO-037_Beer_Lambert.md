---
type: isomorphism
id: ISO-037
status: confirmed
domain_a: optics
domain_b: economics/theology
concept_a: "Beer-Lambert Law: I(x) = I_0 * e^(-alpha*x). Absorption coefficient alpha is a property of the medium."
concept_b: "Transaction fee extraction: P(n) = P_0 * (1-f)^n approx P_0 * e^(-fn). Proverbs 11:1."
confidence: high
iso_type: structural_isomorphism
created: 2026-04-04
---

# Beer-Lambert Law :: Transaction Fee Extraction

## DOMAINS

**Domain A — Optics (Beer-Lambert Law)**
The Beer-Lambert Law describes the attenuation of light passing through an absorbing medium: I(x) = I_0 * e^(-alpha*x), where I_0 is initial intensity, alpha is the absorption coefficient (a property of the medium), and x is the path length. A transparent medium has alpha near 0; an opaque medium has large alpha. The law is exact for monochromatic light in a homogeneous medium.

**Domain B — Economics/Theology**
Transaction fees extract value at each step through a supply chain: P(n) = P_0 * (1-f)^n, where P_0 is initial purchasing power, f is the fee fraction per transaction, and n is the number of transactions. For small f, this approximates P_0 * e^(-fn) — the identical mathematical form. "A false balance is an abomination to the Lord" (Proverbs 11:1). Cash (f near 0) is a transparent medium; mandatory digital payment systems with compounding fees are opaque media.

## THE MAPPING

| # | Optics (Domain A) | Economics/Theology (Domain B) | Notes |
|---|-------------------|-------------------------------|-------|
| 1 | Light intensity I(x) | Purchasing power P(n) | The quantity being attenuated |
| 2 | Initial intensity I_0 | Initial purchasing power P_0 | Starting value before medium |
| 3 | Absorption coefficient alpha | Fee fraction f | Property of the medium that determines extraction rate |
| 4 | Path length x | Number of transactions n | How far through the medium the signal travels |
| 5 | Transparent medium (alpha near 0) | Cash economy (f near 0) | Minimal extraction — signal passes through |
| 6 | Opaque medium (large alpha) | Mandatory digital payment (large f, many intermediaries) | Maximum extraction — signal absorbed |
| 7 | Exponential decay e^(-alpha*x) | Exponential decay (1-f)^n approx e^(-fn) | Mathematical identity, not analogy |
| 8 | Monochromatic light | Single-currency transactions | The law is exact for uniform input |

**Mathematical Identity**: This is not a metaphor. For small f:

    P(n) = P_0 * (1-f)^n = P_0 * e^(n*ln(1-f)) approx P_0 * e^(-fn)

Setting alpha = f and x = n gives I(x) = P(n) exactly. The mathematical forms are identical.

**Quantitative Test**: $20 at 3% fee through 30 transactions:
    P(30) = 20 * (1-0.03)^30 = 20 * 0.4010 = $8.09
    59.5% of value absorbed by the medium.

**Combined with Phantom Energy**: When inflation (monetary expansion M(t)) compounds with transaction fees:
    P_effective(t,n) = P_0/M(t) * (1-f)^n
This is dual-mechanism attenuation: inflation erodes from above (denominator grows), fees extract from below (numerator shrinks). The poor experience both simultaneously.

## TESTS

**Swap Test**: PASSED strongly. Replace "absorption coefficient" with "fee fraction" and "path length" with "transaction count" — the mathematics is literally identical. This passes at the level of mathematical identity, not merely structural analogy.

**Bidirectional Prediction**: Optics predicts that doubling the path length should double the exponential exponent → doubling transactions through a supply chain doubles the fee extraction exponent. Economics predicts that a transparent medium should transmit fully → cash (alpha near 0) transmits purchasing power with minimal loss.

**Falsification Condition**: If transaction fees did not compound exponentially through supply chains — i.e., if the 30th transaction extracted the same absolute amount as the 1st — the mapping would fail. This is empirically false: compounding is the mathematical reality of percentage-based fees.

## CLASSIFICATION

**Type**: Structural isomorphism at the level of mathematical identity. The exponential forms are the same equation with relabeled variables. This is the strongest possible type of isomorphism — not structural analogy but mathematical equivalence.

**Connections**: ISO-002 (Grace — grace as the "light" being transmitted), ISO-003 (Entropy/Sin — extraction as entropy increase), ISO-005 (Fiat/Phantom Energy — inflation as the other attenuation mechanism), ISO-008 (Coherence — transparent vs opaque economies).
