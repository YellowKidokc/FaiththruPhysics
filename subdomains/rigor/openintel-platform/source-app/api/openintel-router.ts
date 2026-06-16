import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import {
  cases,
  evidenceItems,
  timelineEvents,
  fakeryMatrixItems,
  populationDensityItems,
  softSignals,
  protocolSteps,
  entities,
  contradictions,
} from "@db/schema";
import { eq, asc } from "drizzle-orm";

export const openintelRouter = createRouter({
  // ───────────────────────────────────────────
  // CASES
  // ───────────────────────────────────────────

  caseCreate: publicQuery
    .input(z.object({
      caseId: z.string().min(1),
      canonicalTitle: z.string().min(1),
      caseType: z.enum(["PHENOMENON", "CONSPIRACY", "EVENT", "PERSON", "ORGANIZATION", "TOPIC"]).default("PHENOMENON"),
      category: z.string().optional(),
      aliases: z.string().optional(),
      notes: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const [newCase] = await db.insert(cases).values({
        caseId: input.caseId,
        canonicalTitle: input.canonicalTitle,
        caseType: input.caseType,
        category: input.category,
        aliases: input.aliases,
        notes: input.notes,
      }).returning({ id: cases.id });
      return newCase;
    }),

  caseList: publicQuery.query(async ({ ctx }) => {
    const db = getDb(ctx.env);
    return db.select().from(cases).orderBy(cases.createdAt);
  }),

  caseGetById: publicQuery
    .input(z.object({ id: z.number() }))
    .query(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const results = await db.select().from(cases).where(eq(cases.id, input.id));
      return results[0] ?? null;
    }),

  caseGetByCaseId: publicQuery
    .input(z.object({ caseId: z.string() }))
    .query(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const results = await db.select().from(cases).where(eq(cases.caseId, input.caseId));
      return results[0] ?? null;
    }),

  caseUpdate: publicQuery
    .input(z.object({
      id: z.number(),
      canonicalTitle: z.string().optional(),
      status: z.enum(["DRAFT", "ACTIVE", "REVIEWING", "COMPLETED", "ARCHIVED"]).optional(),
      oneSentenceVerdict: z.string().optional(),
      ocsScore: z.string().optional(),
      verdict: z.enum(["PROVEN", "PARTIALLY_PROVEN", "DISPUTED", "UNPROVEN", "DEBUNKED", "INSUFFICIENT_EVIDENCE"]).optional(),
      notes: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const { id, ...data } = input;
      await db.update(cases).set(data).where(eq(cases.id, id));
      return { success: true };
    }),

  // ───────────────────────────────────────────
  // EVIDENCE ITEMS
  // ───────────────────────────────────────────

  evidenceCreate: publicQuery
    .input(z.object({
      caseId: z.number(),
      domain: z.enum([
        "MATERIAL_SCIENCE", "HEMATOLOGY", "PATHOLOGY", "BOTANICAL_GEOLOGICAL",
        "IMAGING_PHYSICS", "HISTORICAL_PROVENANCE", "DATING", "ART_HISTORICAL",
        "TESTIMONIAL", "DOCUMENTARY", "FORENSIC", "DIGITAL", "STATISTICAL", "OTHER"
      ]),
      evidenceName: z.string().min(1),
      tier: z.enum(["T1", "T2", "T3", "T4", "T5"]),
      tierDescription: z.string().optional(),
      source: z.string().optional(),
      sourceChainOfCustody: z.string().optional(),
      whatItProves: z.string().optional(),
      weaknesses: z.string().optional(),
      fabricationCost: z.enum(["EXTREME", "HIGH", "MODERATE", "LOW", "ZERO", "IMPOSSIBLE"]).optional(),
      fabricationCostDescription: z.string().optional(),
      counterArguments: z.string().optional(),
      isDiscriminating: z.string().default("true"),
      independenceVerified: z.string().default("true"),
      yearDiscovered: z.number().optional(),
      notes: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const [item] = await db.insert(evidenceItems).values(input).returning({ id: evidenceItems.id });
      return item;
    }),

  evidenceListByCase: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      return db.select().from(evidenceItems)
        .where(eq(evidenceItems.caseId, input.caseId))
        .orderBy(evidenceItems.domain, evidenceItems.tier);
    }),

  evidenceDelete: publicQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      await db.delete(evidenceItems).where(eq(evidenceItems.id, input.id));
      return { success: true };
    }),

  // ───────────────────────────────────────────
  // TIMELINE EVENTS
  // ───────────────────────────────────────────

  timelineCreate: publicQuery
    .input(z.object({
      caseId: z.number(),
      eventDate: z.string().optional(),
      datePrecision: z.enum(["DAY", "MONTH", "YEAR", "DECADE", "CENTURY"]).default("YEAR"),
      eventDescription: z.string().min(1),
      source: z.string().optional(),
      verificationStatus: z.enum(["CONFIRMED", "PROBABLE", "DISPUTED", "UNVERIFIED", "DEBUNKED"]).default("CONFIRMED"),
      tier: z.enum(["T1", "T2", "T3", "T4", "T5"]).default("T2"),
      entitiesInvolved: z.string().optional(),
      notes: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const [item] = await db.insert(timelineEvents).values(input).returning({ id: timelineEvents.id });
      return item;
    }),

  timelineListByCase: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      return db.select().from(timelineEvents)
        .where(eq(timelineEvents.caseId, input.caseId))
        .orderBy(asc(timelineEvents.eventDate));
    }),

  // ───────────────────────────────────────────
  // FAKERY MATRIX ITEMS
  // ───────────────────────────────────────────

  fakeryCreate: publicQuery
    .input(z.object({
      caseId: z.number(),
      constraintId: z.string().min(1),
      constraintName: z.string().min(1),
      description: z.string().min(1),
      fabricationCost: z.enum(["EXTREME", "HIGH", "MODERATE", "LOW", "ZERO", "IMPOSSIBLE"]),
      fabricationCostDescription: z.string().optional(),
      possibilityScore: z.string().default("1.0"),
      possibilityJustification: z.string().optional(),
      rating: z.enum(["EXTREME", "HIGH", "MODERATE", "LOW", "ZERO", "IMPOSSIBLE"]).default("EXTREME"),
      sortOrder: z.number().default(0),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const [item] = await db.insert(fakeryMatrixItems).values(input).returning({ id: fakeryMatrixItems.id });
      return item;
    }),

  fakeryListByCase: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      return db.select().from(fakeryMatrixItems)
        .where(eq(fakeryMatrixItems.caseId, input.caseId))
        .orderBy(asc(fakeryMatrixItems.sortOrder));
    }),

  fakeryUpdateScore: publicQuery
    .input(z.object({
      id: z.number(),
      possibilityScore: z.string(),
      rating: z.enum(["EXTREME", "HIGH", "MODERATE", "LOW", "ZERO", "IMPOSSIBLE"]),
      possibilityJustification: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const { id, ...data } = input;
      await db.update(fakeryMatrixItems).set(data).where(eq(fakeryMatrixItems.id, id));
      return { success: true };
    }),

  // ───────────────────────────────────────────
  // POPULATION DENSITY ITEMS
  // ───────────────────────────────────────────

  popDensityCreate: publicQuery
    .input(z.object({
      caseId: z.number(),
      direction: z.enum(["FORGERY", "CONSPIRACY", "AUTHENTICITY", "OTHER"]),
      capability: z.string().min(1),
      locationRequired: z.string().optional(),
      eraRequired: z.string().optional(),
      densityScore: z.string().default("0.0"),
      confidence: z.enum(["HIGH", "MEDIUM", "LOW"]).default("HIGH"),
      justification: z.string().optional(),
      populationEstimate: z.string().optional(),
      sortOrder: z.number().default(0),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const [item] = await db.insert(populationDensityItems).values(input).returning({ id: populationDensityItems.id });
      return item;
    }),

  popDensityListByCase: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      return db.select().from(populationDensityItems)
        .where(eq(populationDensityItems.caseId, input.caseId))
        .orderBy(asc(populationDensityItems.sortOrder));
    }),

  popDensityUpdateScore: publicQuery
    .input(z.object({
      id: z.number(),
      densityScore: z.string(),
      confidence: z.enum(["HIGH", "MEDIUM", "LOW"]).optional(),
      justification: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const { id, ...data } = input;
      await db.update(populationDensityItems).set(data).where(eq(populationDensityItems.id, id));
      return { success: true };
    }),

  // ───────────────────────────────────────────
  // SOFT SIGNALS
  // ───────────────────────────────────────────

  signalCreate: publicQuery
    .input(z.object({
      caseId: z.number(),
      signalName: z.string().min(1),
      signalKey: z.string().min(1),
      description: z.string().optional(),
      score: z.string().default("0.0"),
      maxScore: z.string().default("10.0"),
      justification: z.string().optional(),
      evidenceRefs: z.string().optional(),
      sortOrder: z.number().default(0),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const [item] = await db.insert(softSignals).values(input).returning({ id: softSignals.id });
      return item;
    }),

  signalListByCase: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      return db.select().from(softSignals)
        .where(eq(softSignals.caseId, input.caseId))
        .orderBy(asc(softSignals.sortOrder));
    }),

  signalUpdateScore: publicQuery
    .input(z.object({
      id: z.number(),
      score: z.string(),
      justification: z.string().optional(),
      evidenceRefs: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const { id, ...data } = input;
      await db.update(softSignals).set(data).where(eq(softSignals.id, id));
      return { success: true };
    }),

  // ───────────────────────────────────────────
  // PROTOCOL STEPS
  // ───────────────────────────────────────────

  stepCreate: publicQuery
    .input(z.object({
      caseId: z.number(),
      stepNumber: z.number().min(1).max(10),
      stepName: z.string().min(1),
      stepKey: z.string().min(1),
      description: z.string().optional(),
      status: z.enum(["PENDING", "IN_PROGRESS", "COMPLETED", "SKIPPED", "BLOCKED"]).default("PENDING"),
      findings: z.string().optional(),
      conclusion: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const [item] = await db.insert(protocolSteps).values(input).returning({ id: protocolSteps.id });
      return item;
    }),

  stepListByCase: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      return db.select().from(protocolSteps)
        .where(eq(protocolSteps.caseId, input.caseId))
        .orderBy(asc(protocolSteps.stepNumber));
    }),

  stepUpdateStatus: publicQuery
    .input(z.object({
      id: z.number(),
      status: z.enum(["PENDING", "IN_PROGRESS", "COMPLETED", "SKIPPED", "BLOCKED"]),
      findings: z.string().optional(),
      conclusion: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const { id, ...data } = input;
      await db.update(protocolSteps).set(data).where(eq(protocolSteps.id, id));
      return { success: true };
    }),

  // ───────────────────────────────────────────
  // ENTITIES
  // ───────────────────────────────────────────

  entityCreate: publicQuery
    .input(z.object({
      caseId: z.number(),
      entityName: z.string().min(1),
      entityType: z.enum(["PERSON", "ORGANIZATION", "INSTITUTION", "PLACE", "EVENT", "ARTIFACT"]),
      aliases: z.string().optional(),
      knownFacts: z.string().optional(),
      disputedClaims: z.string().optional(),
      connections: z.string().optional(),
      tier: z.enum(["T1", "T2", "T3", "T4", "T5"]).default("T2"),
      notes: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const [item] = await db.insert(entities).values(input).returning({ id: entities.id });
      return item;
    }),

  entityListByCase: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      return db.select().from(entities)
        .where(eq(entities.caseId, input.caseId))
        .orderBy(entities.entityType, entities.entityName);
    }),

  // ───────────────────────────────────────────
  // CONTRADICTIONS
  // ───────────────────────────────────────────

  contradictionCreate: publicQuery
    .input(z.object({
      caseId: z.number(),
      contradictionType: z.enum(["OFFICIAL_NARRATIVE", "INTERNAL", "SKEPTICAL", "EVIDENTIAL"]),
      description: z.string().min(1),
      positionA: z.string().optional(),
      positionB: z.string().optional(),
      severityScore: z.string().default("5.0"),
      resolution: z.string().optional(),
      notes: z.string().optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const [item] = await db.insert(contradictions).values(input).returning({ id: contradictions.id });
      return item;
    }),

  contradictionListByCase: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      return db.select().from(contradictions)
        .where(eq(contradictions.caseId, input.caseId))
        .orderBy(asc(contradictions.severityScore));
    }),

  // ───────────────────────────────────────────
  // FULL CASE DATA (for verdict page)
  // ───────────────────────────────────────────

  getFullCase: publicQuery
    .input(z.object({ caseId: z.number() }))
    .query(async ({ input, ctx }) => {
      const db = getDb(ctx.env);
      const [caseData] = await db.select().from(cases).where(eq(cases.id, input.caseId));
      if (!caseData) return null;

      const evidence = await db.select().from(evidenceItems).where(eq(evidenceItems.caseId, input.caseId)).orderBy(evidenceItems.domain);
      const timeline = await db.select().from(timelineEvents).where(eq(timelineEvents.caseId, input.caseId)).orderBy(asc(timelineEvents.eventDate));
      const fakery = await db.select().from(fakeryMatrixItems).where(eq(fakeryMatrixItems.caseId, input.caseId)).orderBy(asc(fakeryMatrixItems.sortOrder));
      const popDensity = await db.select().from(populationDensityItems).where(eq(populationDensityItems.caseId, input.caseId)).orderBy(asc(populationDensityItems.sortOrder));
      const signals = await db.select().from(softSignals).where(eq(softSignals.caseId, input.caseId)).orderBy(asc(softSignals.sortOrder));
      const steps = await db.select().from(protocolSteps).where(eq(protocolSteps.caseId, input.caseId)).orderBy(asc(protocolSteps.stepNumber));
      const caseEntities = await db.select().from(entities).where(eq(entities.caseId, input.caseId));
      const caseContradictions = await db.select().from(contradictions).where(eq(contradictions.caseId, input.caseId));

      return {
        case: caseData,
        evidence,
        timeline,
        fakeryMatrix: fakery,
        populationDensity: popDensity,
        softSignals: signals,
        protocolSteps: steps,
        entities: caseEntities,
        contradictions: caseContradictions,
      };
    }),
});
