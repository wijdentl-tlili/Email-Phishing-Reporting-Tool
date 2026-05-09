import { Routes, Route } from "react-router-dom"

import Dashboard from "./pages/Dashboard"
import UploadPage from "./pages/UploadPage"
import ReportDetails from "./pages/ReportDetails"

export default function App() {

  return (
    <Routes>

      <Route
        path="/"
        element={<Dashboard />}
      />

      <Route
        path="/upload"
        element={<UploadPage />}
      />

      <Route
        path="/reports/:id"
        element={<ReportDetails />}
      />

    </Routes>
  )
}