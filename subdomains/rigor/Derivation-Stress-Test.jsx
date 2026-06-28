import { useState, useCallback, useMemo } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, Cell } from "recharts";

// ── PHYSICS FEATURE TAGS ──
// These are physics-domain properties. Each tag describes a type of physical behavior.
// Tags are assigned based on the EQUATION of each term, not its parent assignment.
const TAG_LABELS = {
  curvature: "Curvature/GR",
  field_eq: "Field Equation",
  wave: "Wave/Oscillation",
  potential: "Potential Energy",
  confinement: "Binding/Confinement",
  equilibrium: "Equilibrium/Stability",
  entropy: "Entropy/Disorder",
  free_energy: "Free Energy/Cost",
  phase_trans: "Phase Transition",
  channel: "Info Channel",
  encoding: "Signal Encoding",
  compression: "Data Compression",
  detection: "Signal Detection",
  prediction: "Prediction/Filtering",
  frame: "Reference Frame",
  proper_time: "Proper Time",
  metric: "Metric/Distance",
  geodesic: "Geodesic",
  measurement: "QM Measurement",
  coherence: "QM Coherence",
  decoherence: "Decoherence",
  phase_lock: "Phase Lock",
  conservation: "Conservation Law",
  operator: "State Operator",
  impossibility: "Impossibility Thm",
  external: "External Source",
  resonance: "Resonance",
  feedback: "Feedback Control",
  activation: "Activation Energy",
  radiation: "Radiation/Emission",
  eigenmode: "Eigenmode",
  boundary: "Boundary Condition",
  boost: "Lorentz Boost",
  symmetry: "Symmetry/Invariance",
};

// ── PARENT LAW SIGNATURES ──
// Each parent law gets tags based on its PHYSICS DOMAIN
const PARENTS = [
  { id: 0, name: "Laws 1+2: Grace", short: "Grace", color: "#c9a227",
    tags: ["curvature","field_eq","impossibility","external","operator","conservation","phase_trans"] },
  { id: 1, name: "Law 4: Love/Strong", short: "Fruits", color: "#ef4444",
    tags: ["confinement","potential","equilibrium","resonance","conservation","feedback","activation"] },
  { id: 2, name: "Law 5: Judgment/Thermo", short: "Justice", color: "#f97316",
    tags: ["entropy","free_energy","phase_trans","conservation"] },
  { id: 3, name: "Law 8: Faith/Quantum", short: "Armor", color: "#a78bfa",
    tags: ["measurement","coherence","decoherence","phase_lock","conservation","phase_trans"] },
  { id: 4, name: "Law 3: Truth/EM", short: "I AM", color: "#3b82f6",
    tags: ["wave","radiation","eigenmode","boundary","resonance","channel"] },
  { id: 5, name: "Law 6: Logos/Shannon", short: "Logos", color: "#22c55e",
    tags: ["channel","encoding","compression","detection","prediction","entropy"] },
  { id: 6, name: "Law 7: Relativity", short: "Covenant", color: "#06b6d4",
    tags: ["frame","proper_time","metric","geodesic","boost","symmetry"] },
];

// ── DERIVED TERMS ──
// Tags assigned based on each term's EQUATION, not its parent.
const TERMS = [
  // Chain 1: Grace (parent 0)
  { name: "Forgiveness", tags: ["operator","conservation","external"], parent: 0 },
  { name: "Healing", tags: ["external","operator","field_eq"], parent: 0 },
  { name: "Redemption", tags: ["external","operator","confinement"], parent: 0 },
  { name: "Sanctification", tags: ["curvature","field_eq","operator"], parent: 0 },
  { name: "Justification", tags: ["operator","external","symmetry"], parent: 0 },
  { name: "Adoption", tags: ["operator","external","frame"], parent: 0 },
  { name: "Regeneration", tags: ["phase_trans","operator","external"], parent: 0 },
  // Chain 2: Fruits (parent 1)
  { name: "Love", tags: ["potential","equilibrium","confinement"], parent: 1 },
  { name: "Joy", tags: ["resonance","potential","equilibrium"], parent: 1 },
  { name: "Peace", tags: ["equilibrium","potential","confinement"], parent: 1 },
  { name: "Patience", tags: ["potential","activation","equilibrium"], parent: 1 },
  { name: "Kindness", tags: ["activation","potential","equilibrium"], parent: 1 },
  { name: "Goodness", tags: ["confinement","potential","external"], parent: 1 },
  { name: "Faithfulness", tags: ["conservation","symmetry","potential"], parent: 1 },
  { name: "Gentleness", tags: ["feedback","potential","resonance"], parent: 1 },
  { name: "Self-Control", tags: ["feedback","potential","equilibrium"], parent: 1 },
  // Chain 3: Justice-Mercy (parent 2)
  { name: "Justice", tags: ["entropy","free_energy","conservation"], parent: 2 },
  { name: "Mercy", tags: ["free_energy","entropy","external"], parent: 2 },
  { name: "The Cross", tags: ["free_energy","entropy","conservation","phase_trans"], parent: 2 },
  { name: "Beatitude 1", tags: ["phase_trans","free_energy","entropy"], parent: 2 },
  { name: "Beatitude 2", tags: ["phase_trans","free_energy","entropy"], parent: 2 },
  { name: "Beatitude 3", tags: ["phase_trans","free_energy","entropy"], parent: 2 },
  { name: "Beatitude 4", tags: ["phase_trans","free_energy","entropy"], parent: 2 },
  { name: "Beatitude 5", tags: ["phase_trans","free_energy","entropy"], parent: 2 },
  { name: "Beatitude 6", tags: ["phase_trans","free_energy","entropy"], parent: 2 },
  { name: "Beatitude 7", tags: ["phase_trans","free_energy","entropy"], parent: 2 },
  { name: "Beatitude 8", tags: ["phase_trans","free_energy","entropy"], parent: 2 },
  // Chain 4: Armor (parent 3)
  { name: "Belt of Truth", tags: ["phase_lock","coherence","measurement"], parent: 3 },
  { name: "Breastplate", tags: ["conservation","coherence","measurement"], parent: 3 },
  { name: "Shoes of Peace", tags: ["coherence","measurement","equilibrium"], parent: 3 },
  { name: "Shield of Faith", tags: ["decoherence","coherence","measurement"], parent: 3 },
  { name: "Helmet of Salvation", tags: ["phase_trans","coherence","measurement"], parent: 3 },
  { name: "Sword of Spirit", tags: ["coherence","wave","phase_lock"], parent: 3 },
  // Chain 5: I AM (parent 4)
  { name: "Bread of Life", tags: ["wave","boundary","resonance"], parent: 4 },
  { name: "Light of World", tags: ["radiation","wave","boundary"], parent: 4 },
  { name: "The Door", tags: ["boundary","wave","eigenmode"], parent: 4 },
  { name: "Good Shepherd", tags: ["wave","eigenmode","boundary"], parent: 4 },
  { name: "Resurrection", tags: ["resonance","wave","eigenmode"], parent: 4 },
  { name: "Way/Truth/Life", tags: ["eigenmode","wave","resonance"], parent: 4 },
  { name: "The Vine", tags: ["radiation","wave","boundary"], parent: 4 },
  // Chain 6: Logos (parent 5)
  { name: "Word/Logos", tags: ["encoding","channel","compression"], parent: 5 },
  { name: "Revelation", tags: ["channel","encoding","entropy"], parent: 5 },
  { name: "Understanding", tags: ["channel","encoding","compression"], parent: 5 },
  { name: "Prophecy", tags: ["prediction","channel","encoding"], parent: 5 },
  { name: "Discernment", tags: ["detection","channel","encoding"], parent: 5 },
  { name: "Counsel", tags: ["prediction","detection","encoding"], parent: 5 },
  { name: "Knowledge", tags: ["compression","encoding","channel"], parent: 5 },
  // Chain 7: Covenant (parent 6)
  { name: "Covenant", tags: ["proper_time","frame","metric"], parent: 6 },
  { name: "Presence", tags: ["frame","proper_time","geodesic"], parent: 6 },
  { name: "Empathy", tags: ["boost","frame","proper_time"], parent: 6 },
  { name: "Constancy", tags: ["symmetry","metric","proper_time"], parent: 6 },
  { name: "Mutual Submit", tags: ["frame","symmetry","metric"], parent: 6 },
  { name: "Growth", tags: ["geodesic","metric","frame"], parent: 6 },
  { name: "Reconciliation", tags: ["boost","frame","proper_time"], parent: 6 },
];

// ── SCORING FUNCTION ──
function scoreAssignment(terms, assignments) {
  let total = 0;
  for (let i = 0; i < terms.length; i++) {
    const parentIdx = assignments[i];
    const parentTags = new Set(PARENTS[parentIdx].tags);
    const termTags = terms[i].tags;
    let matches = 0;
    for (const tag of termTags) {
      if (parentTags.has(tag)) matches++;
    }
    total += matches / termTags.length;
  }
  return total;
}

function scoreByChain(terms, assignments) {
  const chainScores = {};
  for (let i = 0; i < terms.length; i++) {
    const actualParent = terms[i].parent;
    const pName = PARENTS[actualParent].short;
    if (!chainScores[pName]) chainScores[pName] = { actual: 0, count: 0 };
    const parentTags = new Set(PARENTS[assignments[i]].tags);
    let matches = 0;
    for (const tag of terms[i].tags) {
      if (parentTags.has(tag)) matches++;
    }
    chainScores[pName].actual += matches / terms[i].tags.length;
    chainScores[pName].count++;
  }
  return chainScores;
}

// ── MONTE CARLO ──
function runMonteCarlo(terms, nTrials) {
  const n = terms.length;
  const nParents = PARENTS.length;
  const actualAssignment = terms.map(t => t.parent);
  const actualScore = scoreAssignment(terms, actualAssignment);

  const randomScores = [];
  for (let trial = 0; trial < nTrials; trial++) {
    const randomAssignment = [];
    for (let i = 0; i < n; i++) {
      randomAssignment.push(Math.floor(Math.random() * nParents));
    }
    randomScores.push(scoreAssignment(terms, randomAssignment));
  }

  randomScores.sort((a, b) => a - b);
  const exceedCount = randomScores.filter(s => s >= actualScore).length;
  const pValue = exceedCount / nTrials;

  // Build histogram
  const min = Math.floor(Math.min(...randomScores, actualScore));
  const max = Math.ceil(Math.max(...randomScores, actualScore)) + 1;
  const binWidth = (max - min) / 40;
  const bins = [];
  for (let b = min; b < max; b += binWidth) {
    const count = randomScores.filter(s => s >= b && s < b + binWidth).length;
    bins.push({ x: +(b + binWidth/2).toFixed(1), count, isActual: false });
  }

  return { actualScore, randomScores, pValue, bins, exceedCount, nTrials };
}

// ── MAIN COMPONENT ──
export default function DerivationStressTest() {
  const [nTrials, setNTrials] = useState(1000);
  const [results, setResults] = useState(null);
  const [running, setRunning] = useState(false);
  const [showTerms, setShowTerms] = useState(false);

  const actualScorePreview = useMemo(() => {
    return scoreAssignment(TERMS, TERMS.map(t => t.parent));
  }, []);

  const chainBreakdown = useMemo(() => {
    return scoreByChain(TERMS, TERMS.map(t => t.parent));
  }, []);

  const runSim = useCallback(() => {
    setRunning(true);
    setTimeout(() => {
      const r = runMonteCarlo(TERMS, nTrials);
      setResults(r);
      setRunning(false);
    }, 50);
  }, [nTrials]);

  const sigma = useMemo(() => {
    if (!results) return null;
    const mean = results.randomScores.reduce((a,b) => a+b, 0) / results.randomScores.length;
    const variance = results.randomScores.reduce((a,b) => a + (b-mean)**2, 0) / results.randomScores.length;
    const std = Math.sqrt(variance);
    return std > 0 ? ((results.actualScore - mean) / std).toFixed(1) : "∞";
  }, [results]);

  return (
    <div style={{ fontFamily: "'Inter', system-ui, sans-serif", background: "#0a0e17", color: "#c9d1d9", minHeight: "100vh", padding: "20px" }}>
      <div style={{ maxWidth: 780, margin: "0 auto" }}>

        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: 32 }}>
          <div style={{ fontSize: 11, letterSpacing: 4, textTransform: "uppercase", color: "#c9a227", opacity: 0.7, marginBottom: 8 }}>
            POF 2828 · Theophysics
          </div>
          <h1 style={{ fontFamily: "'Georgia', serif", fontSize: "1.8em", color: "#fff", margin: "0 0 6px" }}>
            Derivation Structure Stress Test
          </h1>
          <p style={{ fontSize: ".85em", color: "#8b949e", margin: 0 }}>
            Bayesian Monte Carlo · Bottom-Up Validation
          </p>
        </div>

        {/* Explanation */}
        <div style={{ background: "#111827", border: "1px solid rgba(201,162,39,.2)", borderRadius: 10, padding: "16px 20px", marginBottom: 24 }}>
          <p style={{ fontSize: ".85em", lineHeight: 1.7, margin: 0 }}>
            <strong style={{ color: "#c9a227" }}>The test:</strong> Each of the {TERMS.length} derived terms has a physics signature (equation type, domain tags).
            Each of the {PARENTS.length} parent laws has a physics signature. The actual assignment scores how well each term's physics matches its assigned parent.
            The Monte Carlo generates <em>N</em> random assignments and scores each one.
            <strong style={{ color: "#fff" }}> If the actual assignment scores higher than {">"}99.9% of random trials, the structure is not coincidence.</strong>
          </p>
        </div>

        {/* Controls */}
        <div style={{ display: "flex", gap: 16, alignItems: "center", marginBottom: 24, flexWrap: "wrap" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <label style={{ fontSize: ".8em", color: "#8b949e" }}>Trials:</label>
            <select value={nTrials} onChange={e => setNTrials(+e.target.value)}
              style={{ background: "#1a2035", color: "#c9d1d9", border: "1px solid #484f58", borderRadius: 6, padding: "6px 12px", fontSize: ".85em" }}>
              <option value={100}>100</option>
              <option value={500}>500</option>
              <option value={1000}>1,000</option>
              <option value={5000}>5,000</option>
              <option value={10000}>10,000</option>
            </select>
          </div>
          <button onClick={runSim} disabled={running}
            style={{ background: running ? "#484f58" : "#c9a227", color: "#0a0e17", border: "none", borderRadius: 6, padding: "8px 24px", fontSize: ".85em", fontWeight: 600, cursor: running ? "wait" : "pointer" }}>
            {running ? "Running..." : "Run Simulation"}
          </button>
          <div style={{ fontSize: ".8em", color: "#8b949e" }}>
            Actual score: <strong style={{ color: "#22c55e" }}>{actualScorePreview.toFixed(2)}</strong> / {TERMS.length}
          </div>
        </div>

        {/* Results */}
        {results && (
          <>
            {/* Big numbers */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 24 }}>
              {[
                { label: "Actual Score", value: results.actualScore.toFixed(2), color: "#22c55e" },
                { label: "p-value", value: results.pValue < 0.001 ? "<0.001" : results.pValue.toFixed(4), color: results.pValue < 0.01 ? "#22c55e" : "#ef4444" },
                { label: "Sigma (σ)", value: sigma + "σ", color: "#c9a227" },
                { label: "Beat Random", value: `${results.nTrials - results.exceedCount}/${results.nTrials}`, color: "#3b82f6" },
              ].map((item, i) => (
                <div key={i} style={{ background: "#111827", borderRadius: 10, padding: "16px 12px", textAlign: "center", border: "1px solid rgba(255,255,255,.06)" }}>
                  <div style={{ fontSize: ".65em", letterSpacing: 2, textTransform: "uppercase", color: "#8b949e", marginBottom: 6 }}>{item.label}</div>
                  <div style={{ fontFamily: "'Georgia', serif", fontSize: "1.5em", fontWeight: 700, color: item.color }}>{item.value}</div>
                </div>
              ))}
            </div>

            {/* Histogram */}
            <div style={{ background: "#111827", borderRadius: 10, padding: "20px 16px", marginBottom: 24, border: "1px solid rgba(255,255,255,.06)" }}>
              <div style={{ fontSize: ".75em", letterSpacing: 2, textTransform: "uppercase", color: "#8b949e", marginBottom: 12 }}>
                Score Distribution: Random vs Actual
              </div>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={results.bins} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
                  <XAxis dataKey="x" tick={{ fill: "#484f58", fontSize: 10 }} axisLine={{ stroke: "#484f58" }}
                    label={{ value: "Coherence Score", position: "insideBottom", offset: -10, fill: "#8b949e", fontSize: 11 }} />
                  <YAxis tick={{ fill: "#484f58", fontSize: 10 }} axisLine={{ stroke: "#484f58" }}
                    label={{ value: "Frequency", angle: -90, position: "insideLeft", offset: 10, fill: "#8b949e", fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ background: "#1a2035", border: "1px solid #484f58", borderRadius: 6, fontSize: ".8em" }}
                    labelStyle={{ color: "#c9a227" }}
                  />
                  <Bar dataKey="count" radius={[2, 2, 0, 0]}>
                    {results.bins.map((entry, i) => (
                      <Cell key={i} fill={entry.x >= results.actualScore - 0.3 && entry.x <= results.actualScore + 0.3 ? "#22c55e" : "rgba(59,130,246,.5)"} />
                    ))}
                  </Bar>
                  <ReferenceLine x={+results.actualScore.toFixed(1)} stroke="#22c55e" strokeWidth={2} strokeDasharray="4 4"
                    label={{ value: "ACTUAL", position: "top", fill: "#22c55e", fontSize: 11, fontWeight: 600 }} />
                </BarChart>
              </ResponsiveContainer>
              <p style={{ fontSize: ".78em", color: "#8b949e", textAlign: "center", marginTop: 8 }}>
                Blue = random assignment scores · Green line = actual assignment score
              </p>
            </div>

            {/* Interpretation */}
            <div style={{
              background: results.pValue < 0.001 ? "rgba(34,197,94,.06)" : results.pValue < 0.05 ? "rgba(234,179,8,.06)" : "rgba(239,68,68,.06)",
              border: `1px solid ${results.pValue < 0.001 ? "rgba(34,197,94,.25)" : results.pValue < 0.05 ? "rgba(234,179,8,.25)" : "rgba(239,68,68,.25)"}`,
              borderRadius: 10, padding: "16px 20px", marginBottom: 24
            }}>
              <div style={{ fontSize: ".75em", letterSpacing: 2, textTransform: "uppercase", color: results.pValue < 0.001 ? "#22c55e" : results.pValue < 0.05 ? "#eab308" : "#ef4444", fontWeight: 600, marginBottom: 8 }}>
                {results.pValue < 0.001 ? "✅ STRUCTURE IS REAL" : results.pValue < 0.05 ? "⚠️ SUGGESTIVE BUT NOT CONCLUSIVE" : "❌ NOT DISTINGUISHABLE FROM RANDOM"}
              </div>
              <p style={{ fontSize: ".85em", color: "#c9d1d9", lineHeight: 1.7, margin: 0 }}>
                {results.pValue < 0.001
                  ? `The actual term-to-parent assignment scores ${sigma}σ above the random distribution. Out of ${nTrials.toLocaleString()} random shuffles, ${results.exceedCount === 0 ? "ZERO" : results.exceedCount} matched or exceeded the actual score. The probability of this structure arising by chance is less than 0.1%. The derivation architecture is statistically real — the terms belong under their assigned parent laws more than random chance would predict.`
                  : results.pValue < 0.05
                  ? `The actual assignment outperforms most random shuffles, but the margin is not overwhelming. Some terms may be cross-law (assignable to multiple parents). This typically indicates that certain chains need tighter physics signatures.`
                  : `The actual assignment does not significantly outperform random. The term-to-parent structure may be too loose. Review which terms have ambiguous physics signatures.`
                }
              </p>
            </div>
          </>
        )}

        {/* Chain Breakdown */}
        <div style={{ background: "#111827", borderRadius: 10, padding: "20px", marginBottom: 24, border: "1px solid rgba(255,255,255,.06)" }}>
          <div style={{ fontSize: ".75em", letterSpacing: 2, textTransform: "uppercase", color: "#8b949e", marginBottom: 16 }}>
            Per-Chain Coherence (Actual Assignment)
          </div>
          {Object.entries(chainBreakdown).map(([name, data]) => {
            const pct = (data.actual / data.count * 100).toFixed(0);
            const parent = PARENTS.find(p => p.short === name);
            return (
              <div key={name} style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 10 }}>
                <div style={{ width: 80, fontSize: ".8em", color: parent?.color || "#8b949e", fontWeight: 600 }}>{name}</div>
                <div style={{ flex: 1, height: 8, background: "#1a2035", borderRadius: 4, overflow: "hidden" }}>
                  <div style={{ width: `${pct}%`, height: "100%", background: parent?.color || "#22c55e", borderRadius: 4, transition: "width .5s" }} />
                </div>
                <div style={{ width: 48, fontSize: ".78em", color: "#c9d1d9", textAlign: "right" }}>{pct}%</div>
                <div style={{ width: 40, fontSize: ".7em", color: "#484f58" }}>{data.count} terms</div>
              </div>
            );
          })}
        </div>

        {/* Term Detail Toggle */}
        <button onClick={() => setShowTerms(!showTerms)}
          style={{ background: "transparent", color: "#8b949e", border: "1px solid #484f58", borderRadius: 6, padding: "8px 16px", fontSize: ".8em", cursor: "pointer", marginBottom: 16 }}>
          {showTerms ? "Hide" : "Show"} All {TERMS.length} Terms + Tags
        </button>

        {showTerms && (
          <div style={{ background: "#111827", borderRadius: 10, padding: "16px", marginBottom: 24, border: "1px solid rgba(255,255,255,.06)", maxHeight: 500, overflowY: "auto" }}>
            {PARENTS.map(parent => (
              <div key={parent.id} style={{ marginBottom: 16 }}>
                <div style={{ fontSize: ".78em", fontWeight: 600, color: parent.color, marginBottom: 6 }}>
                  {parent.name} — tags: [{parent.tags.join(", ")}]
                </div>
                {TERMS.filter(t => t.parent === parent.id).map((term, i) => {
                  const parentTags = new Set(parent.tags);
                  const matchCount = term.tags.filter(t => parentTags.has(t)).length;
                  const score = (matchCount / term.tags.length * 100).toFixed(0);
                  return (
                    <div key={i} style={{ display: "flex", gap: 8, alignItems: "center", padding: "3px 0 3px 16px", fontSize: ".78em" }}>
                      <span style={{ color: "#c9d1d9", minWidth: 120 }}>{term.name}</span>
                      <span style={{ color: "#484f58" }}>[{term.tags.join(", ")}]</span>
                      <span style={{ marginLeft: "auto", color: +score === 100 ? "#22c55e" : +score >= 67 ? "#c9a227" : "#ef4444", fontWeight: 600 }}>{score}%</span>
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
        )}

        {/* Footer */}
        <div style={{ textAlign: "center", padding: "24px 0", borderTop: "1px solid rgba(255,255,255,.05)" }}>
          <p style={{ fontSize: ".7em", color: "#484f58" }}>
            Theophysics Derivation Stress Test · Bayesian Monte Carlo · Bottom-Up Validation
          </p>
          <p style={{ fontSize: ".65em", color: "#484f58" }}>
            David Lowe · POF 2828 · faiththruphysics.com
          </p>
        </div>
      </div>
    </div>
  );
}
