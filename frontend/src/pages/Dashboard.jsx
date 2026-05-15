import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from "recharts"

export default function Dashboard() {

  const [reports, setReports] = useState([])

  const navigate = useNavigate()

  useEffect(() => {

    fetchReports()

  }, [])

  const fetchReports = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/reports"
      )

      setReports(response.data)

    } catch (error) {

      console.error(error)
    }
  }

  // Statistics
  const phishingCount = reports.filter(
    r => r.verdict === "Phishing"
  ).length

  const suspiciousCount = reports.filter(
    r => r.verdict === "Suspicious"
  ).length

  const safeCount = reports.filter(
    r => r.verdict === "Safe"
  ).length

  // Pie chart data
  const pieData = [
    { name: "Phishing", value: phishingCount },
    { name: "Suspicious", value: suspiciousCount },
    { name: "Safe", value: safeCount }
  ]

  // Risk distribution
  const riskData = reports.map(report => ({
    id: report.id,
    risk: report.risk_score
  }))

  const COLORS = [
    "#ef4444",
    "#facc15",
    "#22c55e"
  ]

  const getBadgeColor = (verdict) => {

    if (verdict === "Phishing")
      return "bg-red-500"

    if (verdict === "Suspicious")
      return "bg-yellow-500"

    return "bg-green-500"
  }

  return (

    <div className="p-8 space-y-8">

      {/* HEADER */}
      <div className="flex justify-between items-center">

        <h1 className="text-4xl font-bold">
          PhishGuard SOC Dashboard
        </h1>

        <button
          onClick={() => navigate("/upload")}
          className="bg-blue-600 px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Upload Email
        </button>

      </div>

      {/* STATS */}
      <div className="grid grid-cols-4 gap-6">

        <div className="bg-slate-800 p-6 rounded-xl">
          <h2 className="text-gray-400">
            Total Reports
          </h2>

          <p className="text-4xl font-bold mt-2">
            {reports.length}
          </p>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl">
          <h2 className="text-gray-400">
            Phishing
          </h2>

          <p className="text-4xl font-bold text-red-500 mt-2">
            {phishingCount}
          </p>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl">
          <h2 className="text-gray-400">
            Suspicious
          </h2>

          <p className="text-4xl font-bold text-yellow-400 mt-2">
            {suspiciousCount}
          </p>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl">
          <h2 className="text-gray-400">
            Safe
          </h2>

          <p className="text-4xl font-bold text-green-500 mt-2">
            {safeCount}
          </p>
        </div>

      </div>

      {/* CHARTS */}
      <div className="grid grid-cols-2 gap-6">

        {/* PIE CHART */}
        <div className="bg-slate-800 p-6 rounded-xl">

          <h2 className="text-2xl font-bold mb-4">
            Threat Distribution
          </h2>

          <ResponsiveContainer width="100%" height={300}>

            <PieChart>

              <Pie
                data={pieData}
                dataKey="value"
                outerRadius={100}
                label
              >

                {pieData.map((entry, index) => (

                  <Cell
                    key={index}
                    fill={COLORS[index % COLORS.length]}
                  />

                ))}

              </Pie>

              <Tooltip />

            </PieChart>

          </ResponsiveContainer>

        </div>

        {/* BAR CHART */}
        <div className="bg-slate-800 p-6 rounded-xl">

          <h2 className="text-2xl font-bold mb-4">
            Risk Scores
          </h2>

          <ResponsiveContainer width="100%" height={300}>

            <BarChart data={riskData}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="id" />

              <YAxis />

              <Tooltip />

              <Bar dataKey="risk" fill="#3b82f6" />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

      {/* REPORT TABLE */}
      <div className="bg-slate-800 rounded-xl overflow-hidden">

        <table className="w-full">

          <thead className="bg-slate-700">

            <tr>

              <th className="text-left p-4">ID</th>
              <th className="text-left p-4">Sender</th>
              <th className="text-left p-4">Subject</th>
              <th className="text-left p-4">Risk</th>
              <th className="text-left p-4">Verdict</th>

            </tr>

          </thead>

          <tbody>

            {reports.map((report) => (

              <tr
                key={report.id}
                className="border-t border-slate-700 cursor-pointer hover:bg-slate-700"
                onClick={() =>
                  navigate(`/reports/${report.id}`)
                }
              >

                <td className="p-4">
                  {report.id}
                </td>

                <td className="p-4">
                  {report.sender}
                </td>

                <td className="p-4">
                  {report.subject}
                </td>

                <td className="p-4">
                  {report.risk_score}
                </td>

                <td className="p-4">

                  <span className={`
                    px-3 py-1 rounded-full text-sm
                    ${getBadgeColor(report.verdict)}
                  `}>

                    {report.verdict}

                  </span>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  )
}