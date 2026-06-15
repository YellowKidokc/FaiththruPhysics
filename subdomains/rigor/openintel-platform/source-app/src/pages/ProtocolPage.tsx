import { trpc } from "@/providers/trpc";
import Layout from "@/components/Layout";
import {
  ListChecks,
  CheckCircle,
  Clock,
  AlertCircle,
  Lock,
  ChevronRight,
  ShieldCheck,
} from "lucide-react";

const statusConfig: Record<string, { color: string; icon: React.ElementType; label: string }> = {
  COMPLETED: { color: "text-emerald-400", icon: CheckCircle, label: "Completed" },
  IN_PROGRESS: { color: "text-amber-400", icon: Clock, label: "In Progress" },
  PENDING: { color: "text-slate-500", icon: Clock, label: "Pending" },
  SKIPPED: { color: "text-slate-600", icon: AlertCircle, label: "Skipped" },
  BLOCKED: { color: "text-red-400", icon: Lock, label: "Blocked" },
};

export default function ProtocolPage() {
  const { data: fullCase, isLoading } = trpc.openintel.getFullCase.useQuery({ caseId: 1 });

  if (isLoading || !fullCase) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full" />
        </div>
      </Layout>
    );
  }

  const steps = fullCase.protocolSteps;
  const completed = steps.filter(s => s.status === "COMPLETED").length;

  return (
    <Layout>
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <ListChecks className="w-7 h-7 text-sky-400" />
          <h1 className="text-2xl font-bold text-white">Truth-Finding Protocol</h1>
          <span className="px-2 py-0.5 text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full font-mono">
            {completed}/{steps.length} Complete
          </span>
        </div>
        <p className="text-slate-400 text-sm max-w-3xl">
          The 10-step protocol derived from Theophysics 7Q Method + Shannon Base Layer.
          Original 7 steps + 3 repairs. Each step includes red-team results for gaming resistance.
        </p>
      </div>

      {/* Progress bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-slate-400">Protocol Progress</span>
          <span className="text-sm font-bold text-emerald-400">{Math.round((completed / steps.length) * 100)}%</span>
        </div>
        <div className="w-full bg-slate-800 rounded-full h-3 overflow-hidden">
          <div
            className="bg-emerald-500 h-full rounded-full transition-all duration-1000"
            style={{ width: `${(completed / steps.length) * 100}%` }}
          />
        </div>
      </div>

      {/* Steps */}
      <div className="space-y-4">
        {steps.map((step) => {
          const sConfig = statusConfig[step.status] || statusConfig.PENDING;
          const StatusIcon = sConfig.icon;
          const isCompleted = step.status === "COMPLETED";

          return (
            <div
              key={step.id}
              className={`bg-slate-900 border rounded-xl overflow-hidden transition-all ${
                isCompleted
                  ? "border-emerald-500/20"
                  : "border-slate-800"
              }`}
            >
              <div className="p-5">
                <div className="flex items-start gap-4">
                  {/* Step number */}
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                    isCompleted ? "bg-emerald-500/10" : "bg-slate-800"
                  }`}>
                    {isCompleted ? (
                      <CheckCircle size={20} className="text-emerald-400" />
                    ) : (
                      <span className="text-lg font-bold text-slate-500">{step.stepNumber}</span>
                    )}
                  </div>

                  <div className="flex-1">
                    {/* Header */}
                    <div className="flex items-center gap-3 mb-1">
                      <h3 className="text-base font-semibold text-white">{step.stepName}</h3>
                      <span className={`px-2 py-0.5 text-xs rounded-full border flex items-center gap-1 ${
                        isCompleted
                          ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-400"
                          : "bg-slate-800 border-slate-700 text-slate-500"
                      }`}>
                        <StatusIcon size={10} />
                        {sConfig.label}
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-sm text-slate-400 mb-3">{step.description}</p>

                    {/* Findings + Conclusion */}
                    {step.findings && (
                      <div className="bg-slate-800/50 rounded-lg p-3 mb-2">
                        <div className="text-xs text-sky-500 font-semibold uppercase tracking-wider mb-1">Findings</div>
                        <p className="text-sm text-slate-300">{step.findings}</p>
                      </div>
                    )}
                    {step.conclusion && (
                      <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${
                        step.conclusion.includes("PASS") || step.conclusion.includes("UPDATE")
                          ? "bg-emerald-500/10 text-emerald-400"
                          : step.conclusion.includes("fail") || step.conclusion.includes("FAIL")
                          ? "bg-rose-500/10 text-rose-400"
                          : "bg-slate-800 text-slate-400"
                      }`}>
                        <ChevronRight size={12} />
                        {step.conclusion}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Red Team Results */}
      <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <h2 className="text-lg font-semibold text-white">Red Team Results</h2>
        </div>
        <p className="text-sm text-slate-400 mb-4">
          The protocol was adversarially tested against 6 attack vectors. All survived.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            { attack: "Coordinated liar problem", defense: "Evidence Hierarchy + Independence Verification", survived: true },
            { attack: "Gaming Step 4 (Update Commitment)", defense: "Judge's Update Audit power", survived: true },
            { attack: "Evidence base control", defense: "Absence Audit + Hostile Corroboration requirement", survived: true },
            { attack: "Testimonial stacking", defense: "T1-T4 tier weighting", survived: true },
            { attack: "Too-clean-story paradox", defense: "Noise-Floor Check", survived: true },
            { attack: "Unfalsifiable anchor", defense: "Protocol correctly identifies as unresolvable + explains why", survived: true },
          ].map((test, i) => (
            <div key={i} className="bg-emerald-500/5 border border-emerald-500/10 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                <CheckCircle size={12} className="text-emerald-400" />
                <span className="text-xs text-emerald-400 font-semibold uppercase">Survived</span>
              </div>
              <div className="text-sm text-slate-300 font-medium">{test.attack}</div>
              <div className="text-xs text-slate-500 mt-1">Defense: {test.defense}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Limits */}
      <div className="mt-6 bg-amber-500/5 border border-amber-500/20 rounded-xl p-5">
        <div className="flex items-center gap-2 mb-2">
          <AlertCircle className="w-5 h-5 text-amber-400" />
          <span className="text-sm font-semibold text-amber-300">Protocol Limits</span>
        </div>
        <p className="text-sm text-slate-400">
          Truth cannot be found when all evidence is controlled by dishonest parties with no independent verification,
          when claims are inherently unfalsifiable, when both parties have zero willingness to receive truth (A=0),
          or when evidence has been destroyed and only unverifiable testimony remains.
          <strong className="text-slate-300"> But even in limits, the protocol correctly IDENTIFIES the condition rather than producing a false result.</strong>
        </p>
      </div>
    </Layout>
  );
}
