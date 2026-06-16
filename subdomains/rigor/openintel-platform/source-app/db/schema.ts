import {
  sqliteTable,
  integer,
  text,
} from "drizzle-orm/sqlite-core";

// ───────────────────────────────────────────
// Layer 1 — Case Management
// ───────────────────────────────────────────

export const cases = sqliteTable("cases", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  caseId: text("case_id").notNull().unique(),
  canonicalTitle: text("canonical_title").notNull(),
  caseType: text("case_type").notNull().default("PHENOMENON"),
  category: text("category"),
  aliases: text("aliases"),
  status: text("status").notNull().default("DRAFT"),
  oneSentenceVerdict: text("one_sentence_verdict"),
  ocsScore: text("ocs_score"),
  verdict: text("verdict"),
  createdAt: integer("created_at", { mode: "timestamp" }).defaultNow().notNull(),
  updatedAt: integer("updated_at", { mode: "timestamp" }).defaultNow().notNull().$onUpdate(() => new Date()),
  notes: text("notes"),
});

export const caseRuns = sqliteTable("case_runs", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  caseId: integer("case_id", { mode: "number" }).notNull(),
  intent: text("intent").notNull().default("run_protocol"),
  sourceScope: text("source_scope").notNull().default("trusted_hubs"),
  depth: text("depth").notNull().default("top_50"),
  outputType: text("output_type").notNull().default("workbook"),
  orgMode: text("org_mode").notNull().default("by_domain"),
  configJson: text("config_json"),
  startedAt: integer("started_at", { mode: "timestamp" }).defaultNow().notNull(),
  completedAt: integer("completed_at", { mode: "timestamp" }),
  status: text("status").notNull().default("PENDING"),
});

// ───────────────────────────────────────────
// Layer 2 — Evidence Catalog
// ───────────────────────────────────────────

export const evidenceItems = sqliteTable("evidence_items", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  caseId: integer("case_id", { mode: "number" }).notNull(),
  domain: text("domain").notNull(),
  evidenceName: text("evidence_name").notNull(),
  tier: text("tier").notNull(),
  tierDescription: text("tier_description"),
  source: text("source"),
  sourceChainOfCustody: text("source_chain_of_custody"),
  whatItProves: text("what_it_proves"),
  weaknesses: text("weaknesses"),
  fabricationCost: text("fabrication_cost"),
  fabricationCostDescription: text("fabrication_cost_description"),
  counterArguments: text("counter_arguments"),
  isDiscriminating: text("is_discriminating").default("true"),
  independenceVerified: text("independence_verified").default("true"),
  yearDiscovered: integer("year_discovered", { mode: "number" }),
  notes: text("notes"),
  createdAt: integer("created_at", { mode: "timestamp" }).defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 3 — Timeline
// ───────────────────────────────────────────

export const timelineEvents = sqliteTable("timeline_events", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  caseId: integer("case_id", { mode: "number" }).notNull(),
  eventDate: text("event_date"),
  datePrecision: text("date_precision").notNull().default("YEAR"),
  eventDescription: text("event_description").notNull(),
  source: text("source"),
  verificationStatus: text("verification_status").notNull().default("CONFIRMED"),
  tier: text("tier").notNull().default("T2"),
  entitiesInvolved: text("entities_involved"),
  notes: text("notes"),
  createdAt: integer("created_at", { mode: "timestamp" }).defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 4 — Fakery Matrix (Forced Inversion)
// ───────────────────────────────────────────

export const fakeryMatrixItems = sqliteTable("fakery_matrix_items", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  caseId: integer("case_id", { mode: "number" }).notNull(),
  constraintId: text("constraint_id").notNull(),
  constraintName: text("constraint_name").notNull(),
  description: text("description").notNull(),
  fabricationCost: text("fabrication_cost").notNull(),
  fabricationCostDescription: text("fabrication_cost_description"),
  possibilityScore: text("possibility_score").notNull().default("1.0"),
  possibilityJustification: text("possibility_justification"),
  rating: text("rating").notNull().default("EXTREME"),
  sortOrder: integer("sort_order", { mode: "number" }).default(0).notNull(),
  createdAt: integer("created_at", { mode: "timestamp" }).defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 5 — Population Density Test
// ───────────────────────────────────────────

export const populationDensityItems = sqliteTable("population_density_items", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  caseId: integer("case_id", { mode: "number" }).notNull(),
  direction: text("direction").notNull(),
  capability: text("capability").notNull(),
  locationRequired: text("location_required"),
  eraRequired: text("era_required"),
  densityScore: text("density_score").notNull().default("0.0"),
  confidence: text("confidence").notNull().default("HIGH"),
  justification: text("justification"),
  populationEstimate: text("population_estimate"),
  sortOrder: integer("sort_order", { mode: "number" }).default(0).notNull(),
  createdAt: integer("created_at", { mode: "timestamp" }).defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 6 — Soft Signals (14 signals)
// ───────────────────────────────────────────

export const softSignals = sqliteTable("soft_signals", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  caseId: integer("case_id", { mode: "number" }).notNull(),
  signalName: text("signal_name").notNull(),
  signalKey: text("signal_key").notNull(),
  description: text("description"),
  score: text("score").notNull().default("0.0"),
  maxScore: text("max_score").notNull().default("10.0"),
  justification: text("justification"),
  evidenceRefs: text("evidence_refs"),
  sortOrder: integer("sort_order", { mode: "number" }).default(0).notNull(),
  createdAt: integer("created_at", { mode: "timestamp" }).defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 7 — Protocol Steps
// ───────────────────────────────────────────

export const protocolSteps = sqliteTable("protocol_steps", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  caseId: integer("case_id", { mode: "number" }).notNull(),
  stepNumber: integer("step_number", { mode: "number" }).notNull(),
  stepName: text("step_name").notNull(),
  stepKey: text("step_key").notNull(),
  description: text("description"),
  status: text("status").notNull().default("PENDING"),
  findings: text("findings"),
  conclusion: text("conclusion"),
  completedAt: integer("completed_at", { mode: "timestamp" }),
  createdAt: integer("created_at", { mode: "timestamp" }).defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 8 — Entities
// ───────────────────────────────────────────

export const entities = sqliteTable("entities", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  caseId: integer("case_id", { mode: "number" }).notNull(),
  entityName: text("entity_name").notNull(),
  entityType: text("entity_type").notNull(),
  aliases: text("aliases"),
  knownFacts: text("known_facts"),
  disputedClaims: text("disputed_claims"),
  connections: text("connections"),
  tier: text("tier").notNull().default("T2"),
  notes: text("notes"),
  createdAt: integer("created_at", { mode: "timestamp" }).defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 9 — Contradictions
// ───────────────────────────────────────────

export const contradictions = sqliteTable("contradictions", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  caseId: integer("case_id", { mode: "number" }).notNull(),
  contradictionType: text("contradiction_type").notNull(),
  description: text("description").notNull(),
  positionA: text("position_a"),
  positionB: text("position_b"),
  severityScore: text("severity_score").notNull().default("5.0"),
  resolution: text("resolution"),
  notes: text("notes"),
  createdAt: integer("created_at", { mode: "timestamp" }).defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 10 — Users (from auth)
// ───────────────────────────────────────────

export const users = sqliteTable("users", {
  id: integer("id", { mode: "number" }).primaryKey({ autoIncrement: true }),
  unionId: text("unionId").notNull().unique(),
  name: text("name"),
  email: text("email"),
  avatar: text("avatar"),
  role: text("role").notNull().default("user"),
  createdAt: integer("createdAt", { mode: "timestamp" }).defaultNow().notNull(),
  updatedAt: integer("updatedAt", { mode: "timestamp" }).defaultNow().notNull().$onUpdate(() => new Date()),
  lastSignInAt: integer("lastSignInAt", { mode: "timestamp" }).defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Type Exports
// ───────────────────────────────────────────

export type Case = typeof cases.$inferSelect;
export type InsertCase = typeof cases.$inferInsert;
export type CaseRun = typeof caseRuns.$inferSelect;
export type EvidenceItem = typeof evidenceItems.$inferSelect;
export type TimelineEvent = typeof timelineEvents.$inferSelect;
export type FakeryMatrixItem = typeof fakeryMatrixItems.$inferSelect;
export type PopulationDensityItem = typeof populationDensityItems.$inferSelect;
export type SoftSignal = typeof softSignals.$inferSelect;
export type ProtocolStep = typeof protocolSteps.$inferSelect;
export type Entity = typeof entities.$inferSelect;
export type Contradiction = typeof contradictions.$inferSelect;
export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;
