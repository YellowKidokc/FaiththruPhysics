import { trpc } from "@/providers/trpc";
import Layout from "@/components/Layout";
import { useState } from "react";
import {
  Grid3X3,
  AlertTriangle,
  XCircle,
  ChevronDown,
  ChevronUp,
  Info,
  Zap,
  ShieldAlert,
  Ban,
  Calculator,
} from "lucide-react";

const ratingConfig: Record<string, { color: string; bg: string; icon: React.ElementType }> = {
  IMPOSSIBLE: { color: "text-rose-400", bg: "bg-rose-500/10 border-rose-500/30", icon: Ban },
  EXTREME: { color: "text-orange-400", bg: "bg-orange-500/10 border-orange-500/30", icon: ShieldAlert },
  HIGH: { color: "text-amber-400", bg: "bg-amber-500/10 border-amber-500/30", icon: AlertTriangle },
  MODERATE: { color: "text-yellow-400", bg: "bg-yellow-500/10 border-yellow-500/30", icon: Info },
  LOW: { color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/30", icon: Info },
};

export default function FakeryMatrixPage() {
  const { data: fullCase, isLoading } = trpc.openintel.getFullCase.useQuery({ caseId: 1 });
  const { data: fakeryData, isLoading: fakeryLoading } = trpc.scoring.computeFakeryCompound.useQuery({ caseId: 1 });
  const [expandedId, setExpandedId] = useState<number | null>(null);

  if (isLoading || !fullCase) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full" />
        </div>
      </Layout>
    );
  }

  const impossibleCount = fullCase.fakeryMatrix.filter(f => f.rating === "IMPOSSIBLE").length;
  const extremeCount = fullCase.fakeryMatrix.filter(f => f.rating === "EXTREME").length;

  return (
    <Layout>
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Grid3X3 className="w-7 h-7 text-rose-400" />
          <h1 className="text-2xl font-bold text-white">Fakery Matrix</h1>
          <span className="px-2 py-0.5 text-xs bg-rose-500/10 text-rose-400 border border-rose-500/30 rounded-full font-mono">
            F1-F10
          </span>
        </div>
        <p className="text-slate-400 text-sm max-w-3xl">
          <strong className="text-slate-300">Forced Inversion:</strong> If the Shroud is FAKE, ALL of the following constraints
          must be simultaneously true. Each constraint is rated by fabrication cost and possibility.
          Compound probability is the product of all individual probabilities.
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Compound Probability */}
        <div className="bg-slate-900 border border-rose-500/30 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <Calculator className="w-5 h-5 text-rose-400" />
            <span className="text-sm text-slate-400">Compound Probability</span>
          </div>
          {fakeryLoading ? (
            <div className="animate-pulse h-8 bg-slate-800 rounded" />
          ) : (
            <>
              <div className="text-3xl font-bold text-rose-400">{fakeryData?.probabilityString || "Calculating..."}</div>
              <div className="text-xs text-slate-500 mt-1">
                Product of F1 through F10 possibility scores
              </div>
            </>
          )}
        </div>

        {/* Rating Distribution */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <Zap className="w-5 h-5 text-amber-400" />
            <span className="text-sm text-slate-400">Rating Distribution</span>
          </div>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs text-rose-400">IMPOSSIBLE</span>
              <div className="flex items-center gap-2">
                <div className="w-24 bg-slate-800 rounded-full h-2 overflow-hidden">
                  <div className="bg-rose-500 h-full rounded-full" style={{ width: `${(impossibleCount / 10) * 100}%` }} />
                </div>
                <span className="text-sm font-bold text-white">{impossibleCount}</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-orange-400">EXTREME</span>
              <div className="flex items-center gap-2">
                <div className="w-24 bg-slate-800 rounded-full h-2 overflow-hidden">
                  <div className="bg-orange-500 h-full rounded-full" style={{ width: `${(extremeCount / 10) * 100}%` }} />
                </div>
                <span className="text-sm font-bold text-white">{extremeCount}</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-500">Other</span>
              <span className="text-sm font-bold text-slate-500">{10 - impossibleCount - extremeCount}</span>
            </div>
          </div>
        </div>

        {/* Verdict */}
        <div className="bg-rose-500/5 border border-rose-500/20 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <XCircle className="w-5 h-5 text-rose-400" />
            <span className="text-sm text-slate-400">Forced Inversion Verdict</span>
          </div>
          <div className="text-xl font-bold text-rose-300">Forgery Functionally Impossible</div>
          <div className="text-xs text-slate-500 mt-1">
            5 constraints rated IMPOSSIBLE + 5 rated EXTREME. Even at 1/100 per factor,
            compound probability = 1 in 10<sup>20</sup>.
          </div>
        </div>
      </div>

      {/* Blood-Image Sequence Banner */}
      <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-xl p-5 mb-6">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <div className="text-sm font-semibold text-emerald-300">Strongest Single Finding: Blood-Image Sequence</div>
            <p className="text-sm text-slate-400 mt-1">
              STURP documented that blood went onto cloth FIRST, image formed SECOND. The image is NOT present
              under bloodstains. <strong className="text-slate-300">Every artistic process creates image first, adds blood second.</strong> No known
              technique produces blood-first, image-second. This single finding eliminates every forgery hypothesis.
            </p>
            <div className="flex gap-3 mt-2">
              <span className="text-xs text-emerald-400">Peer-reviewed</span>
              <span className="text-xs text-emerald-400">Published</span>
              <span className="text-xs text-emerald-400">Never overturned</span>
              <span className="text-xs text-emerald-400">Never seriously challenged</span>
            </div>
          </div>
        </div>
      </div>

      {/* F1-F10 Constraints */}
      <div className="space-y-3">
        {fullCase.fakeryMatrix.map((item) => {
          const isExpanded = expandedId === item.id;
          const config = ratingConfig[item.rating] || ratingConfig.EXTREME;
          const RatingIcon = config.icon;

          return (
            <div
              key={item.id}
              className={`rounded-xl border overflow-hidden transition-all ${
                item.rating === "IMPOSSIBLE"
                  ? "bg-rose-950/20 border-rose-500/20"
                  : "bg-slate-900 border-slate-800"
              }`}
            >
              {/* Header row */}
              <button
                onClick={() => setExpandedId(isExpanded ? null : item.id)}
                className="w-full px-4 py-3 flex items-center gap-4 text-left"
              >
                <span className="text-lg font-bold text-slate-400 font-mono w-8">{item.constraintId}</span>

                <div className={`p-1.5 rounded-lg ${config.bg}`}>
                  <RatingIcon size={14} className={config.color} />
                </div>

                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-slate-200">{item.constraintName}</div>
                </div>

                <span className={`px-2 py-0.5 text-xs rounded-full font-medium border ${config.bg} ${config.color}`}>
                  {item.rating}
                </span>

                <span className="text-xs text-slate-500 font-mono w-16 text-right">
                  {item.possibilityScore === "0" ? "0" : item.possibilityScore}
                </span>

                {isExpanded ? <ChevronUp size={16} className="text-slate-500" /> : <ChevronDown size={16} className="text-slate-500" />}
              </button>

              {/* Expanded */}
              {isExpanded && (
                <div className="px-4 pb-4 border-t border-slate-800 pt-3 space-y-3">
                  <p className="text-sm text-slate-300 leading-relaxed">{item.description}</p>
                  {item.fabricationCostDescription && (
                    <div className="flex items-start gap-2">
                      <span className="text-xs text-rose-500 font-semibold uppercase tracking-wider shrink-0 mt-0.5">Fabrication Cost:</span>
                      <span className="text-sm text-slate-400">{item.fabricationCostDescription}</span>
                    </div>
                  )}
                  {item.possibilityJustification && (
                    <div className="flex items-start gap-2">
                      <span className="text-xs text-amber-500 font-semibold uppercase tracking-wider shrink-0 mt-0.5">Why This Rating:</span>
                      <span className="text-sm text-slate-400">{item.possibilityJustification}</span>
                    </div>
                  )}
                  <div className="pt-2 border-t border-slate-800 flex items-center gap-4">
                    <span className="text-xs text-slate-600">
                      Fabrication Cost: <span className="text-slate-400 font-medium">{item.fabricationCost}</span>
                    </span>
                    <span className="text-xs text-slate-600">
                      Possibility Score: <span className="font-mono text-slate-400">{item.possibilityScore}</span>
                    </span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Methodology note */}
      <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center gap-2 mb-2">
          <Info size={16} className="text-slate-500" />
          <span className="text-sm font-semibold text-slate-400">Methodology Note</span>
        </div>
        <p className="text-sm text-slate-500">
          The Fakery Matrix uses <strong className="text-slate-400">conservative estimates</strong>. Even at generous
          1/100 per factor, ten coupled constraints yield 1 in 10<sup>20</sup>. With five constraints rated
          IMPOSSIBLE (possibility score = 0), the compound probability is functionally zero regardless of
          the other five ratings. This is the mathematical expression of the forced inversion test.
        </p>
      </div>
    </Layout>
  );
}
