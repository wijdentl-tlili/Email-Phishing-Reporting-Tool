import { useEffect, useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"

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

  const getBadgeColor = (verdict) => {

    if (verdict === "Phishing")
      return "bg-red-500"

    if (verdict === "Suspicious")
      return "bg-yellow-500"

    return "bg-green-500"
  }

  return (

    <div className="p-8">

      <div className="flex justify-between items-center mb-8">

        <h1 className="text-4xl font-bold">
          PhishGuard Dashboard
        </h1>

        <a
          href="/upload"
          className="bg-blue-600 px-4 py-2 rounded-lg"
        >
          Upload Email
        </a>

      </div>

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
                onClick={() => navigate(`/reports/${report.id}`)}
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