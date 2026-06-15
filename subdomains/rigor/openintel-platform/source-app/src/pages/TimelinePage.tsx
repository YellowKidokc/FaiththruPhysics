import { trpc } from "@/providers/trpc";
import Layout from "@/components/Layout";
import {
  Clock,
  CheckCircle,
  HelpCircle,
  AlertTriangle,
  XCircle,
} from "lucide-react";

const verificationIcons: Record<string, { icon: React.ElementType; color: string; label: string }> = {
  CONFIRMED: { icon: CheckCircle, color: "text-emerald-400", label: "Confirmed" },
  PROBABLE: { icon: HelpCircle, color: "text-blue-400", label: "Probable" },
  DISPUTED: { icon: AlertTriangle, color: "text-amber-400", label: "Disputed" },
  UNVERIFIED: { icon: HelpCircle, color: "text-slate-400", label: "Unverified" },
  DEBUNKED: { icon: XCircle, color: "text-red-400", label: "Debunked" },
};

const tierColors: Record<string, string> = {
  T1: "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
  T2: "bg-blue-500/15 text-blue-400 border-blue-500/30",
  T3: "bg-amber-500/15 text-amber-400 border-amber-500/30",
  T4: "bg-orange-500/15 text-orange-400 border-orange-500/30",
  T5: "bg-red-500/15 text-red-400 border-red-500/30",
};

export default function TimelinePage() {
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

  const timeline = fullCase.timeline;

  return (
    <Layout>
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Clock className="w-7 h-7 text-cyan-400" />
          <h1 className="text-2xl font-bold text-white">Timeline</h1>
          <span className="px-2 py-0.5 text-xs bg-slate-800 text-slate-300 rounded-full font-mono">
            {timeline.length} events
          </span>
        </div>
        <p className="text-slate-400 text-sm">Chronological events from the crucifixion (~30 AD) to present day.</p>
      </div>

      {/* Timeline visualization */}
      <div className="relative">
        {/* Vertical line */}
        <div className="absolute left-6 top-0 bottom-0 w-px bg-gradient-to-b from-amber-500/50 via-slate-700 to-slate-800" />

        <div className="space-y-4">
          {timeline.map((event) => {
            const vConfig = verificationIcons[event.verificationStatus] || verificationIcons.UNVERIFIED;
            const VIcon = vConfig.icon;
            const isDisputed = event.verificationStatus === "DISPUTED";

            return (
              <div key={event.id} className={`relative flex gap-4 ${isDisputed ? 'opacity-70' : ''}`}>
                {/* Dot on the line */}
                <div className="relative z-10 flex flex-col items-center">
                  <div className={`w-3 h-3 rounded-full border-2 ${
                    event.verificationStatus === "CONFIRMED" ? "bg-emerald-500 border-emerald-400" :
                    event.verificationStatus === "DISPUTED" ? "bg-amber-500 border-amber-400" :
                    "bg-slate-600 border-slate-500"
                  }`} />
                </div>

                {/* Content card */}
                <div className={`flex-1 bg-slate-900 border rounded-xl p-4 ${
                  isDisputed ? "border-amber-500/20" : "border-slate-800"
                }`}>
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-lg font-bold text-amber-400 font-mono">{event.eventDate}</span>
                        <span className={`px-1.5 py-0.5 text-xs rounded border ${tierColors[event.tier]}`}>
                          {event.tier}
                        </span>
                        {isDisputed && (
                          <span className="px-1.5 py-0.5 text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded">
                            DISPUTED
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-slate-200">{event.eventDescription}</p>
                      {event.source && (
                        <p className="text-xs text-slate-500 mt-1">Source: {event.source}</p>
                      )}
                      {event.entitiesInvolved && (
                        <p className="text-xs text-slate-600 mt-1">Entities: {event.entitiesInvolved}</p>
                      )}
                    </div>
                    <div className="flex items-center gap-1 shrink-0">
                      <VIcon size={14} className={vConfig.color} />
                      <span className={`text-xs ${vConfig.color}`}>{vConfig.label}</span>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Legend */}
      <div className="mt-8 flex flex-wrap gap-4 text-xs text-slate-500">
        {Object.entries(verificationIcons).map(([key, val]) => {
          const Icon = val.icon;
          return (
            <div key={key} className="flex items-center gap-1">
              <Icon size={12} className={val.color} />
              <span>{val.label}</span>
            </div>
          );
        })}
      </div>
    </Layout>
  );
}
