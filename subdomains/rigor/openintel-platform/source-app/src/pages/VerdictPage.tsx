import { trpc } from "@/providers/trpc";
import Layout from "@/components/Layout";
import {
  Gavel,
  CheckCircle,
  AlertTriangle,
  XCircle,
  Scale,
  Info,
  Shield,
  ChevronRight,
} from "lucide-react";

const verdictConfig: Record<string, { color: string; bg: string; label: string; icon: React.ElementType }> = {
  PROVEN: { color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/30", label: "Proven", icon: CheckCircle },
  PARTIALLY_PROVEN: { color: "text-sky-400", bg: "bg-sky-500/10 border-sky-500/30", label: "Partially Proven", icon: CheckCircle },
  DISPUTED: { color: "text-amber-400", bg: "bg-amber-500/10 border-amber-500/30", label: "Disputed", icon: AlertTriangle },
  UNPROVEN: { color: "text-orange-400", bg: "bg-orange-500/10 border-orange-500/30", label: "Unproven", icon: AlertTriangle },
  DEBUNKED: { color: "text-rose-400", bg: "bg-rose-500/10 border-rose-500/30", label: "Debunked", icon: XCircle },
};

export default function VerdictPage() {
  const { data: fullCase, isLoading } = trpc.openintel.getFullCase.useQuery({ caseId: 1 });
  const { data: ocsData, isLoading: ocsLoading } = trpc.scoring.computeOCS.useQuery({ caseId: 1 });
  const { data: evidenceStats } = trpc.scoring.computeEvidenceStats.useQuery({ caseId: 1 });
  const { data: fakeryData } = trpc.scoring.computeFakeryCompound.useQuery({ caseId: 1 });
  const { data: popDensityData } = trpc.scoring.computePopDensityCompound.useQuery({ caseId: 1 });
  const { data: signalsData } = trpc.scoring.computeSoftSignalsAggregate.useQuery({ caseId: 1 });

  if (isLoading || !fullCase || ocsLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full" />
        </div>
      </Layout>
    );
  }

  const verdict = verdictConfig[ocsData?.verdict || "DISPUTED"];
  const VerdictIcon = verdict?.icon || AlertTriangle;

  return (
    <Layout>
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Gavel className="w-7 h-7 text-amber-400" />
          <h1 className="text-2xl font-bold text-white">Verdict Dashboard</h1>
        </div>
        <p className="text-slate-400 text-sm">Overall Case Score (OCS) computation with weighted component analysis.</p>
      </div>

      {/* Main Verdict Card */}
      <div className={`border rounded-xl p-8 mb-6 ${verdict.bg}`}>
        <div className="flex items-center gap-4 mb-4">
          <VerdictIcon size={32} className={verdict.color} />
          <div>
            <div className={`text-xs uppercase tracking-wider font-semibold ${verdict.color}`}>OpenIntel Verdict</div>
            <div className="text-3xl font-bold text-white">{verdict.label}</div>
          </div>
        </div>

        {/* OCS Big Number */}
        <div className="flex items-end gap-3 mb-4">
          <span className="text-6xl font-bold text-white">{ocsData?.ocs}%</span>
          <span className="text-sm text-slate-500 mb-2">OCS</span>
        </div>

        {/* OCS Bar */}
        <div className="w-full bg-slate-800/50 rounded-full h-4 overflow-hidden mb-2">
          <div
            className={`h-full rounded-full transition-all ${
              (ocsData?.ocsRaw || 0) >= 0.65 ? "bg-emerald-500" :
              (ocsData?.ocsRaw || 0) >= 0.45 ? "bg-amber-500" :
              "bg-red-500"
            }`}
            style={{ width: `${ocsData?.ocs || 0}%` }}
          />
        </div>
        <div className="flex justify-between text-xs text-slate-500">
          <span>0% (Debunked)</span>
          <span>50% (Disputed)</span>
          <span>100% (Proven)</span>
        </div>
      </div>

      {/* Component Breakdown */}
      {ocsData?.components && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
          <div className="flex items-center gap-2 mb-4">
            <Scale className="w-5 h-5 text-amber-400" />
            <h2 className="text-lg font-semibold text-white">OCS Component Breakdown</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Evidence Quality */}
            <ComponentBar
              label="Evidence Quality (E_qual)"
              value={ocsData.components.evidenceQuality}
              weight={ocsData.weights.evidenceQuality}
              color="bg-emerald-500"
              description={`${evidenceStats?.t1Count || 0} T1 + ${evidenceStats?.t2Count || 0} T2 + ${evidenceStats?.t3Count || 0} T3 out of ${evidenceStats?.total || 0} total items`}
            />
            {/* Fakery Score */}
            <ComponentBar
              label="Fakery Impossibility (F_score)"
              value={ocsData.components.fakeryScore}
              weight={ocsData.weights.fakeryScore}
              color="bg-rose-500"
              description={fakeryData?.probabilityString || "F1-F10 compound probability"}
            />
            {/* Population Density */}
            <ComponentBar
              label="Population Density (P_score)"
              value={ocsData.components.popScore}
              weight={ocsData.weights.popScore}
              color="bg-violet-500"
              description={popDensityData?.probabilityString || "8 skills, 7 with zero density"}
            />
            {/* Soft Signals */}
            <ComponentBar
              label="Soft Signals (S_score)"
              value={ocsData.components.signalScore}
              weight={ocsData.weights.signalScore}
              color="bg-amber-500"
              description={`${signalsData?.totalScore || 0} / ${signalsData?.maxPossible || 0} aggregate`}
            />
          </div>

          {/* Formula */}
          <div className="mt-4 p-3 bg-slate-800/50 rounded-lg">
            <div className="text-xs text-slate-500 font-mono">
              OCS = (E_qual x 0.{ocsData.weights.evidenceQuality}) +
              (F_score x 0.{ocsData.weights.fakeryScore}) +
              (P_score x 0.{ocsData.weights.popScore}) +
              (S_score x 0.{ocsData.weights.signalScore}) -
              (C_penalty x 0.{ocsData.weights.contradictionPenalty})
            </div>
          </div>
        </div>
      )}

      {/* What Would Change This Rating */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Info className="w-5 h-5 text-sky-400" />
          <h2 className="text-lg font-semibold text-white">What Would Change This Rating</h2>
        </div>
        <div className="space-y-3">
          <div className="flex items-start gap-3 text-sm">
            <ChevronRight size={16} className="text-emerald-400 shrink-0 mt-0.5" />
            <p className="text-slate-400">
              <strong className="text-slate-300">C-14 dating from a clean, representative sample</strong> showing
              medieval date (1260-1390 CE) would reduce OCS by ~25 points. The update commitment is clear.
            </p>
          </div>
          <div className="flex items-start gap-3 text-sm">
            <ChevronRight size={16} className="text-emerald-400 shrink-0 mt-0.5" />
            <p className="text-slate-400">
              <strong className="text-slate-300">Replication of all Shroud image properties</strong> by a known
              physical/chemical process would reduce fakery score to zero, dropping OCS by ~20 points.
            </p>
          </div>
          <div className="flex items-start gap-3 text-sm">
            <ChevronRight size={16} className="text-emerald-400 shrink-0 mt-0.5" />
            <p className="text-slate-400">
              <strong className="text-slate-300">Identification of a plausible forger</strong> with documented
              access to all required capabilities would increase population density score significantly.
            </p>
          </div>
          <div className="flex items-start gap-3 text-sm">
            <ChevronRight size={16} className="text-rose-400 shrink-0 mt-0.5" />
            <p className="text-slate-400">
              <strong className="text-slate-300">Evidence of blood-image sequence being artifact</strong> (i.e., image-first,
              blood-second mechanism exists) would fundamentally challenge the strongest single finding.
            </p>
          </div>
        </div>
      </div>

      {/* Evidence Asymmetry */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Scale className="w-5 h-5 text-amber-400" />
          <h2 className="text-lg font-semibold text-white">Evidence Asymmetry</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-rose-500/5 border border-rose-500/20 rounded-lg p-4">
            <div className="text-xs text-rose-400 font-semibold uppercase tracking-wider mb-2">Against Authenticity</div>
            <ul className="space-y-2 text-sm text-slate-400">
              <li className="flex items-start gap-2">
                <XCircle size={14} className="text-rose-400 shrink-0 mt-0.5" />
                1 compromised C-14 test (contaminated sample)
              </li>
              <li className="flex items-start gap-2">
                <XCircle size={14} className="text-rose-400 shrink-0 mt-0.5" />
                1 debunked pigment claim (McCrone, overruled by STURP)
              </li>
              <li className="flex items-start gap-2">
                <XCircle size={14} className="text-rose-400 shrink-0 mt-0.5" />
                1 hearsay memo (d'Arcis, draft, possibly never sent)
              </li>
              <li className="flex items-start gap-2">
                <XCircle size={14} className="text-rose-400 shrink-0 mt-0.5" />
                1 non-hypothesis ("someone could have done it somehow")
              </li>
            </ul>
            <div className="mt-3 text-xs text-rose-400 font-medium">Tier: T3-T5 | Weak evidence base</div>
          </div>
          <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-lg p-4">
            <div className="text-xs text-emerald-400 font-semibold uppercase tracking-wider mb-2">For Authenticity</div>
            <ul className="space-y-2 text-sm text-slate-400">
              <li className="flex items-start gap-2">
                <CheckCircle size={14} className="text-emerald-400 shrink-0 mt-0.5" />
                Material Science: linen, 2-micron depth, no pigments, fires survived
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle size={14} className="text-emerald-400 shrink-0 mt-0.5" />
                Hematology: Type AB, pre/post-mortem, blood-image sequence
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle size={14} className="text-emerald-400 shrink-0 mt-0.5" />
                Imaging: 3D encoding, photographic negative, VUV replication
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle size={14} className="text-emerald-400 shrink-0 mt-0.5" />
                Pathology: 700+ wounds, wrist nails, forensic accuracy
              </li>
            </ul>
            <div className="mt-3 text-xs text-emerald-400 font-medium">8 domains | 57 items | 30 T1 + 17 T2</div>
          </div>
        </div>
        <div className="mt-4 p-3 bg-amber-500/5 border border-amber-500/10 rounded-lg">
          <p className="text-sm text-slate-400 text-center">
            <strong className="text-slate-300">This is not symmetric.</strong> The skeptical case is thin.
            The authenticity case is deep, convergent, and cross-domain.
          </p>
        </div>
      </div>

      {/* Final statement */}
      <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-3">
          <Shield className="w-6 h-6 text-amber-400" />
          <h2 className="text-lg font-semibold text-amber-300">Methodological Statement</h2>
        </div>
        <p className="text-sm text-slate-400 leading-relaxed">
          The OpenIntel Truth-Finding Protocol does not claim to prove religious claims. It evaluates
          <strong className="text-slate-300"> evidence quality, coherence, and the impossibility of alternative explanations</strong>.
          The Shroud of Turin case demonstrates that across 8 independent domains of evidence, the forgery hypothesis
          requires a forger with a skill set that has a population density of zero in any known historical period.
          The authenticity hypothesis explains more with less, survives forced inversion, and passes the Solomon Test.
          This is what the evidence says — regardless of what anyone wishes it said.
        </p>
      </div>
    </Layout>
  );
}

// Component Bar sub-component
function ComponentBar({ label, value, weight, color, description }: {
  label: string;
  value: number;
  weight: number;
  color: string;
  description: string;
}) {
  return (
    <div className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-slate-300">{label}</span>
        <div className="flex items-center gap-2">
          <span className="text-lg font-bold text-white">{value}%</span>
          <span className="text-xs text-slate-500">(w:{weight}%)</span>
        </div>
      </div>
      <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden mb-2">
        <div className={`${color} h-full rounded-full`} style={{ width: `${value}%` }} />
      </div>
      <p className="text-xs text-slate-500">{description}</p>
    </div>
  );
}
