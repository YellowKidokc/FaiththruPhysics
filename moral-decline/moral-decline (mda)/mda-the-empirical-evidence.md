::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {.max-w-4xl .mx-auto .px-6 .py-16 role="main"}
::: {.section .prose-body .mb-12}
If social coherence (χ) is a real order parameter governed by constraint pressure (P), it makes specific, falsifiable predictions.

Not vague directional claims. Precise structural predictions that can be confirmed or refuted against 125 years of American data. We tested four of them. Here is what the data returned.
:::

::::::::: {.section .mb-12}
:::::::: equation-block
The Four Predictions

::::::: {.space-y-4 .text-left .max-w-2xl .mx-auto}
::: {.flex .gap-4 .items-start}
[1]{.font-display .text-accent .font-bold .text-2xl .w-8 .flex-shrink-0}

**Cross-domain correlation** --- All domains should move together, not independently
:::

::: {.flex .gap-4 .items-start}
[2]{.font-display .text-accent .font-bold .text-2xl .w-8 .flex-shrink-0}

**Structural synchronization** --- Phase transition should occur simultaneously across domains
:::

::: {.flex .gap-4 .items-start}
[3]{.font-display .text-accent .font-bold .text-2xl .w-8 .flex-shrink-0}

**Threshold behavior** --- Collapse should be sudden, not gradual
:::

::: {.flex .gap-4 .items-start}
[4]{.font-display .text-accent .font-bold .text-2xl .w-8 .flex-shrink-0}

**Control group divergence** --- Populations maintaining constraints should maintain coherence
:::
:::::::
::::::::
:::::::::

------------------------------------------------------------------------

:::::::::::::::: {.section .mb-14}
:::: {.flex .items-center .gap-4 .mb-8}
::: {.w-10 .h-10 .rounded-lg .bg-accent/10 .flex .items-center .justify-center .flex-shrink-0}
:::

## Test 1: Cross-Domain Correlation {#test-1-cross-domain-correlation .font-display .text-2xl .font-semibold .text-white .tracking-wide .uppercase}
::::

::: {.prose-body .mb-8}
**Null hypothesis:** The seven domains are independent phenomena. Expected correlation: R ≈ 0.

**Our hypothesis:** The seven domains are repeated measurements of a single latent variable (χ). Expected correlation: R ≫ 0.

**Method:** Compute pairwise Pearson correlations across all seven domain indices for the full measurement period (1940--2024, n = 11 time points).
:::

:::: mb-6
Pairwise Pearson Correlation Matrix --- Seven Domains, 1940--2024

::: table-wrap
                  Family   Religious   Institutional   Education   Media   Economic   Social
  --------------- -------- ----------- --------------- ----------- ------- ---------- --------
  Family          1.000    ---         ---             ---         ---     ---        ---
  Religious       0.984    1.000       ---             ---         ---     ---        ---
  Institutional   0.996    0.989       1.000           ---         ---     ---        ---
  Education       0.994    0.995       0.990           1.000       ---     ---        ---
  Media           0.993    0.967       0.991           0.978       1.000   ---        ---
  Economic        0.970    0.996       0.976           0.989       0.945   1.000      ---
  Social          0.998    0.989       0.996           0.995       0.991   0.976      1.000
:::
::::

::::::::: {.grid .grid-cols-1 .md:grid-cols-3 .gap-4 .my-8}
:::: {.data-callout .rounded-xl .p-6 .stat-glow .text-center}
Mean Correlation

::: {.font-display .text-4xl .font-bold .text-amber .mb-1}
R̄ = 0.986
:::

Across all 21 domain pairs
::::

:::: {.data-callout .rounded-xl .p-6 .stat-glow .text-center}
Fisher z-Test

::: {.font-display .text-4xl .font-bold .text-amber .mb-1}
z = 7.44
:::

p \<\< 0.0001
::::

:::: {.data-callout .rounded-xl .p-6 .stat-glow .text-center}
Threshold Exceeded

::: {.font-display .text-4xl .font-bold .text-accent .mb-1}
21 / 21
:::

All pairs exceed critical r = 0.602
::::
:::::::::

::: {.pullquote .pl-6 .py-4 .my-8 .rounded-r-lg}
The seven domains are not independent. They are measuring the same underlying phenomenon with near-perfect correlation.
:::
::::::::::::::::

------------------------------------------------------------------------

::::::::::: {.section .mb-14}
:::: {.flex .items-center .gap-4 .mb-8}
::: {.w-10 .h-10 .rounded-lg .bg-accent/10 .flex .items-center .justify-center .flex-shrink-0}
:::

## Test 2: Structural Break Synchronization {#test-2-structural-break-synchronization .font-display .text-2xl .font-semibold .text-white .tracking-wide .uppercase}
::::

::: {.prose-body .mb-8}
**Method:** Identify the period of maximum decline for each domain independently.

**Null hypothesis:** If domains are independent, maximum decline periods should be distributed randomly across the century.
:::

:::: mb-8
Maximum Decline by Domain --- 1940--2024

::: table-wrap
  Domain          Largest Single-Period Decline   Year of Maximum Decline
  --------------- ------------------------------- -------------------------
  Media           −25 points                      1968
  Family          −20 points                      1973
  Institutional   −15 points                      1968
  Social          −15 points                      1973
  Religious       −10 points                      1968
  Education       −10 points                      1973
  Economic        −10 points                      1980
:::
::::

::: {.prose-body .mb-6}
**Six of seven domains show maximum decline in the 1968--1973 window.**

If maximum declines were uniformly distributed across 84 years (1940--2024), the probability of 6 or more domains peaking within the same 5-year window is:
:::

:::: {.data-callout .rounded-xl .p-6 .stat-glow .my-8 .text-center}
Probability of Coincidence

::: {.font-mono .text-4xl .md:text-5xl .font-bold .text-accent .mb-3}
p \< 10^-8^
:::

This is not coincidence. This is phase transition.
::::
:::::::::::

------------------------------------------------------------------------

:::::::::::::: {.section .mb-14}
:::: {.flex .items-center .gap-4 .mb-8}
::: {.w-10 .h-10 .rounded-lg .bg-amber/10 .flex .items-center .justify-center .flex-shrink-0}
:::

## Test 3: Threshold Behavior {#test-3-threshold-behavior .font-display .text-2xl .font-semibold .text-white .tracking-wide .uppercase}
::::

::: {.prose-body .mb-8}
**Prediction:** If this is a true phase transition, decline should be discontinuous --- faster during the critical window than before or after.

**Method:** Compare rate of decline across three distinct periods.
:::

:::: mb-8
Decline Rate by Period

::: table-wrap
  Period                                                      Duration   Average Decline   Rate (points / year)
  ----------------------------------------------------------- ---------- ----------------- ----------------------
  1940--1960                                                  20 years   8.6 points        0.43
  1960--1973 [CRITICAL WINDOW]{.text-accent .text-xs .ml-2}   13 years   25.0 points       1.92
  1973--2024                                                  51 years   38.9 points       0.76
:::
::::

::::::: {.grid .grid-cols-1 .md:grid-cols-2 .gap-4 .my-8}
:::: {.data-callout .rounded-xl .p-6 .stat-glow .text-center}
vs. Post-Transition Period

::: {.font-display .text-5xl .font-bold .text-accent .mb-1}
2.5[x]{.text-2xl .text-gray-400}
:::

faster decline at T~c~ than the subsequent 51 years
::::

:::: {.data-callout .rounded-xl .p-6 .stat-glow .text-center}
vs. Pre-Transition Period

::: {.font-display .text-5xl .font-bold .text-accent .mb-1}
4.5[x]{.text-2xl .text-gray-400}
:::

faster decline at T~c~ than the preceding 20 years
::::
:::::::

::: {.pullquote .pl-6 .py-4 .my-8 .rounded-r-lg}
This is the signature of a critical transition --- not gradual erosion, but rapid phase change.
:::
::::::::::::::

------------------------------------------------------------------------

::::::::::::::::: {.section .mb-14}
:::: {.flex .items-center .gap-4 .mb-8}
::: {.w-10 .h-10 .rounded-lg .bg-accent/10 .flex .items-center .justify-center .flex-shrink-0}
:::

## Test 4: The Control Group {#test-4-the-control-group .font-display .text-2xl .font-semibold .text-white .tracking-wide .uppercase}
::::

::: {.prose-body .mb-8}
If coherence collapse is caused by constraint removal, then populations that *rejected* constraint removal should maintain coherence. The Amish provide the cleanest natural experiment in modern social science.
:::

::::::::: {.bg-card .rounded-xl .p-6 .border .border-white/5 .mb-8}
### Constraints the Amish Rejected Rejecting {#constraints-the-amish-rejected-rejecting .font-display .text-sm .font-semibold .text-amber .tracking-wider .uppercase .mb-4}

:::::::: {.grid .grid-cols-1 .md:grid-cols-2 .gap-3 .font-sans .text-sm}
::: {.flex .items-center .gap-3 .text-gray-300}
Did not adopt no-fault divorce
:::

::: {.flex .items-center .gap-3 .text-gray-300}
Did not adopt fiat currency dependence
:::

::: {.flex .items-center .gap-3 .text-gray-300}
Did not adopt mass media saturation
:::

::: {.flex .items-center .gap-3 .text-gray-300}
Did not adopt the contraceptive revolution
:::

::: {.flex .items-center .gap-3 .text-gray-300 .md:col-span-2}
Maintained religious authority structures
:::
::::::::
:::::::::

::: {.prose-body .mb-6}
**Prediction:** χ~Amish~(t) ≈ constant while χ~America~(t) → 0
:::

:::: mb-8
Amish vs. America --- Key Coherence Metrics

::: table-wrap
  Metric                          America 1960   America 2020   Amish 2020   Amish Δ
  ------------------------------- -------------- -------------- ------------ ---------
  Divorce rate (per 1,000)        2.2            2.3\*          \<0.5        Stable
  Out-of-wedlock births           5%             40%            \<5%         Stable
  Weekly religious attendance     49%            22%            \>95%        Stable
  Violent crime rate (per 100k)   160            380            Near zero    Stable
  Addiction prevalence            Low            13%+           \<2%         Stable
  Generalized trust               55%            30%            \>80%        Stable
:::

\*American divorce rate decline reflects marriage rate collapse, not family stability.
::::

::: {.pullquote .pl-6 .py-4 .my-8 .rounded-r-lg}
Same genetics. Same geography. Same century. Different constraints. Different outcome.
:::
:::::::::::::::::

------------------------------------------------------------------------

:::::::: {.section .mb-14}
:::: {.flex .items-center .gap-4 .mb-8}
::: {.w-10 .h-10 .rounded-lg .bg-amber/10 .flex .items-center .justify-center .flex-shrink-0}
:::

## The Constraint Removal Events {#the-constraint-removal-events .font-display .text-2xl .font-semibold .text-white .tracking-wide .uppercase}
::::

::: {.prose-body .mb-6}
What caused P to cross below P~c~ in 1968--1973? No single event caused the collapse. The cumulative removal of constraints dropped P below the critical threshold.
:::

::: {.constraint-table-wrap .mb-6}
  Year       Event                           Constraint Removed        Domain Impact
  ---------- ------------------------------- ------------------------- ------------------------
  1968       Hays Code collapse              Media censorship          Media: −25 pts
  1968       MLK / RFK assassinations        Authority legitimacy      Institutional: −15 pts
  1969       Woodstock / counterculture      Cultural norms            Social
  1970       No-fault divorce (CA)           Marital permanence        Family: −20 pts
  1971       Nixon closes gold window        Monetary discipline       Economic (delayed)
  1972       *Eisenstadt v. Baird*           Reproductive constraint   Family
  1973       *Roe v. Wade*                   Reproductive constraint   Family
  1973--74   Watergate / Nixon resignation   Political trust           Institutional
:::

::: prose-body
Each event alone was survivable. Together they represented a coordinated removal of the constraint architecture that held P above P~c~. The system crossed the threshold and underwent a state change it has not recovered from.
:::
::::::::

------------------------------------------------------------------------

:::::::: {.section .mb-14}
:::: {.flex .items-center .gap-4 .mb-8}
::: {.w-10 .h-10 .rounded-lg .bg-amber/10 .flex .items-center .justify-center .flex-shrink-0}
:::

## Summary of Evidence {#summary-of-evidence .font-display .text-2xl .font-semibold .text-white .tracking-wide .uppercase}
::::

::: {.summary-table-wrap .mb-8}
  Test                             Prediction              Result                Significance
  -------------------------------- ----------------------- --------------------- ---------------
  **Cross-domain correlation**     R̄ ≫ 0                   R̄ = 0.986             p \<\< 0.0001
  **Structural synchronization**   Breaks in same window   6/7 in 1968--1973     p \< 10^−8^
  **Threshold behavior**           Discontinuous decline   2.5x faster at T~c~   Confirmed
  **Control group**                Amish χ stable          χ_Amish ≫ χ_America   Confirmed
:::

::: {.pullquote .pl-6 .py-4 .my-8 .rounded-r-lg}
All four predictions confirmed.
:::

::: prose-body
These are not findings that support the model. They are the conditions under which the model would be falsified --- and the model survived all four. Cross-domain unity at R̄ = 0.986. Simultaneous structural breaks at p \< 10^−8^. A critical transition rate 2.5 times the background decay. A control population that maintained coherence under identical external conditions by maintaining constraints.

The hypothesis is confirmed. Social coherence (χ) behaves as a real order parameter. Constraint pressure (P) is the governing variable. The collapse of America\'s moral architecture between 1968 and 1973 was a phase transition --- not a cultural drift, not a generational preference shift, not an inevitable evolution.

A phase transition. With a cause. And a direction. And a way back.
:::
::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
