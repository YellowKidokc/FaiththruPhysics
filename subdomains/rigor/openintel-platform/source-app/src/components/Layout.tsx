import { Link, useLocation } from "react-router";
import { trpc } from "@/providers/trpc";
import {
  Home,
  Database,
  Grid3X3,
  Users,
  Clock,
  Signal,
  ListChecks,
  Gavel,
  FileCode,
  FlaskConical,
  Menu,
  X,
  Shield,
  ChevronRight,
} from "lucide-react";
import { useState } from "react";

const navItems = [
  { path: "/", label: "Dashboard", icon: Home },
  { path: "/evidence", label: "Evidence Catalog", icon: Database },
  { path: "/fakery", label: "Fakery Matrix", icon: Grid3X3 },
  { path: "/population", label: "Population Density", icon: Users },
  { path: "/timeline", label: "Timeline", icon: Clock },
  { path: "/signals", label: "Soft Signals", icon: Signal },
  { path: "/protocol", label: "Protocol", icon: ListChecks },
  { path: "/verdict", label: "Verdict", icon: Gavel },
  { path: "/export", label: "SQL Export", icon: FileCode },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { data: fullCase } = trpc.openintel.getFullCase.useQuery({ caseId: 1 });
  const { data: ocsData } = trpc.scoring.computeOCS.useQuery({ caseId: 1 });

  const currentPath = location.pathname;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex">
      {/* Sidebar */}
      <aside
        className={`fixed left-0 top-0 h-screen bg-slate-900 border-r border-slate-800 transition-all duration-300 z-50 flex flex-col ${
          sidebarOpen ? "w-64" : "w-16"
        }`}
      >
        {/* Header */}
        <div className="h-16 flex items-center px-4 border-b border-slate-800">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-lg hover:bg-slate-800 transition-colors"
          >
            {sidebarOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
          {sidebarOpen && (
            <div className="ml-3 flex items-center gap-2">
              <Shield className="w-5 h-5 text-amber-400" />
              <span className="font-bold text-sm tracking-wide text-amber-400">OpenIntel</span>
            </div>
          )}
        </div>

        {/* Case badge */}
        {sidebarOpen && fullCase && (
          <div className="px-4 py-3 border-b border-slate-800">
            <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Case</div>
            <div className="text-sm font-medium text-slate-200 mt-0.5 truncate">
              {fullCase.case.canonicalTitle}
            </div>
            <div className="text-xs text-slate-500 mt-0.5">{fullCase.case.caseId}</div>
            {ocsData && (
              <div className="mt-2 flex items-center gap-2">
                <div className="text-xs text-slate-400">OCS:</div>
                <div className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                  ocsData.ocsRaw >= 0.65 ? 'bg-emerald-900/50 text-emerald-400' :
                  ocsData.ocsRaw >= 0.45 ? 'bg-amber-900/50 text-amber-400' :
                  'bg-red-900/50 text-red-400'
                }`}>
                  {ocsData.ocs}%
                </div>
              </div>
            )}
          </div>
        )}
        {!sidebarOpen && fullCase && (
          <div className="py-3 border-b border-slate-800 flex justify-center">
            <FlaskConical className="w-5 h-5 text-amber-400" />
          </div>
        )}

        {/* Navigation */}
        <nav className="flex-1 py-3 space-y-0.5 overflow-y-auto">
          {navItems.map((item) => {
            const isActive = currentPath === item.path;
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2 mx-2 rounded-lg text-sm transition-all ${
                  isActive
                    ? "bg-amber-500/10 text-amber-400 font-medium border border-amber-500/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                }`}
                title={!sidebarOpen ? item.label : undefined}
              >
                <Icon size={18} className={isActive ? "text-amber-400" : ""} />
                {sidebarOpen && <span>{item.label}</span>}
                {isActive && sidebarOpen && <ChevronRight size={14} className="ml-auto text-amber-400/50" />}
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        {sidebarOpen && (
          <div className="px-4 py-3 border-t border-slate-800 text-xs text-slate-600">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500" />
              System Active
            </div>
            <div className="mt-1">Truth-Finding Protocol v1.0</div>
          </div>
        )}
      </aside>

      {/* Main Content */}
      <main
        className={`flex-1 transition-all duration-300 ${
          sidebarOpen ? "ml-64" : "ml-16"
        }`}
      >
        <div className="p-6 max-w-7xl mx-auto">{children}</div>
      </main>
    </div>
  );
}
