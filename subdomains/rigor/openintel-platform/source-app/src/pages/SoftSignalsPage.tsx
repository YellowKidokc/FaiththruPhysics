import { trpc } from "@/providers/trpc";
import Layout from "@/components/Layout";
import {
  Signal,
  BarChart3,
  Info,
} from "lucide-react";

export default function SoftSignalsPage() {
  const { data: fullCase, isLoading } = trpc.openintel.getFullCase.useQuery({ caseId: 1 });
  const { data: aggregateData } = trpc.scoring.computeSoftSignalsAggregate.useQuery({ caseId: 1 });

  if (isLoading || !fullCase) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full" />
        </div>
      </Layout>
    );
  }

  const signals = fullCase.softSignals;

  // Sort by score desc
  const sortedSignals = [...signals].sort((a, b) => parseFloat(b.score) - parseFloat(a.score));

  return (
    <Layout>
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Signal className="w-7 h-7 text-amber-400" />
          <h1 className="text-2xl font-bold text-white">Soft Signals</h1>
          <span className="px-2 py-0.5 text-xs bg-slate-800 text-slate-300 rounded-full font-mono">
            {signals.length} signals
          </span>
        </div>
        <p className="text-slate-400 text-sm max-w-3xl">
          14 structural indicators that assess the overall trustworthiness of a position.
          These are not direct evidence but meta-evidence about how the evidence behaves.
        </p>
      </div>

      {/* Aggregate Score */}
      {aggregateData && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-amber-400" />
              <span className="text-sm font-semibold text-white">Aggregate Signal Score</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-2xl font-bold text-amber-400">{aggregateData.totalScore}</span>
              <span className="text-sm text-slate-500">/ {aggregateData.maxPossible}</span>
              <span className={`ml-2 px-2 py-0.5 text-xs rounded-full font-medium ${
                aggregateData.percentage >= 70 ? "bg-emerald-500/15 text-emerald-400" :
                aggregateData.percentage >= 50 ? "bg-amber-500/15 text-amber-400" :
                "bg-red-500/15 text-red-400"
              }`}>
                {aggregateData.percentage}%
              </span>
            </div>
          </div>
          <div className="w-full bg-slate-800 rounded-full h-3 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all ${
                aggregateData.percentage >= 70 ? "bg-emerald-500" :
                aggregateData.percentage >= 50 ? "bg-amber-500" :
                "bg-red-500"
              }`}
              style={{ width: `${aggregateData.percentage}%` }}
            />
          </div>
        </div>
      )}

      {/* Signal Bars */}
      <div className="space-y-4">
        {sortedSignals.map((signal) => {
          const score = parseFloat(signal.score);
          const max = parseFloat(signal.maxScore);
          const pct = (score / max) * 100;
          const barColor = pct >= 80 ? "bg-emerald-500" : pct >= 60 ? "bg-amber-500" : pct >= 40 ? "bg-yellow-500" : "bg-red-500";

          return (
            <div key={signal.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-colors">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-sm font-semibold text-slate-200">{signal.signalName}</h3>
                    <span className="text-xs text-slate-600 font-mono">{signal.signalKey}</span>
                  </div>
                  <p className="text-xs text-slate-500 mt-0.5">{signal.description}</p>
                </div>
                <div className="text-right shrink-0">
                  <div className="text-lg font-bold text-white">{score}</div>
                  <div className="text-xs text-slate-500">/ {max}</div>
                </div>
              </div>

              {/* Bar */}
              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden mb-2">
                <div className={`h-full rounded-full transition-all ${barColor}`} style={{ width: `${pct}%` }} />
              </div>

              {/* Justification */}
              {signal.justification && (
                <p className="text-xs text-slate-400 mt-2"><strong className="text-slate-500">Justification:</strong> {signal.justification}</p>
              )}
              {signal.evidenceRefs && (
                <p className="text-xs text-slate-600 mt-1"><strong>Refs:</strong> {signal.evidenceRefs}</p>
              )}
            </div>
          );
        })}
      </div>

      {/* Legend */}
      <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center gap-2 mb-3">
          <Info className="w-4 h-4 text-slate-500" />
          <span className="text-sm font-semibold text-slate-400">Signal Scoring Guide</span>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-emerald-500" />
            <span className="text-slate-400">8-10: Strong signal</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-amber-500" />
            <span className="text-slate-400">6-7: Moderate signal</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <span className="text-slate-400">4-5: Weak signal</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <span className="text-slate-400">0-3: No signal / Negative</span>
          </div>
        </div>
      </div>
    </Layout>
  );
}
