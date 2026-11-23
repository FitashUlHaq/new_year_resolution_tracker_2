import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import CategoriesProfile from "./pages/CategoriesProfile";
import ResolutionDetail from "./pages/ResolutionDetail";
import Resolutions from "./pages/Resolutions";
import Dashboard from "./pages/Dashboard";
import Habits from "./pages/Habits";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/categories-profile" element={<CategoriesProfile />} />
            <Route path="/resolution-detail" element={<ResolutionDetail />} />
            <Route path="/resolutions" element={<Resolutions />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/habits" element={<Habits />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
