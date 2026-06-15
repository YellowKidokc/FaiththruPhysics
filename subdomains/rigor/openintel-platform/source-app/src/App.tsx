import { Routes, Route } from "react-router";
import Home from "./pages/Home";
import EvidencePage from "./pages/EvidencePage";
import FakeryMatrixPage from "./pages/FakeryMatrixPage";
import PopulationDensityPage from "./pages/PopulationDensityPage";
import TimelinePage from "./pages/TimelinePage";
import SoftSignalsPage from "./pages/SoftSignalsPage";
import ProtocolPage from "./pages/ProtocolPage";
import VerdictPage from "./pages/VerdictPage";
import ExportPage from "./pages/ExportPage";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/evidence" element={<EvidencePage />} />
      <Route path="/fakery" element={<FakeryMatrixPage />} />
      <Route path="/population" element={<PopulationDensityPage />} />
      <Route path="/timeline" element={<TimelinePage />} />
      <Route path="/signals" element={<SoftSignalsPage />} />
      <Route path="/protocol" element={<ProtocolPage />} />
      <Route path="/verdict" element={<VerdictPage />} />
      <Route path="/export" element={<ExportPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
