import { trpc } from "@/providers/trpc";
import Layout from "@/components/Layout";
import {
  Database,
  Grid3X3,
  Users,
  Clock,
  Signal,
  ListChecks,
  Gavel,
  Shield,
  FlaskConical,
  AlertTriangle,
  CheckCircle,
  XCircle,
  BarChart3,
} from "lucide-react";
import { Link } from "react-router";

const tierColors: Record<string, string> = {
  T1: "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
  T2: "bg-blue-500/15 text-blue-400 border-blue-500/30",
  T3: "bg-amber-500/15 text-amber-400 border-amber-500/30",
  T4: "bg-orange-500/15 text-orange-400 border-orange-500/30",
  T5: "bg-red-500/15 text-red-400 border-red-500/30",
};

const statCards = [
  { label: "Evidence Items", value: "57", icon: Database, path: "/evidence", color: "text-emerald-400", bg: "bg-emerald-500/10" },
  { label: "Fakery Constraints", value: "F1-F10", icon: Grid3X3, path: "/fakery", color: "text-rose-400", bg: "bg-rose-500/10" },
  { label: "Population Density", value: "8 Skills", icon: Users, path: "/population", color: "text-violet-400", bg: "bg-violet-500/10" },
  { label: "Timeline Events", value: "18", icon: Clock, path: "/timeline", color: "text-cyan-400", bg: "bg-cyan-500/10" },
  { label: "Soft Signals", value: "14", icon: Signal, path: "/signals", color: "text-amber-400", bg: "bg-amber-500/10" },
  { label: "Protocol Steps", value: "10", icon: ListChecks, path: "/protocol", color: "text-sky-400", bg: "bg-sky-500/10" },
];

export default function Home() {
  const { data: fullCase, isLoading } = trpc.openintel.getFullCase.useQuery({ caseId: 1 });
  const { data: ocsData } = trpc.scoring.computeOCS.useQuery({ caseId: 1 });
  const { data: evidenceStats } = trpc.scoring.computeEvidenceStats.useQuery({ caseId: 1 });
  const { data: fakeryData } = trpc.scoring.computeFakeryCompound.useQuery({ caseId: 1 });
  const { data: popDensityData } = trpc.scoring.computePopDensityCompound.useQuery({ caseId: 1 });

  if (isLoading || !fullCase) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full" />
        </div>
      </Layout>
    );
  }

  const { case: caseData, evidence, fakeryMatrix, protocolSteps } = fullCase;

  const t1Count = evidence.filter(e => e.tier === "T1").length;
  const t2Count = evidence.filter(e => e.tier === "T2").length;
  const t3Count = evidence.filter(e => e.tier === "T3").length;

  return (
    <Layout>
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Shield className="w-8 h-8 text-amber-400" />
          <h1 className="text-3xl font-bold text-white">OpenIntel</h1>
          <span className="px-2 py-0.5 text-xs bg-amber-500/15 text-amber-400 border border-amber-500/30 rounded-full font-medium">
            Truth-Finding Protocol
          </span>
        </div>
        <p className="text-slate-400 max-w-2xl">
          Universal framework for adversarial truth-resolution. A systematic, evidence-based methodology
          for resolving polarized disputes between opposing factions using the scientific method.
        </p>
      </div>

      {/* Case Summary */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <FlaskConical className="w-6 h-6 text-amber-400" />
              <h2 className="text-xl font-semibold text-white">{caseData.canonicalTitle}</h2>
              <span className="px-2 py-0.5 text-xs bg-slate-800 text-slate-300 rounded-full font-mono">
                {caseData.caseId}
              </span>
            </div>
            <p className="text-slate-400 text-sm max-w-3xl">{caseData.category}</p>
            <p className="text-slate-500 text-sm mt-2">{caseData.notes}</p>
          </div>
          <Link
            to="/verdict"
            className="flex items-center gap-2 px-4 py-2 bg-amber-500/10 border border-amber-500/30 text-amber-400 rounded-lg hover:bg-amber-500/20 transition-colors text-sm font-medium"
          >
            <Gavel size={16} />
            View Verdict
          </Link>
        </div>

        {/* Key metrics row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/50">
            <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">Evidence Quality</div>
            <div className="text-2xl font-bold text-emerald-400">{evidenceStats?.evidenceQuality ? (evidenceStats.evidenceQuality * 100).toFixed(0) : 0}%</div>
            <div className="text-xs text-slate-500 mt-1">{t1Count} T1 / {t2Count} T2 / {t3Count} T3</div>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/50">
            <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">Fakery Probability</div>
            <div className="text-2xl font-bold text-rose-400">
              {fakeryData?.verdict === "FORGERY_IMPOSSIBLE" ? "Zero" : fakeryData?.probabilityString || "N/A"}
            </div>
            <div className="text-xs text-slate-500 mt-1">{fakeryData?.verdict === "FORGERY_IMPOSSIBLE" ? "5 IMPOSSIBLE + 5 EXTREME" : "F1-F10 constraints"}</div>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/50">
            <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">Population Density</div>
            <div className="text-2xl font-bold text-violet-400">
              {popDensityData?.verdict === "POPULATION_ZERO" ? "Zero" : popDensityData?.probabilityString || "N/A"}
            </div>
            <div className="text-xs text-slate-500 mt-1">Required forger population</div>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/50">
            <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">Protocol Complete</div>
            <div className="text-2xl font-bold text-sky-400">{protocolSteps.filter(s => s.status === "COMPLETED").length}/10</div>
            <div className="text-xs text-slate-500 mt-1">All steps completed</div>
          </div>
        </div>

        {/* OCS Score Bar */}
        {ocsData && (
          <div className="mt-6 bg-slate-800/50 rounded-lg p-4 border border-slate-700/50">
            <div className="flex items-center justify-between mb-2">
              <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Overall Case Score (OCS)</div>
              <div className="flex items-center gap-2">
                <span className={`text-lg font-bold ${
                  ocsData.ocsRaw >= 0.65 ? 'text-emerald-400' :
                  ocsData.ocsRaw >= 0.45 ? 'text-amber-400' : 'text-red-400'
                }`}>{ocsData.ocs}%</span>
                <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${
                  ocsData.ocsRaw >= 0.65 ? 'bg-emerald-500/15 text-emerald-400' :
                  ocsData.ocsRaw >= 0.45 ? 'bg-amber-500/15 text-amber-400' :
                  'bg-red-500/15 text-red-400'
                }`}>{ocsData.verdictLabel}</span>
              </div>
            </div>
            <div className="w-full bg-slate-700 rounded-full h-3 overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-1000 ${
                  ocsData.ocsRaw >= 0.65 ? 'bg-emerald-500' :
                  ocsData.ocsRaw >= 0.45 ? 'bg-amber-500' :
                  'bg-red-500'
                }`}
                style={{ width: `${ocsData.ocs}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-slate-500 mt-1">
              <span>0%</span>
              <span>Debauched</span>
              <span className="text-slate-400">50%</span>
              <span>Disputed</span>
              <span>100%</span>
              <span>Proven</span>
            </div>
          </div>
        )}
      </div>

      {/* Stat Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
        {statCards.map((card) => {
          const Icon = card.icon;
          return (
            <Link
              key={card.path}
              to={card.path}
              className="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-slate-700 hover:bg-slate-800/30 transition-all group"
            >
              <div className="flex items-center justify-between mb-3">
                <div className={`p-2 rounded-lg ${card.bg}`}>
                  <Icon size={20} className={card.color} />
                </div>
                <BarChart3 size={16} className="text-slate-600 group-hover:text-slate-400 transition-colors" />
              </div>
              <div className="text-2xl font-bold text-white">{card.value}</div>
              <div className="text-sm text-slate-400">{card.label}</div>
            </Link>
          );
        })}
      </div>

      {/* Quick Preview: Top Evidence & Fakery Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top T1 Evidence */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <CheckCircle size={18} className="text-emerald-400" />
              <h3 className="font-semibold text-white">Strongest T1 Evidence</h3>
            </div>
            <Link to="/evidence" className="text-xs text-amber-400 hover:text-amber-300">View All</Link>
          </div>
          <div className="space-y-3">
            {evidence.filter(e => e.tier === "T1").slice(0, 5).map((item, i) => (
              <div key={i} className="flex items-start gap-3 text-sm">
                <span className={`px-1.5 py-0.5 text-xs rounded border font-mono shrink-0 mt-0.5 ${tierColors[item.tier]}`}>
                  {item.tier}
                </span>
                <div>
                  <div className="text-slate-200 font-medium">{item.evidenceName}</div>
                  <div className="text-slate-500 text-xs mt-0.5">{item.source}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Fakery Quick View */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <XCircle size={18} className="text-rose-400" />
              <h3 className="font-semibold text-white">Fakery Matrix Summary</h3>
            </div>
            <Link to="/fakery" className="text-xs text-amber-400 hover:text-amber-300">View All</Link>
          </div>
          <div className="space-y-2">
            {fakeryMatrix.slice(0, 5).map((item, i) => (
              <div key={i} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <span className="text-slate-500 font-mono text-xs">{item.constraintId}</span>
                  <span className="text-slate-300">{item.constraintName}</span>
                </div>
                <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${
                  item.rating === "IMPOSSIBLE" ? "bg-rose-500/15 text-rose-400" :
                  item.rating === "EXTREME" ? "bg-orange-500/15 text-orange-400" :
                  "bg-slate-700 text-slate-400"
                }`}>
                  {item.rating}
                </span>
              </div>
            ))}
          </div>
          {fakeryData && (
            <div className="mt-4 p-3 bg-rose-500/5 border border-rose-500/20 rounded-lg">
              <div className="flex items-center gap-2">
                <AlertTriangle size={14} className="text-rose-400" />
                <span className="text-xs text-rose-400 font-medium">Compound Probability: {fakeryData.probabilityString}</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Protocol Status */}
      <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <ListChecks size={18} className="text-sky-400" />
          <h3 className="font-semibold text-white">10-Step Protocol Status</h3>
        </div>
        <div className="grid grid-cols-5 md:grid-cols-10 gap-2">
          {protocolSteps.map((step) => (
            <Link
              key={step.id}
              to="/protocol"
              className={`p-2 rounded-lg border text-center transition-all hover:scale-105 ${
                step.status === "COMPLETED"
                  ? "bg-emerald-500/10 border-emerald-500/30"
                  : step.status === "IN_PROGRESS"
                  ? "bg-amber-500/10 border-amber-500/30"
                  : "bg-slate-800 border-slate-700"
              }`}
            >
              <div className={`text-lg font-bold ${
                step.status === "COMPLETED" ? "text-emerald-400" :
                step.status === "IN_PROGRESS" ? "text-amber-400" : "text-slate-500"
              }`}>{step.stepNumber}</div>
              <div className="text-[10px] text-slate-500 leading-tight mt-0.5 hidden md:block">
                {step.stepKey.split('_').map(w => w[0]).join('')}
              </div>
            </Link>
          ))}
        </div>
      </div>
    </Layout>
  );
}
