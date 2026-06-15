import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import {
  fakeryMatrixItems,
  populationDensityItems,
  softSignals,
  evidenceItems,
  contradictions,
  cases,
  timelineEvents,
} from "@db/schema";
import { eq } from "drizzle-orm";

// ───────────────────────────────────────────
// Scoring Engine
// ───────────────────────────────────────────

export const scoringRouter = createRouter({

  // ───────────────────────────────────────────
  // Fakery Matrix Compound Probability
  // ───────────────────────────────────────────

  computeFakeryCompound: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input }) => {
      const db = getDb();
      const items = await db.select().from(fakeryMatrixItems)
        .where(eq(fakeryMatrixItems.caseId, input.caseId))
        .orderBy(fakeryMatrixItems.sortOrder);

      if (items.length === 0) {
        return { compoundProbability: 1, probabilityString: "1", items: [], verdict: "NO_DATA" };
      }

      // Convert possibility scores to numbers and compute product
      let compound = 1;
      const ratings: Record<string, number> = {
        IMPOSSIBLE: 0,
        ZERO: 0,
        EXTREME: 0.01,
        HIGH: 0.05,
        MODERATE: 0.25,
        LOW: 0.5,
      };

      const scoredItems = items.map(item => {
        const score = parseFloat(item.possibilityScore);
        const ratingMultiplier = ratings[item.rating] ?? score;
        // Use the lower of the two (conservative)
        const finalScore = Math.min(score, ratingMultiplier);
        compound *= finalScore;
        return { ...item, effectiveScore: finalScore };
      });

      // Convert to human-readable
      let probabilityString: string;
      let verdict: string;

      if (compound === 0) {
        probabilityString = "0 (functionally impossible)";
        verdict = "FORGERY_IMPOSSIBLE";
      } else if (compound < 1e-20) {
        probabilityString = `< 1 in 10^${Math.abs(Math.floor(Math.log10(compound)))}`;
        verdict = "FORGERY_IMPOSSIBLE";
      } else if (compound < 1e-10) {
        probabilityString = `< 1 in 10 billion`;
        verdict = "FORGERY_EXTREMELY_UNLIKELY";
      } else if (compound < 0.001) {
        probabilityString = `< 1 in 1,000`;
        verdict = "FORGERY_HIGHLY_UNLIKELY";
      } else if (compound < 0.01) {
        probabilityString = `< 1 in 100`;
        verdict = "FORGERY_UNLIKELY";
      } else {
        probabilityString = `${(compound * 100).toFixed(4)}%`;
        verdict = "FORGERY_POSSIBLE";
      }

      return { compoundProbability: compound, probabilityString, items: scoredItems, verdict };
    }),

  // ───────────────────────────────────────────
  // Population Density Compound Probability
  // ───────────────────────────────────────────

  computePopDensityCompound: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input }) => {
      const db = getDb();
      const items = await db.select().from(populationDensityItems)
        .where(eq(populationDensityItems.caseId, input.caseId))
        .orderBy(populationDensityItems.sortOrder);

      if (items.length === 0) {
        return { compoundProbability: 0, probabilityString: "0", items: [], verdict: "NO_DATA" };
      }

      // For population density: product of all capability densities
      let compound = 1;
      const scoredItems = items.map(item => {
        const score = parseFloat(item.densityScore);
        compound *= score;
        return { ...item, effectiveScore: score };
      });

      let probabilityString: string;
      let verdict: string;

      if (compound === 0) {
        probabilityString = "ZERO (required population does not exist)";
        verdict = "POPULATION_ZERO";
      } else if (compound < 1e-15) {
        probabilityString = `< 1 in 10^${Math.abs(Math.floor(Math.log10(compound)))}`;
        verdict = "POPULATION_NEGLIGIBLE";
      } else if (compound < 0.01) {
        probabilityString = "Extremely low population density";
        verdict = "POPULATION_EXTREMELY_LOW";
      } else if (compound < 0.1) {
        probabilityString = "Low population density";
        verdict = "POPULATION_LOW";
      } else if (compound < 0.5) {
        probabilityString = "Moderate population density";
        verdict = "POPULATION_MODERATE";
      } else {
        probabilityString = "High population density";
        verdict = "POPULATION_HIGH";
      }

      return { compoundProbability: compound, probabilityString, items: scoredItems, verdict };
    }),

  // ───────────────────────────────────────────
  // Evidence Summary Stats
  // ───────────────────────────────────────────

  computeEvidenceStats: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input }) => {
      const db = getDb();
      const items = await db.select().from(evidenceItems)
        .where(eq(evidenceItems.caseId, input.caseId));

      const total = items.length;
      const t1Count = items.filter(i => i.tier === "T1").length;
      const t2Count = items.filter(i => i.tier === "T2").length;
      const t3Count = items.filter(i => i.tier === "T3").length;
      const t4Count = items.filter(i => i.tier === "T4").length;
      const t5Count = items.filter(i => i.tier === "T5").length;

      // Weighted score: T1=5, T2=4, T3=3, T4=2, T5=1
      const weights: Record<string, number> = { T1: 5, T2: 4, T3: 3, T4: 2, T5: 1 };
      const weightedScore = items.reduce((sum, i) => sum + (weights[i.tier] || 0), 0);
      const maxPossible = total * 5;
      const evidenceQuality = maxPossible > 0 ? weightedScore / maxPossible : 0;

      return {
        total,
        t1Count,
        t2Count,
        t3Count,
        t4Count,
        t5Count,
        weightedScore,
        evidenceQuality: parseFloat(evidenceQuality.toFixed(3)),
      };
    }),

  // ───────────────────────────────────────────
  // Soft Signals Aggregate
  // ───────────────────────────────────────────

  computeSoftSignalsAggregate: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input }) => {
      const db = getDb();
      const items = await db.select().from(softSignals)
        .where(eq(softSignals.caseId, input.caseId));

      const totalScore = items.reduce((sum, i) => sum + parseFloat(i.score), 0);
      const maxPossible = items.reduce((sum, i) => sum + parseFloat(i.maxScore), 0);
      const percentage = maxPossible > 0 ? totalScore / maxPossible : 0;

      return {
        signalCount: items.length,
        totalScore: parseFloat(totalScore.toFixed(2)),
        maxPossible: parseFloat(maxPossible.toFixed(2)),
        percentage: parseFloat((percentage * 100).toFixed(1)),
      };
    }),

  // ───────────────────────────────────────────
  // OCS (Overall Case Score)
  // ───────────────────────────────────────────

  computeOCS: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input }) => {
      const db = getDb();

      // Get evidence stats
      const evidence = await db.select().from(evidenceItems)
        .where(eq(evidenceItems.caseId, input.caseId));
      const weights: Record<string, number> = { T1: 5, T2: 4, T3: 3, T4: 2, T5: 1 };
      const weightedScore = evidence.reduce((sum, i) => sum + (weights[i.tier] || 0), 0);
      const evidenceQuality = evidence.length > 0 ? weightedScore / (evidence.length * 5) : 0;

      // Get fakery compound
      const fakeryItems = await db.select().from(fakeryMatrixItems)
        .where(eq(fakeryMatrixItems.caseId, input.caseId));
      let fakeryCompound = 1;
      fakeryItems.forEach(item => {
        fakeryCompound *= parseFloat(item.possibilityScore);
      });
      const fakeryScore = fakeryCompound === 0 ? 1 : Math.max(0, 1 - fakeryCompound * 100);

      // Get population density compound
      const popItems = await db.select().from(populationDensityItems)
        .where(eq(populationDensityItems.caseId, input.caseId));
      let popCompound = 1;
      popItems.forEach(item => {
        popCompound *= parseFloat(item.densityScore);
      });
      const popScore = popCompound === 0 ? 1 : Math.max(0, 1 - popCompound * 10);

      // Get soft signals
      const signals = await db.select().from(softSignals)
        .where(eq(softSignals.caseId, input.caseId));
      const totalSignalScore = signals.reduce((sum, i) => sum + parseFloat(i.score), 0);
      const maxSignalScore = signals.reduce((sum, i) => sum + parseFloat(i.maxScore), 0);
      const signalScore = maxSignalScore > 0 ? totalSignalScore / maxSignalScore : 0;

      // Get contradictions
      const contras = await db.select().from(contradictions)
        .where(eq(contradictions.caseId, input.caseId));
      const contradictionSeverity = contras.length > 0
        ? contras.reduce((sum, c) => sum + parseFloat(c.severityScore), 0) / contras.length / 10
        : 0;

      // OCS formula: weighted blend
      // E_qual (evidence quality) = 30%
      // F_score (fakery impossibility) = 25%
      // P_score (population density) = 20%
      // S_score (soft signals) = 15%
      // C_penalty (contradiction penalty) = 10%
      const ocs = (
        evidenceQuality * 0.30 +
        fakeryScore * 0.25 +
        popScore * 0.20 +
        signalScore * 0.15 -
        contradictionSeverity * 0.10
      );

      // Clamp to [0, 1]
      const finalOcs = Math.max(0, Math.min(1, ocs));

      // Determine verdict
      let verdict: string;
      let verdictLabel: string;
      if (finalOcs >= 0.85) {
        verdict = "PROVEN";
        verdictLabel = "Proven";
      } else if (finalOcs >= 0.65) {
        verdict = "PARTIALLY_PROVEN";
        verdictLabel = "Partially Proven";
      } else if (finalOcs >= 0.45) {
        verdict = "DISPUTED";
        verdictLabel = "Disputed";
      } else if (finalOcs >= 0.25) {
        verdict = "UNPROVEN";
        verdictLabel = "Unproven";
      } else {
        verdict = "DEBUNKED";
        verdictLabel = "Debunked / False";
      }

      return {
        ocs: parseFloat((finalOcs * 100).toFixed(2)),
        ocsRaw: parseFloat(finalOcs.toFixed(4)),
        verdict,
        verdictLabel,
        components: {
          evidenceQuality: parseFloat((evidenceQuality * 100).toFixed(2)),
          fakeryScore: parseFloat((fakeryScore * 100).toFixed(2)),
          popScore: parseFloat((popScore * 100).toFixed(2)),
          signalScore: parseFloat((signalScore * 100).toFixed(2)),
          contradictionPenalty: parseFloat((contradictionSeverity * 100).toFixed(2)),
        },
        weights: {
          evidenceQuality: 30,
          fakeryScore: 25,
          popScore: 20,
          signalScore: 15,
          contradictionPenalty: 10,
        },
      };
    }),

  // ───────────────────────────────────────────
  // SQL Export (INSERT statements)
  // ───────────────────────────────────────────

  generateSqlExport: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input }) => {
      const db = getDb();
      const fullCase = await db.select().from(cases).where(eq(cases.id, input.caseId));
      if (!fullCase[0]) return { sql: "-- Case not found" };

      const c = fullCase[0];
      let sql = `-- OpenIntel SQL Export for Case: ${c.canonicalTitle}\n`;
      sql += `-- Case ID: ${c.caseId}\n`;
      sql += `-- Generated: ${new Date().toISOString()}\n\n`;

      // Insert case
      sql += `-- Case\n`;
      sql += `INSERT INTO cases (case_id, canonical_title, case_type, category, status, one_sentence_verdict, ocs_score, verdict, notes) VALUES (`;
      sql += `'${c.caseId}', '${c.canonicalTitle}', '${c.caseType}', ${c.category ? `'${c.category}'` : 'NULL'}, `;
      sql += `'${c.status}', ${c.oneSentenceVerdict ? `'${c.oneSentenceVerdict}'` : 'NULL'}, `;
      sql += `${c.ocsScore ? c.ocsScore : 'NULL'}, ${c.verdict ? `'${c.verdict}'` : 'NULL'}, `;
      sql += `${c.notes ? `'${c.notes}'` : 'NULL'});\n\n`;

      // Get case numeric ID for FK references
      const caseNumericId = c.id;

      // Evidence
      const evidence = await db.select().from(evidenceItems).where(eq(evidenceItems.caseId, input.caseId));
      if (evidence.length > 0) {
        sql += `-- Evidence Items (${evidence.length})\n`;
        evidence.forEach(e => {
          sql += `INSERT INTO evidence_items (case_id, domain, evidence_name, tier, source, what_it_proves, fabrication_cost, is_discriminating) VALUES (`;
          sql += `${caseNumericId}, '${e.domain}', '${e.evidenceName.replace(/'/g, "''")}', '${e.tier}', `;
          sql += `${e.source ? `'${e.source.replace(/'/g, "''")}'` : 'NULL'}, `;
          sql += `${e.whatItProves ? `'${e.whatItProves.replace(/'/g, "''")}'` : 'NULL'}, `;
          sql += `${e.fabricationCost ? `'${e.fabricationCost}'` : 'NULL'}, '${e.isDiscriminating}');\n`;
        });
        sql += `\n`;
      }

      // Timeline
      const timeline = await db.select().from(timelineEvents).where(eq(timelineEvents.caseId, input.caseId));
      if (timeline.length > 0) {
        sql += `-- Timeline Events (${timeline.length})\n`;
        timeline.forEach(t => {
          sql += `INSERT INTO timeline_events (case_id, event_date, date_precision, event_description, source, verification_status, tier) VALUES (`;
          sql += `${caseNumericId}, ${t.eventDate ? `'${t.eventDate}'` : 'NULL'}, '${t.datePrecision}', `;
          sql += `'${t.eventDescription.replace(/'/g, "''")}', ${t.source ? `'${t.source.replace(/'/g, "''")}'` : 'NULL'}, `;
          sql += `'${t.verificationStatus}', '${t.tier}');\n`;
        });
        sql += `\n`;
      }

      // Fakery Matrix
      const fakery = await db.select().from(fakeryMatrixItems).where(eq(fakeryMatrixItems.caseId, input.caseId));
      if (fakery.length > 0) {
        sql += `-- Fakery Matrix Items (${fakery.length})\n`;
        fakery.forEach(f => {
          sql += `INSERT INTO fakery_matrix_items (case_id, constraint_id, constraint_name, description, fabrication_cost, possibility_score, rating) VALUES (`;
          sql += `${caseNumericId}, '${f.constraintId}', '${f.constraintName.replace(/'/g, "''")}', `;
          sql += `'${f.description.replace(/'/g, "''")}', '${f.fabricationCost}', ${f.possibilityScore}, '${f.rating}');\n`;
        });
        sql += `\n`;
      }

      // Population Density
      const popDensity = await db.select().from(populationDensityItems).where(eq(populationDensityItems.caseId, input.caseId));
      if (popDensity.length > 0) {
        sql += `-- Population Density Items (${popDensity.length})\n`;
        popDensity.forEach(p => {
          sql += `INSERT INTO population_density_items (case_id, direction, capability, location_required, era_required, density_score, confidence, justification) VALUES (`;
          sql += `${caseNumericId}, '${p.direction}', '${p.capability.replace(/'/g, "''")}', `;
          sql += `${p.locationRequired ? `'${p.locationRequired}'` : 'NULL'}, `;
          sql += `${p.eraRequired ? `'${p.eraRequired}'` : 'NULL'}, ${p.densityScore}, '${p.confidence}', `;
          sql += `${p.justification ? `'${p.justification.replace(/'/g, "''")}'` : 'NULL'});\n`;
        });
        sql += `\n`;
      }

      // Soft Signals
      const signals = await db.select().from(softSignals).where(eq(softSignals.caseId, input.caseId));
      if (signals.length > 0) {
        sql += `-- Soft Signals (${signals.length})\n`;
        signals.forEach(s => {
          sql += `INSERT INTO soft_signals (case_id, signal_name, signal_key, score, max_score, justification) VALUES (`;
          sql += `${caseNumericId}, '${s.signalName.replace(/'/g, "''")}', '${s.signalKey}', ${s.score}, ${s.maxScore}, `;
          sql += `${s.justification ? `'${s.justification.replace(/'/g, "''")}'` : 'NULL'});\n`;
        });
        sql += `\n`;
      }

      sql += `-- End of export\n`;

      return { sql };
    }),
});
