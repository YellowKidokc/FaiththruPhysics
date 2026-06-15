import {
  mysqlTable,
  mysqlEnum,
  serial,
  varchar,
  text,
  timestamp,
  decimal,
  bigint,
  int,
} from "drizzle-orm/mysql-core";

// ───────────────────────────────────────────
// Layer 1 — Case Management
// ───────────────────────────────────────────

export const cases = mysqlTable("cases", {
  id: serial("id").primaryKey(),
  caseId: varchar("case_id", { length: 50 }).notNull().unique(),
  canonicalTitle: varchar("canonical_title", { length: 255 }).notNull(),
  caseType: mysqlEnum("case_type", ["PHENOMENON", "CONSPIRACY", "EVENT", "PERSON", "ORGANIZATION", "TOPIC"]).default("PHENOMENON").notNull(),
  category: varchar("category", { length: 100 }),
  aliases: text("aliases"),
  status: mysqlEnum("status", ["DRAFT", "ACTIVE", "REVIEWING", "COMPLETED", "ARCHIVED"]).default("DRAFT").notNull(),
  oneSentenceVerdict: text("one_sentence_verdict"),
  ocsScore: decimal("ocs_score", { precision: 5, scale: 2 }),
  verdict: mysqlEnum("verdict", ["PROVEN", "PARTIALLY_PROVEN", "DISPUTED", "UNPROVEN", "DEBUNKED", "INSUFFICIENT_EVIDENCE"]),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
  notes: text("notes"),
});

export const caseRuns = mysqlTable("case_runs", {
  id: serial("id").primaryKey(),
  caseId: bigint("case_id", { mode: "number", unsigned: true }).notNull(),
  intent: mysqlEnum("intent", ["define_it", "aggregate_sources", "rip_site", "find_outgoing_links", "find_best_evidence", "build_timeline", "build_entity_map", "run_protocol"]).default("run_protocol").notNull(),
  sourceScope: mysqlEnum("source_scope", ["wikipedia_only", "trusted_hubs", "web_wide", "domain_specific", "archives_gov_legal", "mixed"]).default("trusted_hubs").notNull(),
  depth: mysqlEnum("depth", ["top_10", "top_25", "top_50", "one_hop", "two_hops", "deep_crawl"]).default("top_50").notNull(),
  outputType: mysqlEnum("output_type", ["link_list", "source_inventory", "ripped_pages", "entities", "timeline_events", "workbook", "notebook", "package_json"]).default("workbook").notNull(),
  orgMode: mysqlEnum("org_mode", ["by_case", "by_source_type", "by_date", "by_entity", "by_confidence", "by_domain"]).default("by_domain").notNull(),
  configJson: text("config_json"),
  startedAt: timestamp("started_at").defaultNow().notNull(),
  completedAt: timestamp("completed_at"),
  status: mysqlEnum("status", ["PENDING", "RUNNING", "COMPLETED", "FAILED"]).default("PENDING").notNull(),
});

// ───────────────────────────────────────────
// Layer 2 — Evidence Catalog
// ───────────────────────────────────────────

export const evidenceItems = mysqlTable("evidence_items", {
  id: serial("id").primaryKey(),
  caseId: bigint("case_id", { mode: "number", unsigned: true }).notNull(),
  domain: mysqlEnum("domain", [
    "MATERIAL_SCIENCE", "HEMATOLOGY", "PATHOLOGY", "BOTANICAL_GEOLOGICAL",
    "IMAGING_PHYSICS", "HISTORICAL_PROVENANCE", "DATING", "ART_HISTORICAL",
    "TESTIMONIAL", "DOCUMENTARY", "FORENSIC", "DIGITAL", "STATISTICAL", "OTHER"
  ]).notNull(),
  evidenceName: varchar("evidence_name", { length: 255 }).notNull(),
  tier: mysqlEnum("tier", ["T1", "T2", "T3", "T4", "T5"]).notNull(),
  tierDescription: text("tier_description"),
  source: varchar("source", { length: 500 }),
  sourceChainOfCustody: text("source_chain_of_custody"),
  whatItProves: text("what_it_proves"),
  weaknesses: text("weaknesses"),
  fabricationCost: mysqlEnum("fabrication_cost", ["EXTREME", "HIGH", "MODERATE", "LOW", "ZERO", "IMPOSSIBLE"]),
  fabricationCostDescription: text("fabrication_cost_description"),
  counterArguments: text("counter_arguments"),
  isDiscriminating: varchar("is_discriminating", { length: 10 }).default("true"),
  independenceVerified: varchar("independence_verified", { length: 10 }).default("true"),
  yearDiscovered: int("year_discovered"),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 3 — Timeline
// ───────────────────────────────────────────

export const timelineEvents = mysqlTable("timeline_events", {
  id: serial("id").primaryKey(),
  caseId: bigint("case_id", { mode: "number", unsigned: true }).notNull(),
  eventDate: varchar("event_date", { length: 50 }),
  datePrecision: mysqlEnum("date_precision", ["DAY", "MONTH", "YEAR", "DECADE", "CENTURY"]).default("YEAR").notNull(),
  eventDescription: text("event_description").notNull(),
  source: varchar("source", { length: 500 }),
  verificationStatus: mysqlEnum("verification_status", ["CONFIRMED", "PROBABLE", "DISPUTED", "UNVERIFIED", "DEBUNKED"]).default("CONFIRMED").notNull(),
  tier: mysqlEnum("tier", ["T1", "T2", "T3", "T4", "T5"]).default("T2").notNull(),
  entitiesInvolved: text("entities_involved"),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 4 — Fakery Matrix (Forced Inversion)
// ───────────────────────────────────────────

export const fakeryMatrixItems = mysqlTable("fakery_matrix_items", {
  id: serial("id").primaryKey(),
  caseId: bigint("case_id", { mode: "number", unsigned: true }).notNull(),
  constraintId: varchar("constraint_id", { length: 10 }).notNull(),
  constraintName: varchar("constraint_name", { length: 255 }).notNull(),
  description: text("description").notNull(),
  fabricationCost: mysqlEnum("fabrication_cost", ["EXTREME", "HIGH", "MODERATE", "LOW", "ZERO", "IMPOSSIBLE"]).notNull(),
  fabricationCostDescription: text("fabrication_cost_description"),
  possibilityScore: decimal("possibility_score", { precision: 10, scale: 9 }).default("1.0").notNull(),
  possibilityJustification: text("possibility_justification"),
  rating: mysqlEnum("rating", ["EXTREME", "HIGH", "MODERATE", "LOW", "ZERO", "IMPOSSIBLE"]).default("EXTREME").notNull(),
  sortOrder: int("sort_order").default(0).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 5 — Population Density Test
// ───────────────────────────────────────────

export const populationDensityItems = mysqlTable("population_density_items", {
  id: serial("id").primaryKey(),
  caseId: bigint("case_id", { mode: "number", unsigned: true }).notNull(),
  direction: mysqlEnum("direction", ["FORGERY", "CONSPIRACY", "AUTHENTICITY", "OTHER"]).notNull(),
  capability: varchar("capability", { length: 255 }).notNull(),
  locationRequired: varchar("location_required", { length: 255 }),
  eraRequired: varchar("era_required", { length: 255 }),
  densityScore: decimal("density_score", { precision: 10, scale: 9 }).default("0.0").notNull(),
  confidence: mysqlEnum("confidence", ["HIGH", "MEDIUM", "LOW"]).default("HIGH").notNull(),
  justification: text("justification"),
  populationEstimate: varchar("population_estimate", { length: 100 }),
  sortOrder: int("sort_order").default(0).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 6 — Soft Signals (14 signals)
// ───────────────────────────────────────────

export const softSignals = mysqlTable("soft_signals", {
  id: serial("id").primaryKey(),
  caseId: bigint("case_id", { mode: "number", unsigned: true }).notNull(),
  signalName: varchar("signal_name", { length: 100 }).notNull(),
  signalKey: varchar("signal_key", { length: 50 }).notNull(),
  description: text("description"),
  score: decimal("score", { precision: 4, scale: 2 }).default("0.0").notNull(),
  maxScore: decimal("max_score", { precision: 4, scale: 2 }).default("10.0").notNull(),
  justification: text("justification"),
  evidenceRefs: text("evidence_refs"),
  sortOrder: int("sort_order").default(0).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 7 — Protocol Steps
// ───────────────────────────────────────────

export const protocolSteps = mysqlTable("protocol_steps", {
  id: serial("id").primaryKey(),
  caseId: bigint("case_id", { mode: "number", unsigned: true }).notNull(),
  stepNumber: int("step_number").notNull(),
  stepName: varchar("step_name", { length: 100 }).notNull(),
  stepKey: varchar("step_key", { length: 50 }).notNull(),
  description: text("description"),
  status: mysqlEnum("status", ["PENDING", "IN_PROGRESS", "COMPLETED", "SKIPPED", "BLOCKED"]).default("PENDING").notNull(),
  findings: text("findings"),
  conclusion: text("conclusion"),
  completedAt: timestamp("completed_at"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 8 — Entities
// ───────────────────────────────────────────

export const entities = mysqlTable("entities", {
  id: serial("id").primaryKey(),
  caseId: bigint("case_id", { mode: "number", unsigned: true }).notNull(),
  entityName: varchar("entity_name", { length: 255 }).notNull(),
  entityType: mysqlEnum("entity_type", ["PERSON", "ORGANIZATION", "INSTITUTION", "PLACE", "EVENT", "ARTIFACT"]).notNull(),
  aliases: text("aliases"),
  knownFacts: text("known_facts"),
  disputedClaims: text("disputed_claims"),
  connections: text("connections"),
  tier: mysqlEnum("tier", ["T1", "T2", "T3", "T4", "T5"]).default("T2").notNull(),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 9 — Contradictions
// ───────────────────────────────────────────

export const contradictions = mysqlTable("contradictions", {
  id: serial("id").primaryKey(),
  caseId: bigint("case_id", { mode: "number", unsigned: true }).notNull(),
  contradictionType: mysqlEnum("contradiction_type", ["OFFICIAL_NARRATIVE", "INTERNAL", "SKEPTICAL", "EVIDENTIAL"]).notNull(),
  description: text("description").notNull(),
  positionA: text("position_a"),
  positionB: text("position_b"),
  severityScore: decimal("severity_score", { precision: 4, scale: 2 }).default("5.0").notNull(),
  resolution: text("resolution"),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// ───────────────────────────────────────────
// Layer 10 — Users (from auth)
// ───────────────────────────────────────────

export const users = mysqlTable("users", {
  id: serial("id").primaryKey(),
  unionId: varchar("unionId", { length: 255 }).notNull().unique(),
  name: varchar("name", { length: 255 }),
  email: varchar("email", { length: 320 }),
  avatar: text("avatar"),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().notNull().$onUpdate(() => new Date()),
  lastSignInAt: timestamp("lastSignInAt").defaultNow().notNull(),
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
