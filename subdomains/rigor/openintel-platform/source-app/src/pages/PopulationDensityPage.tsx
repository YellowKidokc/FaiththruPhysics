import { trpc } from "@/providers/trpc";
import Layout from "@/components/Layout";
import {
  Users,
  AlertTriangle,
  Ban,
  Info,
  ChevronRight,
  ShieldAlert,
  UserX,
  BarChart3,
} from "lucide-react";

const confidenceColors: Record<string, string> = {
  HIGH: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
  MEDIUM: "bg-amber-500/10 text-amber-400 border-amber-500/20",
  LOW: "bg-slate-700 text-slate-400 border-slate-600",
};

export default function PopulationDensityPage() {
  const { data: fullCase, isLoading } = trpc.openintel.getFullCase.useQuery({ caseId: 1 });
  const { data: popDensityData, isLoading: pdLoading } = trpc.scoring.computePopDensityCompound.useQuery({ caseId: 1 });

  if (isLoading || !fullCase) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full" />
        </div>
      </Layout>
    );
  }

  const zeroCount = fullCase.populationDensity.filter(p => p.densityScore === "0").length;

  return (
    <Layout>
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Users className="w-7 h-7 text-violet-400" />
          <h1 className="text-2xl font-bold text-white">Population Density Test</h1>
        </div>
        <p className="text-slate-400 text-sm max-w-3xl">
          <strong className="text-slate-300">Universal Truth-Finding Module:</strong> For any claim, what is the
          probability that a person with the EXACT required set of skills, knowledge, access, and motive existed
          in the right place at the right time? The compound probability is the product of all capability densities
          required in ONE person.
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-violet-500/5 border border-violet-500/20 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <BarChart3 className="w-5 h-5 text-violet-400" />
            <span className="text-sm text-slate-400">Compound Probability</span>
          </div>
          {pdLoading ? (
            <div className="animate-pulse h-8 bg-slate-800 rounded" />
          ) : (
            <>
              <div className="text-3xl font-bold text-violet-400">
                {popDensityData?.verdict === "POPULATION_ZERO" ? "Zero" : popDensityData?.probabilityString}
              </div>
              <div className="text-xs text-slate-500 mt-1">
                {popDensityData?.verdict === "POPULATION_ZERO"
                  ? "Required forger population does not exist"
                  : "Product of all capability density scores"}
              </div>
            </>
          )}
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <UserX className="w-5 h-5 text-rose-400" />
            <span className="text-sm text-slate-400">Zero-Density Skills</span>
          </div>
          <div className="text-3xl font-bold text-rose-400">{zeroCount} / {fullCase.populationDensity.length}</div>
          <div className="text-xs text-slate-500 mt-1">
            Capabilities with population density of zero
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <ShieldAlert className="w-5 h-5 text-amber-400" />
            <span className="text-sm text-slate-400">Verdict</span>
          </div>
          <div className="text-xl font-bold text-rose-300">Forgery Population Does Not Exist</div>
          <div className="text-xs text-slate-500 mt-1">
            Zero required skills × any population estimate = Zero
          </div>
        </div>
      </div>

      {/* Required Forger Profile */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Users className="w-5 h-5 text-violet-400" />
          <h2 className="text-lg font-semibold text-white">Required Forger Profile</h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-800 text-slate-500 text-xs uppercase tracking-wider">
                <th className="text-left py-2 pr-4">#</th>
                <th className="text-left py-2 pr-4">Capability Required</th>
                <th className="text-left py-2 pr-4">Location</th>
                <th className="text-left py-2 pr-4">Era</th>
                <th className="text-left py-2 pr-4">Density</th>
                <th className="text-left py-2 pr-4">Population</th>
                <th className="text-left py-2">Confidence</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {fullCase.populationDensity.map((item, i) => {
                const isZero = item.densityScore === "0";
                return (
                  <tr key={item.id} className={`group transition-colors ${isZero ? 'bg-rose-950/10' : ''}`}>
                    <td className="py-3 pr-4 text-slate-500 font-mono">{i + 1}</td>
                    <td className="py-3 pr-4">
                      <div className="flex items-center gap-2">
                        {isZero && <Ban size={14} className="text-rose-400 shrink-0" />}
                        <span className={`font-medium ${isZero ? 'text-rose-300' : 'text-slate-200'}`}>
                          {item.capability}
                        </span>
                      </div>
                    </td>
                    <td className="py-3 pr-4 text-slate-400">{item.locationRequired}</td>
                    <td className="py-3 pr-4 text-slate-400">{item.eraRequired}</td>
                    <td className="py-3 pr-4">
                      <span className={`font-mono font-bold ${isZero ? 'text-rose-400' : 'text-amber-400'}`}>
                        {item.densityScore}
                      </span>
                    </td>
                    <td className="py-3 pr-4 text-slate-400">{item.populationEstimate}</td>
                    <td className="py-3">
                      <span className={`px-2 py-0.5 text-xs rounded-full border ${confidenceColors[item.confidence]}`}>
                        {item.confidence}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Justification Panel */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Info className="w-5 h-5 text-sky-400" />
          <h2 className="text-lg font-semibold text-white">Justification for Each Capability</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {fullCase.populationDensity.filter(item => item.densityScore === "0").map((item) => (
            <div key={item.id} className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Ban size={14} className="text-rose-400" />
                <span className="text-sm font-medium text-rose-300">{item.capability}</span>
              </div>
              <p className="text-xs text-slate-400">{item.justification}</p>
              <div className="mt-2 flex items-center gap-2">
                <span className="text-[10px] text-slate-600">Location: {item.locationRequired}</span>
                <span className="text-slate-700">|</span>
                <span className="text-[10px] text-slate-600">Era: {item.eraRequired}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Key Insight */}
      <div className="bg-violet-500/5 border border-violet-500/20 rounded-xl p-5">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-violet-400 shrink-0 mt-0.5" />
          <div>
            <div className="text-sm font-semibold text-violet-300">Key Insight</div>
            <p className="text-sm text-slate-400 mt-1">
              This test is <strong className="text-slate-300">hard to game</strong> because it's structural, not interpretive.
              You're not arguing about testimony or expert opinion. You're asking: do the people exist? Can they coordinate?
              Do they have the tools? That's verifiable. Nobody can rhetoric their way past a population density of zero.
            </p>
          </div>
        </div>
      </div>

      {/* Direction B examples */}
      <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <ChevronRight className="w-5 h-5 text-emerald-400" />
          <h2 className="text-lg font-semibold text-white">Bidirectional Application</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-rose-500/5 border border-rose-500/20 rounded-lg p-4">
            <div className="text-xs text-rose-400 font-semibold uppercase tracking-wider mb-2">Shroud (Direction A)</div>
            <div className="text-sm text-slate-300 mb-2">"This is FAKE" - does the forger population exist?</div>
            <div className="text-2xl font-bold text-rose-400">ZERO</div>
            <div className="text-xs text-slate-500 mt-1">Forgery population does not exist</div>
          </div>
          <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-lg p-4">
            <div className="text-xs text-emerald-400 font-semibold uppercase tracking-wider mb-2">MKULTRA (Direction B)</div>
            <div className="text-sm text-slate-300 mb-2">"This conspiracy IS REAL" - do the conspirators exist?</div>
            <div className="text-2xl font-bold text-emerald-400">HIGH</div>
            <div className="text-xs text-slate-500 mt-1">CIA + researchers + infrastructure confirmed</div>
          </div>
          <div className="bg-blue-500/5 border border-blue-500/20 rounded-lg p-4">
            <div className="text-xs text-blue-400 font-semibold uppercase tracking-wider mb-2">Flat Earth (Direction B)</div>
            <div className="text-sm text-slate-300 mb-2">Conspiracy population cannot maintain silence</div>
            <div className="text-2xl font-bold text-blue-400">ZERO</div>
            <div className="text-xs text-slate-500 mt-1">~300K pilots + 600 astronauts all silent = impossible</div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
