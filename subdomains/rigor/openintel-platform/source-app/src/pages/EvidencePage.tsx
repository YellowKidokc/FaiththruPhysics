import { trpc } from "@/providers/trpc";
import Layout from "@/components/Layout";
import { useState } from "react";
import {
  Database,
  ChevronDown,
  ChevronUp,
  Microscope,
  Droplets,
  Stethoscope,
  Leaf,
  Camera,
  ScrollText,
  CalendarClock,
  Palette,
  Search,
  CheckCircle,
  XCircle,
  HelpCircle,
} from "lucide-react";

const tierColors: Record<string, string> = {
  T1: "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
  T2: "bg-blue-500/15 text-blue-400 border-blue-500/30",
  T3: "bg-amber-500/15 text-amber-400 border-amber-500/30",
  T4: "bg-orange-500/15 text-orange-400 border-orange-500/30",
  T5: "bg-red-500/15 text-red-400 border-red-500/30",
};

const tierLabels: Record<string, string> = {
  T1: "Constrained Physical",
  T2: "Costly",
  T3: "Cross-Checkable",
  T4: "Unconstrained",
  T5: "No Evidence",
};

const fabricationColors: Record<string, string> = {
  IMPOSSIBLE: "text-rose-400",
  EXTREME: "text-orange-400",
  HIGH: "text-amber-400",
  MODERATE: "text-yellow-400",
  LOW: "text-emerald-400",
  ZERO: "text-emerald-400",
};

const domainIcons: Record<string, React.ElementType> = {
  MATERIAL_SCIENCE: Microscope,
  HEMATOLOGY: Droplets,
  PATHOLOGY: Stethoscope,
  BOTANICAL_GEOLOGICAL: Leaf,
  IMAGING_PHYSICS: Camera,
  HISTORICAL_PROVENANCE: ScrollText,
  DATING: CalendarClock,
  ART_HISTORICAL: Palette,
};

const domainLabels: Record<string, string> = {
  MATERIAL_SCIENCE: "Material Science",
  HEMATOLOGY: "Hematology",
  PATHOLOGY: "Pathology",
  BOTANICAL_GEOLOGICAL: "Botanical / Geological",
  IMAGING_PHYSICS: "Imaging / Physics",
  HISTORICAL_PROVENANCE: "Historical Provenance",
  DATING: "Dating Methods",
  ART_HISTORICAL: "Art Historical",
};

export default function EvidencePage() {
  const { data: fullCase, isLoading } = trpc.openintel.getFullCase.useQuery({ caseId: 1 });
  const { data: evidenceStats } = trpc.scoring.computeEvidenceStats.useQuery({ caseId: 1 });
  const [selectedDomain, setSelectedDomain] = useState<string | null>(null);
  const [selectedTier, setSelectedTier] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  if (isLoading || !fullCase) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full" />
        </div>
      </Layout>
    );
  }

  const evidence = fullCase.evidence;
  const domains = [...new Set(evidence.map(e => e.domain))];

  // Domain stats
  const domainStats = domains.map(domain => {
    const items = evidence.filter(e => e.domain === domain);
    return {
      domain,
      count: items.length,
      t1Count: items.filter(i => i.tier === "T1").length,
      t2Count: items.filter(i => i.tier === "T2").length,
      t3Count: items.filter(i => i.tier === "T3").length,
    };
  });

  let filteredEvidence = evidence;
  if (selectedDomain) filteredEvidence = filteredEvidence.filter(e => e.domain === selectedDomain);
  if (selectedTier) filteredEvidence = filteredEvidence.filter(e => e.tier === selectedTier);
  if (searchQuery) {
    const q = searchQuery.toLowerCase();
    filteredEvidence = filteredEvidence.filter(
      e => e.evidenceName.toLowerCase().includes(q) ||
           (e.whatItProves?.toLowerCase() || "").includes(q) ||
           (e.source?.toLowerCase() || "").includes(q)
    );
  }

  return (
    <Layout>
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <Database className="w-7 h-7 text-emerald-400" />
          <h1 className="text-2xl font-bold text-white">Evidence Catalog</h1>
          <span className="px-2 py-0.5 text-xs bg-slate-800 text-slate-300 rounded-full font-mono">
            {evidence.length} items
          </span>
        </div>
        <p className="text-slate-400 text-sm">All evidence organized by domain and classified by fabrication cost tier (T1-T5).</p>
      </div>

      {/* Stats bar */}
      {evidenceStats && (
        <div className="grid grid-cols-2 md:grid-cols-6 gap-3 mb-6">
          {(["T1", "T2", "T3", "T4", "T5"] as const).map(tier => {
            const count = tier === "T1" ? evidenceStats.t1Count :
                         tier === "T2" ? evidenceStats.t2Count :
                         tier === "T3" ? evidenceStats.t3Count :
                         tier === "T4" ? evidenceStats.t4Count :
                         evidenceStats.t5Count;
            return (
              <button
                key={tier}
                onClick={() => setSelectedTier(selectedTier === tier ? null : tier)}
                className={`p-3 rounded-lg border text-left transition-all ${
                  selectedTier === tier
                    ? "border-amber-500/50 bg-amber-500/10"
                    : "border-slate-800 bg-slate-900 hover:border-slate-700"
                }`}
              >
                <span className={`inline-block px-1.5 py-0.5 text-xs rounded border font-mono ${tierColors[tier]}`}>
                  {tier}
                </span>
                <div className="text-lg font-bold text-white mt-1">{count}</div>
                <div className="text-xs text-slate-500">{tierLabels[tier]}</div>
              </button>
            );
          })}
          <div className="p-3 rounded-lg border border-slate-800 bg-slate-900">
            <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">Quality Score</div>
            <div className="text-lg font-bold text-emerald-400">{(evidenceStats.evidenceQuality * 100).toFixed(0)}%</div>
            <div className="text-xs text-slate-500">Weighted average</div>
          </div>
        </div>
      )}

      {/* Search */}
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
        <input
          type="text"
          placeholder="Search evidence by name, source, or what it proves..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-4 py-2.5 text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-amber-500/50"
        />
      </div>

      {/* Domain filters */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => setSelectedDomain(null)}
          className={`px-3 py-1.5 text-xs rounded-lg border transition-all ${
            !selectedDomain ? "border-amber-500/50 bg-amber-500/10 text-amber-400" : "border-slate-800 bg-slate-900 text-slate-400 hover:border-slate-700"
          }`}
        >
          All Domains
        </button>
        {domainStats.map(ds => {
          const Icon = domainIcons[ds.domain] || HelpCircle;
          return (
            <button
              key={ds.domain}
              onClick={() => setSelectedDomain(selectedDomain === ds.domain ? null : ds.domain)}
              className={`flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-lg border transition-all ${
                selectedDomain === ds.domain
                  ? "border-amber-500/50 bg-amber-500/10 text-amber-400"
                  : "border-slate-800 bg-slate-900 text-slate-400 hover:border-slate-700"
              }`}
            >
              <Icon size={12} />
              {domainLabels[ds.domain] || ds.domain}
              <span className="ml-1 text-slate-600">{ds.count}</span>
            </button>
          );
        })}
      </div>

      {/* Evidence list */}
      <div className="space-y-3">
        {filteredEvidence.length === 0 && (
          <div className="text-center py-12 text-slate-500">No evidence items match the current filters.</div>
        )}
        {filteredEvidence.map((item) => {
          const isExpanded = expandedId === item.id;
          return (
            <div
              key={item.id}
              className={`bg-slate-900 border rounded-xl overflow-hidden transition-all ${
                isExpanded ? "border-amber-500/30" : "border-slate-800 hover:border-slate-700"
              }`}
            >
              {/* Collapsed row */}
              <button
                onClick={() => setExpandedId(isExpanded ? null : item.id)}
                className="w-full px-4 py-3 flex items-center gap-3 text-left"
              >
                <span className={`px-1.5 py-0.5 text-xs rounded border font-mono shrink-0 ${tierColors[item.tier]}`}>
                  {item.tier}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-slate-200 truncate">{item.evidenceName}</div>
                  <div className="text-xs text-slate-500">{item.source}</div>
                </div>
                {item.fabricationCost && (
                  <span className={`text-xs font-medium shrink-0 ${fabricationColors[item.fabricationCost]}`}>
                    {item.fabricationCost}
                  </span>
                )}
                {item.isDiscriminating === "true" && (
                  <span className="px-1.5 py-0.5 text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded shrink-0">
                    Discriminating
                  </span>
                )}
                {isExpanded ? <ChevronUp size={16} className="text-slate-500" /> : <ChevronDown size={16} className="text-slate-500" />}
              </button>

              {/* Expanded content */}
              {isExpanded && (
                <div className="px-4 pb-4 border-t border-slate-800 pt-3 space-y-3">
                  {item.whatItProves && (
                    <div>
                      <div className="text-xs text-emerald-500 font-semibold uppercase tracking-wider mb-1">What It Proves</div>
                      <p className="text-sm text-slate-300">{item.whatItProves}</p>
                    </div>
                  )}
                  {item.fabricationCostDescription && (
                    <div>
                      <div className="text-xs text-rose-500 font-semibold uppercase tracking-wider mb-1">Fabrication Cost</div>
                      <p className="text-sm text-slate-300">{item.fabricationCostDescription}</p>
                    </div>
                  )}
                  {item.counterArguments && (
                    <div>
                      <div className="text-xs text-amber-500 font-semibold uppercase tracking-wider mb-1">Counter-Arguments</div>
                      <p className="text-sm text-slate-400">{item.counterArguments}</p>
                    </div>
                  )}
                  {item.weaknesses && (
                    <div>
                      <div className="text-xs text-orange-500 font-semibold uppercase tracking-wider mb-1">Weaknesses</div>
                      <p className="text-sm text-slate-400">{item.weaknesses}</p>
                    </div>
                  )}
                  {item.sourceChainOfCustody && (
                    <div>
                      <div className="text-xs text-sky-500 font-semibold uppercase tracking-wider mb-1">Chain of Custody</div>
                      <p className="text-sm text-slate-400">{item.sourceChainOfCustody}</p>
                    </div>
                  )}
                  {item.notes && (
                    <div className="pt-2 border-t border-slate-800">
                      <p className="text-xs text-slate-500 italic">{item.notes}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Summary footer */}
      <div className="mt-6 flex items-center justify-between text-xs text-slate-500">
        <div>Showing {filteredEvidence.length} of {evidence.length} evidence items</div>
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1"><CheckCircle size={12} className="text-emerald-400" /> {evidence.filter(e => e.isDiscriminating === "true").length} discriminating</span>
          <span className="flex items-center gap-1"><XCircle size={12} className="text-slate-500" /> {evidence.filter(e => e.isDiscriminating !== "true").length} non-discriminating</span>
        </div>
      </div>
    </Layout>
  );
}
