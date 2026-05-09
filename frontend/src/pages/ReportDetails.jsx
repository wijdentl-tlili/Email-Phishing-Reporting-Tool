import { useEffect, useState } from "react"
import axios from "axios"
import { useParams } from "react-router-dom"

export default function ReportDetails() {

  const { id } = useParams()

  const [report, setReport] = useState(null)

  const [indicators, setIndicators] = useState([])

  useEffect(() => {

    fetchReport()

  }, [])

  const fetchReport = async () => {

    try {

      const res = await axios.get(
        `http://127.0.0.1:8000/reports/${id}`
      )

      setReport(res.data.report)

      setIndicators(res.data.indicators)

    } catch (err) {

      console.log(err)
    }
  }

  if (!report) {

    return (
      <div className="p-8">
        Loading...
      </div>
    )
  }

  const getVerdictColor = (verdict) => {

    if (verdict === "Phishing")
      return "text-red-500"

    if (verdict === "Suspicious")
      return "text-yellow-400"

    return "text-green-400"
  }

  return (

    <div className="p-8 space-y-6">

      {/* HEADER */}
      <div className="bg-slate-800 p-6 rounded-xl">

        <h1 className="text-3xl font-bold">
          SOC Investigation Report #{report.id}
        </h1>

        <div className="flex gap-6 mt-4">

          <p>
            <strong>Sender:</strong> {report.sender}
          </p>

          <p>
            <strong>Subject:</strong> {report.subject}
          </p>

          <p className={`font-bold ${getVerdictColor(report.verdict)}`}>
            {report.verdict}
          </p>

          <p>
            Risk Score: {report.risk_score}/100
          </p>

        </div>

      </div>

      {/* MAIN GRID */}
      <div className="grid grid-cols-2 gap-6">

        {/* LEFT PANEL */}
        <div className="bg-slate-800 p-6 rounded-xl">

          <h2 className="text-xl font-bold mb-4">
            Email Information
          </h2>

          <p><strong>Sender:</strong> {report.sender}</p>

          <p><strong>Subject:</strong> {report.subject}</p>

        </div>

        {/* RIGHT PANEL */}
        <div className="bg-slate-800 p-6 rounded-xl">

          <h2 className="text-xl font-bold mb-4">
            Indicators of Compromise
          </h2>

          {indicators.map((ind) => (

            <div
              key={ind.id}
              className="bg-slate-700 p-3 rounded mb-2"
            >

              <p>
                <strong>Type:</strong> {ind.indicator_type}
              </p>

              <p>
                {ind.value}
              </p>

              <p className={ind.malicious ? "text-red-400" : "text-green-400"}>
                {ind.malicious ? "Malicious" : "Safe"}
              </p>

            </div>

          ))}

        </div>

      </div>

      {/* RAW DATA */}
      <div className="bg-slate-800 p-6 rounded-xl">

        <h2 className="text-xl font-bold mb-4">
          Raw Email Data
        </h2>

        <pre className="text-sm overflow-auto text-gray-300">

          {report.raw_email}

        </pre>

      </div>

    </div>
  )
}