// Relations for OpenIntel schema tables
// Drizzle ORM relations for query optimization

import { relations } from "drizzle-orm/relations";
import {
  cases,
  caseRuns,
  evidenceItems,
  timelineEvents,
  fakeryMatrixItems,
  populationDensityItems,
  softSignals,
  protocolSteps,
  entities,
  contradictions,
} from "./schema";

export const casesRelations = relations(cases, ({ many }) => ({
  runs: many(caseRuns),
  evidence: many(evidenceItems),
  timeline: many(timelineEvents),
  fakeryMatrix: many(fakeryMatrixItems),
  populationDensity: many(populationDensityItems),
  softSignals: many(softSignals),
  protocolSteps: many(protocolSteps),
  entities: many(entities),
  contradictions: many(contradictions),
}));

export const caseRunsRelations = relations(caseRuns, ({ one }) => ({
  case: one(cases, { fields: [caseRuns.caseId], references: [cases.id] }),
}));

export const evidenceItemsRelations = relations(evidenceItems, ({ one }) => ({
  case: one(cases, { fields: [evidenceItems.caseId], references: [cases.id] }),
}));

export const timelineEventsRelations = relations(timelineEvents, ({ one }) => ({
  case: one(cases, { fields: [timelineEvents.caseId], references: [cases.id] }),
}));

export const fakeryMatrixItemsRelations = relations(fakeryMatrixItems, ({ one }) => ({
  case: one(cases, { fields: [fakeryMatrixItems.caseId], references: [cases.id] }),
}));

export const populationDensityItemsRelations = relations(populationDensityItems, ({ one }) => ({
  case: one(cases, { fields: [populationDensityItems.caseId], references: [cases.id] }),
}));

export const softSignalsRelations = relations(softSignals, ({ one }) => ({
  case: one(cases, { fields: [softSignals.caseId], references: [cases.id] }),
}));

export const protocolStepsRelations = relations(protocolSteps, ({ one }) => ({
  case: one(cases, { fields: [protocolSteps.caseId], references: [cases.id] }),
}));

export const entitiesRelations = relations(entities, ({ one }) => ({
  case: one(cases, { fields: [entities.caseId], references: [cases.id] }),
}));

export const contradictionsRelations = relations(contradictions, ({ one }) => ({
  case: one(cases, { fields: [contradictions.caseId], references: [cases.id] }),
}));
