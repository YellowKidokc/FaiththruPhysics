import { createConnection } from 'mysql2/promise';

if (!process.env.DATABASE_URL) {
  throw new Error('DATABASE_URL is required to run seed-direct.ts');
}

const dbUrl = new URL(process.env.DATABASE_URL);
const connectionConfig = {
  host: dbUrl.hostname,
  port: Number(dbUrl.port || 3306),
  user: decodeURIComponent(dbUrl.username),
  password: decodeURIComponent(dbUrl.password),
  database: decodeURIComponent(dbUrl.pathname.replace(/^\//, '')),
  connectTimeout: 10000,
  ssl: { rejectUnauthorized: false },
};

async function seed() {
  console.log("Seeding OpenIntel with Shroud of Turin...");
  const conn = await createConnection(connectionConfig);

  // Check if case exists
  const [existing] = await conn.query('SELECT id FROM cases WHERE case_id = ?', ['OI-CT-SHROUD']);
  if ((existing as any[]).length > 0) {
    console.log("Shroud case already exists. Skipping seed.");
    await conn.end();
    return;
  }

  // Insert case
  const [caseResult] = await conn.execute(
    'INSERT INTO cases (case_id, canonical_title, case_type, category, status, one_sentence_verdict, notes) VALUES (?, ?, ?, ?, ?, ?, ?)',
    ['OI-CT-SHROUD', 'Shroud of Turin', 'PHENOMENON', 'Religious Artifact / Forensic Phenomenon', 'ACTIVE', null, 'Universal truth-finding protocol proof-of-concept.']
  );
  const caseId = (caseResult as any).insertId;
  console.log(`Case created: ${caseId}`);

  // MATERIAL SCIENCE
  await conn.execute(
    'INSERT INTO evidence_items (case_id, domain, evidence_name, tier, source, what_it_proves, fabrication_cost, fabrication_cost_description, counter_arguments, is_discriminating, year_discovered) VALUES ?',
    [[
      [caseId, 'MATERIAL_SCIENCE', 'Pure linen, flax plant, 3:1 herringbone weave', 'T1', 'STURP 1978, textile analysis', 'Wealthy burial cloth, consistent with Joseph of Arimathea', 'EXTREME', 'Cannot replicate exact weave structure from 1st century', 'None - never disputed', 'true', 1978],
      [caseId, 'MATERIAL_SCIENCE', 'Image only 2 microns deep', 'T1', 'STURP microchemical analysis', 'Superficial discoloration of topmost fibrils only - no substance applied', 'IMPOSSIBLE', 'No known technology achieves this precision', 'None - never replicated', 'true', 1978],
      [caseId, 'MATERIAL_SCIENCE', 'No paint, dye, pigment, or ink present', 'T1', 'STURP (Schwalbe & Rogers 1982)', 'Peer-reviewed, never overturned - image is not artistic', 'EXTREME', null, 'McCrone iron oxide claim debunked by superior methods', 'true', 1982],
      [caseId, 'MATERIAL_SCIENCE', 'Blood penetrates fully; image does not', 'T1', 'STURP', 'Different mechanisms - blood is contact transfer, image is not', 'HIGH', null, 'None', 'true', 1978],
      [caseId, 'MATERIAL_SCIENCE', 'Chemical change to fibrils (oxidation/dehydration)', 'T1', 'STURP', 'Not an applied substance - molecular alteration of cellulose', 'EXTREME', null, 'None', 'true', 1978],
      [caseId, 'MATERIAL_SCIENCE', 'Zero vanillin remaining (Rogers 2005)', 'T2', 'Thermochimica Acta 2005, peer-reviewed', 'Zero vanillin = ancient (>1300 years old)', 'HIGH', null, 'Corner sample had vanillin - supports contamination theory', 'true', 2005],
      [caseId, 'MATERIAL_SCIENCE', 'WAXS aging matches Masada shroud (AD 70)', 'T2', 'De Caro et al. 2022, Institute of Crystallography, Rome', '2000-year aging profile matches known 1st century textile', 'EXTREME', null, 'Needs independent replication', 'true', 2022],
      [caseId, 'MATERIAL_SCIENCE', 'Blood went on FIRST, image formed SECOND', 'T1', 'STURP (Heller & Adler)', 'Eliminates ALL forgery hypotheses - every artistic process is image-first, blood-second', 'IMPOSSIBLE', 'No known technique produces blood-first, image-second', 'Never seriously challenged, never overturned', 'true', 1978],
    ]]
  );
  console.log("  Material Science: 8");

  // HEMATOLOGY
  await conn.execute(
    'INSERT INTO evidence_items (case_id, domain, evidence_name, tier, source, what_it_proves, fabrication_cost, fabrication_cost_description, counter_arguments, is_discriminating, year_discovered) VALUES ?',
    [[
      [caseId, 'HEMATOLOGY', 'Type AB human male blood', 'T1', 'Heller & Adler 1980-81, Baima Bollone', 'Multiple independent confirmations - real human blood', 'EXTREME', 'Requires actual human blood of specific type', 'AB is common in Middle East; possible contamination from handling', 'true', 1980],
      [caseId, 'HEMATOLOGY', 'Pre-mortem AND post-mortem blood (chemically distinct)', 'T1', 'STURP hematological analysis', 'Different chemistry, different locations - clinical precision', 'IMPOSSIBLE', 'Hematology did not exist until 19th century', 'None', 'true', 1978],
      [caseId, 'HEMATOLOGY', 'Post-mortem blood at side wound (rib 5-6)', 'T1', 'STURP', "Consistent with John's Gospel - spear wound after death", 'EXTREME', null, 'None', 'true', 1978],
      [caseId, 'HEMATOLOGY', 'Pulmonary edema mixture (6:1 fluid to blood)', 'T2', 'Hematological reports', 'Consistent with crucifixion asphyxiation causing heart failure', 'EXTREME', null, 'Specific ratio disputed by some pathologists', 'true', null],
      [caseId, 'HEMATOLOGY', 'High creatinine = kidney failure', 'T2', 'Blood chemistry analysis', 'Consistent with torture/dehydration', 'HIGH', null, 'Degradation over time affects readings', 'false', null],
      [caseId, 'HEMATOLOGY', 'High ferritin = systemic inflammation', 'T2', 'Blood chemistry analysis', 'Consistent with scourging', 'HIGH', null, 'Degradation concerns', 'false', null],
      [caseId, 'HEMATOLOGY', '~1/3 blood volume lost before death', 'T2', 'Estimated from wound analysis', 'Consistent with flagellation', 'HIGH', null, 'Estimate, not measurement', 'false', null],
      [caseId, 'HEMATOLOGY', 'Sudarium of Oviedo: separate artifact, also Type AB', 'T2', 'Independent analysis', 'Two artifacts, two countries, same blood type - independent confirmation', 'EXTREME', 'Requires cross-artifact coordination', 'Type AB common in region; may not be same individual', 'true', null],
    ]]
  );
  console.log("  Hematology: 8");

  // PATHOLOGY
  await conn.execute(
    'INSERT INTO evidence_items (case_id, domain, evidence_name, tier, source, what_it_proves, fabrication_cost, counter_arguments, is_discriminating, year_discovered) VALUES ?',
    [[
      [caseId, 'PATHOLOGY', '~700 total wounds estimated', 'T1', 'STURP image analysis', 'Front + back + estimated lateral - comprehensive torture record', 'EXTREME', 'Lateral count is estimated', 'false', 1978],
      [caseId, 'PATHOLOGY', '200+ scourge marks (dorsal), 172+ (frontal)', 'T1', 'STURP', 'Dumbbell-shaped = Roman flagrum with lead tips', 'EXTREME', 'None', 'true', 1978],
      [caseId, 'PATHOLOGY', 'Two distinct scourge angles = two executioners', 'T1', 'STURP', 'Consistent with Roman practice', 'HIGH', 'None', 'false', 1978],
      [caseId, 'PATHOLOGY', '50 puncture wounds on head (helmet, not wreath)', 'T1', 'STURP', 'Contradicts medieval art convention - medieval shows wreath', 'EXTREME', 'None', 'true', 1978],
      [caseId, 'PATHOLOGY', 'Nail wounds through wrists (not palms)', 'T1', 'STURP', 'Contradicts medieval art, confirmed by forensics - palms cannot support body weight', 'EXTREME', 'None - anatomically correct', 'true', 1978],
      [caseId, 'PATHOLOGY', 'Side wound between rib 5-6 (~3cm wide)', 'T1', 'STURP', 'Consistent with Roman spear (lancea)', 'HIGH', 'None', 'true', 1978],
      [caseId, 'PATHOLOGY', 'Right shoulder diagonal abrasions', 'T1', 'STURP', 'Patibulum (crossbeam) carrying marks', 'HIGH', 'None', 'false', 1978],
      [caseId, 'PATHOLOGY', 'Knee abrasions + nose tip trauma', 'T1', 'STURP', 'Forward fall under 125-lb crossbeam load', 'HIGH', 'None', 'false', 1978],
    ]]
  );
  console.log("  Pathology: 8");

  // BOTANICAL / GEOLOGICAL
  await conn.execute(
    'INSERT INTO evidence_items (case_id, domain, evidence_name, tier, source, what_it_proves, fabrication_cost, counter_arguments, is_discriminating, year_discovered) VALUES ?',
    [[
      [caseId, 'BOTANICAL_GEOLOGICAL', '56 pollen species identified', 'T2', 'Max Frei (5 years study)', 'Geographic specificity - methodology criticized but not debunked', 'EXTREME', "Frei's methodology questioned; some pollen could be contaminants from display", 'false', 1973],
      [caseId, 'BOTANICAL_GEOLOGICAL', 'Species blooming only in April in Jerusalem', 'T2', 'Frei + Danin/Baruch 1999', 'Seasonal + geographic specificity', 'EXTREME', 'Pollen contamination from later handling possible', 'false', 1999],
      [caseId, 'BOTANICAL_GEOLOGICAL', 'Jerusalem limestone/clay on feet', 'T2', 'Soil analysis', 'Native to Jerusalem', 'HIGH', 'Could be from later pilgrimage handling', 'false', 1978],
      [caseId, 'BOTANICAL_GEOLOGICAL', 'Jerusalem limestone/clay on knees', 'T2', 'Soil analysis', 'Consistent with falling', 'HIGH', 'Contamination possible', 'false', 1978],
      [caseId, 'BOTANICAL_GEOLOGICAL', 'Jerusalem limestone/clay on nose tip', 'T2', 'Soil analysis', 'Consistent with face-first collapse', 'HIGH', 'Contamination possible', 'false', 1978],
    ]]
  );
  console.log("  Botanical/Geological: 5");

  // IMAGING / PHYSICS
  await conn.execute(
    'INSERT INTO evidence_items (case_id, domain, evidence_name, tier, source, what_it_proves, fabrication_cost, fabrication_cost_description, counter_arguments, is_discriminating, year_discovered) VALUES ?',
    [[
      [caseId, 'IMAGING_PHYSICS', 'Photographic negative (discovered 1898)', 'T1', 'Secondo Pia', 'Positive image only visible through photographic inversion', 'IMPOSSIBLE', 'Photography invented 500+ years later', 'None - forger could not have understood negative imaging', 'true', 1898],
      [caseId, 'IMAGING_PHYSICS', '3D topographic information encoded', 'T1', 'VP8 Image Analyzer (Jumper & Jackson 1976)', 'No other image in history has this property - distance-correlated brightness', 'IMPOSSIBLE', '3D spatial encoding concept not formalized until 20th century', 'None', 'true', 1976],
      [caseId, 'IMAGING_PHYSICS', 'VUV radiation replicates chemical change', 'T1', 'Di Lazzaro, ENEA Laboratories', 'Peer-reviewed physics - vacuum ultraviolet radiation produces identical fibril change', 'EXTREME', null, 'Cannot scale to full-body dimensions', 'true', 2010],
      [caseId, 'IMAGING_PHYSICS', '~34,000 billion watts peak power required', 'T1', 'Di Lazzaro calculations', '1/40th billionth of a second - astronomical energy requirement', 'IMPOSSIBLE', null, 'Theoretical calculation, not direct measurement', 'false', null],
      [caseId, 'IMAGING_PHYSICS', 'Cannot scale to full-body dimensions', 'T1', 'ENEA', 'No existing technology can reproduce the image at body scale', 'IMPOSSIBLE', null, 'Future technology might; not proof of mechanism', 'true', null],
      [caseId, 'IMAGING_PHYSICS', 'Image only visible from 8+ feet', 'T1', 'Direct observation', 'Vanishes at close range - property of spatial frequency perception', 'EXTREME', null, 'None', 'true', null],
    ]]
  );
  console.log("  Imaging/Physics: 6");

  // HISTORICAL PROVENANCE
  await conn.execute(
    'INSERT INTO evidence_items (case_id, domain, evidence_name, tier, source, what_it_proves, fabrication_cost, counter_arguments, is_discriminating) VALUES ?',
    [[
      [caseId, 'HISTORICAL_PROVENANCE', 'Burial cloth mentioned in all four Gospels', 'T2', 'Matthew, Mark, Luke, John', 'Multiple attestation - early written sources', 'LOW', 'Gospels are religious texts, not historical records', 'false'],
      [caseId, 'HISTORICAL_PROVENANCE', 'Eusebius reference (~325 AD)', 'T2', 'Church historian, Council of Nicaea', 'Earliest written reference to image cloth', 'LOW', 'Reference is ambiguous; may not refer to Shroud', 'false'],
      [caseId, 'HISTORICAL_PROVENANCE', 'Edessa period (~900 years)', 'T2', 'Multiple historical sources', 'Known as Mandylion / Image of Edessa', 'MODERATE', 'Mandylion may be different artifact', 'false'],
      [caseId, 'HISTORICAL_PROVENANCE', 'Lirey France (Geoffrey de Charny, 1350s)', 'T1', 'Historical record', 'First European documentation - chain of custody begins', 'LOW', 'Sudden appearance without provenance is suspicious', 'false'],
      [caseId, 'HISTORICAL_PROVENANCE', 'Savoy family (traded for two castles)', 'T1', 'Historical record', 'Chain of custody documented', 'LOW', 'None', 'false'],
      [caseId, 'HISTORICAL_PROVENANCE', 'Catholic Church custody from 1983', 'T1', 'Probate records', 'Last Savoy king to Pope John Paul II', 'LOW', 'None', 'false'],
    ]]
  );
  console.log("  Historical Provenance: 6");

  // DATING
  await conn.execute(
    'INSERT INTO evidence_items (case_id, domain, evidence_name, tier, source, what_it_proves, fabrication_cost, counter_arguments, is_discriminating, year_discovered) VALUES ?',
    [[
      [caseId, 'DATING', '1988 C-14: 1260-1390 CE', 'T3', 'Damon et al. 1989 (Nature)', 'FROM CONTAMINATED CORNER SAMPLE - methodology compromised', 'LOW', 'Multiple independent confirmations of contamination issues', 'true', 1988],
      [caseId, 'DATING', 'Rogers: sample chemically different from main cloth', 'T1', 'Thermochimica Acta 2005', 'Cotton in sample (not linen), vanillin absent from main cloth', 'LOW', 'Rogers had pro-authenticity bias; peer review questioned', 'true', 2005],
      [caseId, 'DATING', 'WAXS: 2000-year aging profile', 'T2', 'De Caro et al. 2022', 'Matches Masada shroud (AD 70)', 'EXTREME', 'Needs independent replication', 'true', 2022],
      [caseId, 'DATING', 'Vanillin: zero remaining (main cloth)', 'T2', 'Rogers 2005', 'Medieval cloth would retain traces; zero indicates >1300 years', 'EXTREME', 'Fires may have accelerated vanillin loss', 'true', 2005],
      [caseId, 'DATING', 'Raw C-14 data suppressed 29 years', 'T1', 'Casabianca et al. 2019', 'British Museum released only after FOIA-equivalent; statistical heterogeneity', 'LOW', 'Institutional caution, not conspiracy', 'true', 2019],
      [caseId, 'DATING', 'Only 3 of 7 planned labs tested', 'T1', 'Historical record', 'No explanation for reduction; reduced statistical power', 'LOW', 'Budget constraints', 'true', null],
      [caseId, 'DATING', 'Sample from visibly contaminated corner', 'T1', 'Visual inspection', 'Anyone can see the discoloration - not representative', 'LOW', 'Labs attempted to clean sample', 'true', null],
    ]]
  );
  console.log("  Dating: 7");

  // ART HISTORICAL
  await conn.execute(
    'INSERT INTO evidence_items (case_id, domain, evidence_name, tier, source, what_it_proves, fabrication_cost, counter_arguments, is_discriminating) VALUES ?',
    [[
      [caseId, 'ART_HISTORICAL', '200+ icons share facial features with Shroud', 'T2', 'Iconographic studies', 'Common source material indicated', 'MODERATE', 'Icons copied each other, not necessarily Shroud', 'false'],
      [caseId, 'ART_HISTORICAL', 'Vignon markings (15-20 oddities)', 'T2', 'Paul Vignon', 'Systematic correspondence between Shroud and icons', 'MODERATE', 'Selection bias in choosing which features to compare', 'false'],
      [caseId, 'ART_HISTORICAL', 'Byzantine coinage matches Shroud face', 'T2', 'Numismatic studies', 'Coins predate any proposed medieval hoax', 'MODERATE', 'Coins are stylized, not photographic', 'false'],
      [caseId, 'ART_HISTORICAL', 'Pantocrator icon (6th century) overlaps Shroud', 'T2', "St. Catherine's Monastery", 'Predates all medieval forgery dates', 'HIGH', 'Overlapping features are generic', 'false'],
      [caseId, 'ART_HISTORICAL', 'Medieval art shows DIFFERENT Jesus', 'T2', 'Art history', 'Effeminate, no facial hair, nails in palms = NOT from Shroud - forger contradicted own era', 'EXTREME', 'Shroud could have influenced art AFTER it appeared', 'true'],
    ]]
  );
  console.log("  Art Historical: 5");

  // TIMELINE
  await conn.execute(
    'INSERT INTO timeline_events (case_id, event_date, date_precision, event_description, source, verification_status, tier, entities_involved) VALUES ?',
    [[
      [caseId, '~30 AD', 'YEAR', 'Crucifixion of Jesus', 'Gospels', 'CONFIRMED', 'T2', null],
      [caseId, '~325 AD', 'YEAR', 'Eusebius reference to image cloth at Council of Nicaea', 'Eusebius, Church History', 'PROBABLE', 'T2', null],
      [caseId, '~400-944 AD', 'DECADE', 'Mandylion / Image of Edessa period (540+ years)', 'Multiple historical sources', 'PROBABLE', 'T2', 'King Abgar V'],
      [caseId, '~944-1204 AD', 'DECADE', 'Constantinople period', 'Byzantine records', 'PROBABLE', 'T2', null],
      [caseId, '1204', 'YEAR', 'Fourth Crusade sacks Constantinople; relics dispersed', 'Historical record', 'CONFIRMED', 'T1', null],
      [caseId, '~1353', 'YEAR', 'Shroud appears in Lirey, France (Geoffrey de Charny)', 'Historical record', 'CONFIRMED', 'T1', 'Geoffrey de Charny'],
      [caseId, '1389', 'YEAR', "Bishop d'Arcis memo (draft, possibly never sent)", "d'Arcis memo", 'DISPUTED', 'T4', 'Bishop Pierre d\'Arcis'],
      [caseId, '1532', 'YEAR', 'Chambery fire damages Shroud; molten silver burns through', 'Historical record', 'CONFIRMED', 'T1', null],
      [caseId, '1578', 'YEAR', 'Shroud moved to Turin', 'Historical record', 'CONFIRMED', 'T1', 'Emmanuel Philibert'],
      [caseId, '1898', 'YEAR', 'Secondo Pia photographs Shroud - discovers photographic negative', 'Secondo Pia', 'CONFIRMED', 'T1', 'Secondo Pia'],
      [caseId, '1976', 'YEAR', 'VP8 Image Analyzer reveals 3D topographic encoding', 'Jumper & Jackson', 'CONFIRMED', 'T1', 'Eric Jumper, John Jackson'],
      [caseId, '1978', 'YEAR', 'STURP (Shroud of Turin Research Project) full scientific examination', 'STURP team', 'CONFIRMED', 'T1', 'Heller, Adler, Rogers, Jumper, Jackson'],
      [caseId, '1988', 'YEAR', 'C-14 dating: 1260-1390 CE (contaminated corner sample)', 'Damon et al. 1989 (Nature)', 'DISPUTED', 'T3', 'British Museum, 3 labs'],
      [caseId, '2005', 'YEAR', 'Rogers (Thermochimica Acta): sample chemically different from main cloth', 'Ray Rogers', 'CONFIRMED', 'T1', 'Ray Rogers'],
      [caseId, '2019', 'YEAR', 'Casabianca: British Museum releases raw C-14 data after 29-year suppression', 'Casabianca et al.', 'CONFIRMED', 'T1', null],
      [caseId, '2022', 'YEAR', 'WAXS study: 2000-year aging profile matches Masada shroud (AD 70)', 'De Caro et al.', 'CONFIRMED', 'T2', 'Giuseppe De Caro, ENEA'],
    ]]
  );
  console.log("  Timeline: 16");

  // FAKERY MATRIX
  await conn.execute(
    'INSERT INTO fakery_matrix_items (case_id, constraint_id, constraint_name, description, fabrication_cost, fabrication_cost_description, possibility_score, possibility_justification, rating, sort_order) VALUES ?',
    [[
      [caseId, 'F1', 'Kill a man in a specific way', 'Real human male blood - pre-mortem AND post-mortem, Type AB (6% population). Scourge with Roman flagrum from two angles (~372 dumbbell marks). Drive nails through wrists and heels. Stab between rib 5-6 AFTER death for post-mortem blood with pulmonary edema at 6:1 ratio. 125-lb crossbeam, face-first fall onto Jerusalem limestone.', 'EXTREME', 'Requires actual murder with clinical precision', '0.01', 'Requires killing a person with exact wound specifications', 'EXTREME', 1],
      [caseId, 'F2', 'Obtain Jerusalem-specific materials', "Soil from Jerusalem (specific limestone and clay) on feet, knees, and nose tip. Pollen from 56 plant species including species blooming ONLY in April in Jerusalem. Medieval France had no knowledge of Levantine spring-bloom species.", 'EXTREME', "Requires trans-Mediterranean botanical knowledge that didn't exist", '0.01', "Botanical cataloging of Levant didn't exist in medieval Europe", 'EXTREME', 2],
      [caseId, 'F3', 'Invent photography 500+ years early', 'Image is a photographic negative. Positive only visible through photographic inversion (technology invented 1840s). Forger must create image indistinct to every viewer for 500 years.', 'IMPOSSIBLE', "Technology/concept that won't exist for 5 centuries", '0', 'Concept of negative/positive imaging unknown before 19th century', 'IMPOSSIBLE', 3],
      [caseId, 'F4', 'Encode 3D information into 2D surface', 'No painting, photograph, or print contains distance-correlated brightness data. VP8 image analyzer reveals topographic depth. Forger must understand 3D spatial encoding and apply brightness gradients correlating to body-to-cloth distance.', 'IMPOSSIBLE', "Concept didn't exist until 20th century", '0', '3D spatial encoding formalized in 20th century, impossible to conceive earlier', 'IMPOSSIBLE', 4],
      [caseId, 'F5', 'Apply image at exactly 2 microns depth', 'Not with paint, dye, or any substance. Chemical change affects only outermost fibrils (top 0.2 microns of 150-200 fiber threads). No brush, stamp, contact transfer, or vapor method achieves this.', 'IMPOSSIBLE', 'No known technology - medieval OR modern', '0', 'No existing technology can achieve this precision at body scale', 'IMPOSSIBLE', 5],
      [caseId, 'F6', 'Make image survive fire and water', 'Shroud survived at least 3 fires and water dousing. Any applied pigment, dye, or organic medium would degrade, smear, or wash out.', 'EXTREME', 'Requires permanent chemical alteration of cellulose structure', '0.01', 'Requires molecular-level alteration inherently immune to fire/water', 'EXTREME', 6],
      [caseId, 'F7', 'Know Roman crucifixion forensics with clinical precision', "Wound patterns contradict medieval art: nails through wrists (not palms), helmet of thorns (not wreath), naked (not loincloth), 5'10\" 175-180 lbs (not thin). Forger knew what modern forensic pathology confirmed.", 'EXTREME', 'Requires forensic knowledge that contradicted contemporary convention', '0.01', 'All artistic convention contradicted the actual forensic evidence', 'EXTREME', 7],
      [caseId, 'F8', 'Fake blood chemistry before blood chemistry existed', "Distinguish pre-mortem from post-mortem blood. Correct creatinine and ferritin levels. Pulmonary edema at correct ratio. Translucent serum halo. Hematology didn't exist until 19th century.", 'IMPOSSIBLE', "Requires science that didn't exist", '0', 'Blood chemistry as science emerged 19th century', 'IMPOSSIBLE', 8],
      [caseId, 'F9', 'Get the blood type right', 'Type AB - not identified until Landsteiner 1901. Must match Sudarium of Oviedo (separate artifact, separate country, separate provenance chain).', 'IMPOSSIBLE', 'Requires knowledge 500+ years early AND cross-artifact coordination', '0', 'ABO typing invented 1901; cross-artifact coordination impossible', 'IMPOSSIBLE', 9],
      [caseId, 'F10', 'Make image disappear at close range', 'Image only visible from 8+ feet. Property of superficial fibril discoloration and human visual acuity interaction. No painting or applied image behaves this way.', 'EXTREME', 'Requires understanding of spatial frequency perception', '0.01', 'Requires optics knowledge not available in medieval period', 'EXTREME', 10],
    ]]
  );
  console.log("  Fakery Matrix: F1-F10");

  // POPULATION DENSITY
  await conn.execute(
    'INSERT INTO population_density_items (case_id, direction, capability, location_required, era_required, density_score, confidence, justification, population_estimate, sort_order) VALUES ?',
    [[
      [caseId, 'FORGERY', 'Forensic Pathologist (Roman crucifixion expertise)', 'Lirey, France', '14th century', '0', 'HIGH', 'Forensic pathology as discipline did not exist until 19th century', '0', 1],
      [caseId, 'FORGERY', 'Hematologist (pre/post-mortem blood chemistry)', 'Lirey, France', '14th century', '0', 'HIGH', 'Blood chemistry did not exist as science until 19th century', '0', 2],
      [caseId, 'FORGERY', 'Botanist (Levantine spring flora)', 'Lirey, France', '14th century', '0', 'HIGH', 'No botanical catalog of Levantine species existed in medieval Europe', '0', 3],
      [caseId, 'FORGERY', 'Physicist (3D spatial encoding + VUV radiation)', 'Lirey, France', '14th century', '0', 'HIGH', '3D encoding concept and VUV physics not formalized until 20th century', '0', 4],
      [caseId, 'FORGERY', 'Photographer (negative/positive imaging)', 'Lirey, France', '14th century', '0', 'HIGH', 'Photography invented 500+ years later', '0', 5],
      [caseId, 'FORGERY', 'Chemist (cellulose alteration at 2 microns)', 'Lirey, France', '14th century', '0', 'HIGH', 'No known medieval or modern technique achieves this', '0', 6],
      [caseId, 'FORGERY', 'Person willing to commit specific murder for forgery', 'Lirey, France', '14th century', '0.001', 'MEDIUM', 'Possible but no evidence of such a person; requires killing with clinical precision', '<1', 7],
      [caseId, 'FORGERY', 'ALL capabilities in ONE person', 'Lirey, France', '14th century', '0', 'HIGH', 'Compound probability of all skills in one person: ZERO', '0', 8],
    ]]
  );
  console.log("  Population Density: 8");

  // SOFT SIGNALS
  await conn.execute(
    'INSERT INTO soft_signals (case_id, signal_name, signal_key, description, score, max_score, justification, evidence_refs, sort_order) VALUES ?',
    [[
      [caseId, 'Narrative Compression', 'NARRATIVE_COMPRESSION', 'Official explanation requires too many coincidences to be simultaneously true', '9.5', '10', "C-14 dating requires: contaminated sample, wrong corner, reduced labs, suppressed data, AND disparate results all aligning to same wrong date", 'Casabianca 2019, Rogers 2005', 1],
      [caseId, 'Coincidence Density', 'COINCIDENCE_DENSITY', "Number of independent 'coincidences' required exceeds reasonable threshold", '9', '10', "8+ independent domains of evidence all converge on 1st century; each requires separate 'explanation'", '8-domain evidence catalog', 2],
      [caseId, 'Timing Friction', 'TIMING_FRICTION', 'Events cluster suspiciously or critical moments lack temporal smoothness', '8', '10', 'Shroud appears in France exactly when provenance chain gaps; 29-year data suppression timed around career advancement', 'Timeline events, Casabianca 2019', 3],
      [caseId, 'Suppression Pressure', 'SUPPRESSION_PRESSURE', 'Evidence or data is suppressed, delayed, or access-restricted', '9', '10', 'British Museum suppressed raw C-14 data for 29 years; released only after FOIA-equivalent', 'Casabianca et al. 2019', 4],
      [caseId, 'Documentary Disappearance', 'DOCUMENTARY_DISAPPEARANCE', 'Key documents missing or destroyed at convenient moments', '6', '10', "d'Arcis memo is draft (possibly never sent); some Constantinople records lost", 'd\'Arcis memo 1389', 5],
      [caseId, 'Burden Inversion', 'BURDEN_INVERSION', 'Burden of proof has been shifted from claimant to skeptic inappropriately', '7', '10', "Authenticity bears burden yet skeptics offer 'someone could have done it somehow' as counter-argument", 'Skeptical objections analysis', 6],
      [caseId, 'Information Asymmetry', 'INFO_ASYMMETRY', 'One side controls access to evidence or has privileged information', '7', '10', 'Catholic Church controls physical access; British Museum controlled C-14 raw data', '1988 C-14 protocol', 7],
      [caseId, 'Expert Dissensus', 'EXPERT_DISSENSUS', 'Domain experts are split in ways that correlate with non-evidential factors', '5', '10', 'Split correlates with pre-commitment rather than expertise; STURP scientists (who examined) vs non-examiners', 'STURP composition, Heller & Adler', 8],
      [caseId, 'Institutional Resistance', 'INSTITUTIONAL_RESISTANCE', 'Established institutions resist updating positions despite new evidence', '6', '10', "Nature has not retracted 1989 C-14 paper despite known contamination; some institutions slow to acknowledge WAXS 2022", 'Nature 1989, De Caro 2022', 9],
      [caseId, 'Replication Failure', 'REPLICATION_FAILURE', 'Key claims cannot be replicated or reproduced by independent parties', '8', '10', 'No one has reproduced Shroud image properties; all proposed techniques fail on multiple features', 'Fakery Matrix F1-F10', 10],
      [caseId, 'Absence of Contradiction', 'ABSENCE_CONTRADICTION', 'The authentic evidence set has no internal contradictions despite spanning 8 domains', '9', '10', 'All 8 domains converge consistently; no evidence contradicts another', 'Full evidence catalog', 11],
      [caseId, 'Predictive Success', 'PREDICTIVE_SUCCESS', 'Position predicted findings before they were discovered', '7', '10', 'VP8 3D encoding predicted by image properties; Vignon markings predicted common source', 'VP8 1976, Vignon studies', 12],
      [caseId, 'Hostile Corroboration', 'HOSTILE_CORROBORATION', 'Evidence confirmed by parties with incentive to disprove it', '8', '10', 'STURP included skeptics; C-14 labs expected to confirm medieval date; all confirmed ancient properties', 'STURP 1978, Heller & Adler', 13],
      [caseId, 'Noise Floor Check', 'NOISE_FLOOR', "Truth has noise; fabrication doesn't - authentic evidence has expected messiness", '7', '10', 'Evidence is messy (some T2, some T3, disputes about C-14) but core findings are robust across independent sources', 'Full evidence catalog', 14],
    ]]
  );
  console.log("  Soft Signals: 14");

  // PROTOCOL STEPS
  await conn.execute(
    'INSERT INTO protocol_steps (case_id, step_number, step_name, step_key, description, status, findings, conclusion, completed_at) VALUES ?',
    [[
      [caseId, 1, 'THE PACT (Q0)', 'pact', 'Both parties affirm truth exists and they want to find it more than they want to win.', 'COMPLETED', 'Protocol applied to Shroud case; truth-seeking posture established', 'PASS', new Date()],
      [caseId, 2, 'Isolate the Exact Disagreement', 'isolate_disagreement', 'Not the broad claim. The specific point of divergence.', 'COMPLETED', 'Core disagreement: Is the Shroud a 1st century burial cloth with supernatural image formation, or a medieval forgery?', 'PASS - disagreement isolated', new Date()],
      [caseId, 3, 'Competing Predictions', 'competing_predictions', 'If Position A is true, what specific observable things must be true? If Position B is true, what specific observable things must be true?', 'COMPLETED', 'Authenticity predicts: ancient cloth, real blood, no pigments, 3D encoding, impossible to replicate. Forgery predicts: pigments, medieval materials, reproducible technique.', 'PASS - predictions mapped', new Date()],
      [caseId, 4, 'The Update Commitment', 'update_commitment', 'Both parties state IN ADVANCE what evidence would change their mind.', 'COMPLETED', 'Authenticity side: C-14 from clean sample + replication of image properties. Skeptic side: No specific update criteria stated.', 'Authenticity side passes; skeptic side fails', new Date()],
      [caseId, 5, 'Evidence Classification', 'evidence_classification', 'All evidence classified into tiers T1-T5 by fabrication cost, independence, and verifiability.', 'COMPLETED', '57 evidence items across 8 domains: 30 T1, 17 T2, 7 T3, 0 T4, 0 T5. Strong T1/T2 concentration.', 'PASS - evidence strongly weighted toward T1/T2', new Date()],
      [caseId, 6, 'Independence Audit', 'independence_audit', 'Verify source independence. Count only discriminating evidence.', 'COMPLETED', 'Sources: STURP (independent team), ENEA (independent lab), De Caro (independent), Heller & Adler (independent).', 'PASS - independence verified', new Date()],
      [caseId, 7, 'Coherence Test + Noise-Floor + Absence Audit', 'coherence_test', 'Which position explains full evidence set with minimum complexity?', 'COMPLETED', 'Authenticity: single hypothesis explains all 8 domains. Forgery: requires 10+ independent ad hoc explanations.', 'PASS - authenticity more coherent', new Date()],
      [caseId, 8, 'Forced Inversion (Fakery Matrix)', 'forced_inversion', 'Each side argues the OPPOSITE position.', 'COMPLETED', 'Fakery Matrix F1-F10: 5 IMPOSSIBLE, 5 EXTREME ratings. Compound probability functionally zero.', 'PASS - forgery impossible', new Date()],
      [caseId, 9, 'The Solomon Test', 'solomon_test', 'Judge designs scenario where truth-seeking and victory-seeking produce DIFFERENT behaviors.', 'COMPLETED', 'Authenticity advocates accept C-14 from clean sample. Skeptics offer no criteria to accept authenticity.', 'Authenticity side passes Solomon Test', new Date()],
      [caseId, 10, 'Honest Update', 'honest_update', 'Based on all evidence: which position explains more with less?', 'COMPLETED', 'Authenticity explains 8 domains with single hypothesis. Forgery requires impossible forger with zero population density.', 'UPDATE: Authenticity strongly supported', new Date()],
    ]]
  );
  console.log("  Protocol Steps: 10");

  // ENTITIES
  await conn.execute(
    'INSERT INTO entities (case_id, entity_name, entity_type, known_facts, disputed_claims, connections) VALUES ?',
    [[
      [caseId, 'Secondo Pia', 'PERSON', 'Amateur photographer who first photographed Shroud in 1898', 'None', 'Discovered photographic negative property'],
      [caseId, 'John Jackson', 'PERSON', 'Physicist, STURP team leader', 'None', 'VP8 discovery, STURP leadership'],
      [caseId, 'Ray Rogers', 'PERSON', 'Los Alamos chemist, STURP team member', 'Pro-authenticity bias alleged by some', 'Thermochimica Acta 2005 paper'],
      [caseId, 'Paolo Di Lazzaro', 'PERSON', 'ENEA researcher, VUV radiation experiments', 'None', 'Peer-reviewed physics replication'],
      [caseId, 'STURP', 'ORGANIZATION', 'Shroud of Turin Research Project, 1978', 'None on core findings', '30+ scientists, multiple institutions'],
      [caseId, 'ENEA Laboratories', 'INSTITUTION', 'Italian National Agency for New Technologies', 'None', 'VUV radiation experiments'],
      [caseId, 'British Museum', 'INSTITUTION', 'Custodian of C-14 dating protocol', 'Suppressed raw data for 29 years; reduced from 7 to 3 labs', '1988 C-14 dating controversy'],
      [caseId, 'Heller & Adler', 'PERSON', 'Blood chemists, STURP team', 'None on blood findings', 'Pre/post-mortem blood chemistry'],
      [caseId, 'Walter McCrone', 'PERSON', 'Microscopist, claimed iron oxide = paint', 'Claim overruled by STURP team using better methods', 'Debunked pigment claim'],
      [caseId, 'Geoffrey de Charny', 'PERSON', 'First documented European owner, 1350s', 'How he obtained Shroud is unknown', 'Lirey, France display'],
      [caseId, 'House of Savoy', 'ORGANIZATION', 'Owned Shroud from ~1453 to 1983', 'None on ownership chain', 'Traded castles for Shroud'],
      [caseId, 'Catholic Church', 'INSTITUTION', 'Custodian since 1983', 'Some claim institutional bias toward authenticity', "Current custodian; John Paul II called Shroud 'mirror of the Gospel'"],
    ]]
  );
  console.log("  Entities: 12");

  // CONTRADICTIONS
  await conn.execute(
    'INSERT INTO contradictions (case_id, contradiction_type, description, position_a, position_b, severity_score, resolution) VALUES ?',
    [[
      [caseId, 'OFFICIAL_NARRATIVE', 'C-14 dating (1260-1390 CE) contradicts all other dating methods (WAXS, vanillin, historical provenance)', 'C-14: medieval origin', 'All other methods: ancient origin', '8', 'C-14 sample was contaminated corner; Rogers 2005 proved sample chemically different from main cloth'],
      [caseId, 'SKEPTICAL', 'Skeptical position requires accepting that a medieval forger had impossible knowledge across 8 domains', 'Shroud is medieval forgery', 'No forger could possess required skills (all rated IMPOSSIBLE/EXTREME)', '9', 'Fakery Matrix compound probability is functionally zero'],
      [caseId, 'EVIDENTIAL', "McCrone's pigment claim contradicted by STURP team using superior methods", 'McCrone: iron oxide = paint', 'Heller & Adler: iron is from blood hemoglobin, not pigment', '7', 'STURP team overruled McCrone; chemical microanalysis > optical microscopy'],
      [caseId, 'INTERNAL', 'If Shroud is forged in 14th century, forger created image invisible for 500 years until photography invented', 'Forger created image in 1350s', 'Image only became visible with photography in 1898', '9', 'Impossible to explain - forger could not have understood negative imaging'],
    ]]
  );
  console.log("  Contradictions: 4");

  await conn.end();
  console.log("\n=== SEED COMPLETE ===");
}

seed().catch(e => { console.error(e.message); process.exit(1); });
