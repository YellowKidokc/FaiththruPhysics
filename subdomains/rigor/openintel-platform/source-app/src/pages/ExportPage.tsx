import { trpc } from "@/providers/trpc";
import Layout from "@/components/Layout";
import { useState } from "react";
import {
  FileCode,
  Copy,
  CheckCircle,
  Database,
  Download,
  Table2,
  FileSpreadsheet,
} from "lucide-react";

export default function ExportPage() {
  const { data: sqlData, isLoading } = trpc.scoring.generateSqlExport.useQuery({ caseId: 1 });
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (sqlData?.sql) {
      navigator.clipboard.writeText(sqlData.sql);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    if (sqlData?.sql) {
      const blob = new Blob([sqlData.sql], { type: "text/sql" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "openintel_shroud_export.sql";
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  return (
    <Layout>
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <FileCode className="w-7 h-7 text-emerald-400" />
          <h1 className="text-2xl font-bold text-white">SQL Export</h1>
        </div>
        <p className="text-slate-400 text-sm">
          Generate ready-to-run SQL INSERT statements for the complete Shroud of Turin case.
          Copy and paste into pgAdmin, psql, or any PostgreSQL client.
        </p>
      </div>

      {/* Export cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <Database className="w-5 h-5 text-sky-400 mb-2" />
          <div className="text-sm font-medium text-white">PostgreSQL Export</div>
          <div className="text-xs text-slate-500 mt-1">INSERT statements for all tables</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <Table2 className="w-5 h-5 text-emerald-400 mb-2" />
          <div className="text-sm font-medium text-white">Complete Case Data</div>
          <div className="text-xs text-slate-500 mt-1">57 evidence + 18 timeline + 10 fakery + 8 pop + 14 signals</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <FileSpreadsheet className="w-5 h-5 text-amber-400 mb-2" />
          <div className="text-sm font-medium text-white">Copy-Paste Ready</div>
          <div className="text-xs text-slate-500 mt-1">No manual data entry required</div>
        </div>
      </div>

      {/* SQL Output */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        {/* Toolbar */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <FileCode size={16} className="text-slate-500" />
            <span className="text-sm text-slate-400">openintel_shroud_export.sql</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-slate-800 text-slate-300 rounded-lg hover:bg-slate-700 transition-colors"
            >
              {copied ? <CheckCircle size={12} className="text-emerald-400" /> : <Copy size={12} />}
              {copied ? "Copied" : "Copy"}
            </button>
            <button
              onClick={handleDownload}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-amber-500/10 text-amber-400 border border-amber-500/30 rounded-lg hover:bg-amber-500/20 transition-colors"
            >
              <Download size={12} />
              Download
            </button>
          </div>
        </div>

        {/* SQL content */}
        <div className="p-4 overflow-x-auto">
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin w-6 h-6 border-2 border-amber-500 border-t-transparent rounded-full" />
            </div>
          ) : (
            <pre className="text-xs text-slate-400 leading-relaxed whitespace-pre-wrap font-mono">
              {sqlData?.sql || "-- No data generated"}
            </pre>
          )}
        </div>
      </div>

      {/* Schema reference */}
      <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <Database className="w-5 h-5 text-sky-400" />
          <h2 className="text-lg font-semibold text-white">Database Schema Reference</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          {[
            { table: "cases", desc: "Case management (case_id, title, type, verdict, OCS)" },
            { table: "evidence_items", desc: "57 items across 8 domains with T1-T5 tiers" },
            { table: "timeline_events", desc: "18 chronological events from ~30 AD to 2022" },
            { table: "fakery_matrix_items", desc: "F1-F10 constraints with fabrication costs" },
            { table: "population_density_items", desc: "8 capability density scores" },
            { table: "soft_signals", desc: "14 structural meta-evidence signals" },
            { table: "protocol_steps", desc: "10-step protocol with findings" },
            { table: "entities", desc: "People, organizations, institutions" },
            { table: "contradictions", desc: "Logged contradictions with severity" },
          ].map((item) => (
            <div key={item.table} className="flex items-center gap-2 text-slate-400">
              <span className="text-sky-400 font-mono">{item.table}</span>
              <span className="text-slate-600">|</span>
              <span>{item.desc}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Integration note */}
      <div className="mt-6 bg-emerald-500/5 border border-emerald-500/20 rounded-xl p-5">
        <div className="flex items-start gap-3">
          <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <div className="text-sm font-semibold text-emerald-300">Three-Output Architecture</div>
            <p className="text-sm text-slate-400 mt-1">
              The OpenIntel platform generates three outputs from a single case:
              <strong className="text-slate-300"> SQL INSERT statements</strong> for PostgreSQL,
              <strong className="text-slate-300"> Excel workbooks</strong> for visual analysis, and
              <strong className="text-slate-300"> JSON exports</strong> for API integration.
              The database is the canonical store; Excel is the visual record; the web app is the interface.
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
