# Public Release and Test Protocol

## Purpose

This protocol records the release discipline for high-value Theophysics claims.

The goal is to create a public priority trail without overclaiming. Each major nugget is published before testing, then tested, then published again with the results.

This creates two timestamps:

1. The pre-test thesis timestamp.
2. The post-test result timestamp.

The first shows the idea existed before adversarial review.

The second shows the work was not protected from correction.

## Rule

For every major claim:

```text
Write it.
Commit/publish the pre-test version.
Test it.
Commit/publish the post-test result.
Preserve the failure notes.
```

No major claim should move directly from private draft to polished public certainty.

## Pre-Test Release

The pre-test release should include:

- the claim in its strongest clean form
- the formal shape, if available
- what the claim does not prove
- the first adversarial questions
- the planned test layer

The pre-test release should not include:

- inflated certainty
- hidden bridge assumptions
- "Lean proves God" language
- private source material that should remain held back
- unreviewed empirical claims stated as established facts

## Post-Test Release

The post-test release should include:

- what survived
- what failed
- what had to be narrowed
- what Lean actually proved, if formalized
- what remains historical, empirical, theological, or interpretive
- any new open gaps

The post-test release is stronger if it preserves the correction record.

## Why Two Releases

The first release establishes priority.

The second release establishes integrity.

Together they say:

> We had the idea before the test, and we let the test discipline the idea.

That is the right posture for Templeton-facing work.

## Wrongness Requirement

Every major release must deliberately include a section called one of:

- What Could Be Wrong
- What This Does Not Prove
- Adversarial Questions
- Failure Conditions

This is not weakness. It is the immune system.

If nothing could be wrong, the claim is probably being stated too vaguely.

## Current First Candidate

The first candidate for this protocol is:

```text
JURISDICTION_TEST_PRETEST.md
```

Pre-test thesis:

> Resurrection is not best framed as rule violation. It is a jurisdictional verdict: death has no rightful claim over the sinless one.

Planned test:

- formalize the jurisdiction structure
- distinguish death-as-biology from death-as-moral-jurisdiction
- reject false alternatives
- narrow any overclaim
- publish the post-test result

## Minimum Commit Message Pattern

Use this pattern when committing:

```text
pretest: publish jurisdiction test thesis
posttest: record jurisdiction test results
```

For other claims:

```text
pretest: publish <claim-name> thesis
posttest: record <claim-name> results
```

## Guardrail

The protocol does not require releasing everything.

It requires that whatever is released has a clear status.

Private synthesis can remain private.

Public nuggets should be narrow, timestamped, and testable.

