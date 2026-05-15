import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import axios from "axios"

export default function ReportDetails() {

  const { id } = useParams()

  const [data, setData] = useState(null)

  const [activeTab, setActiveTab] = useState("overview")

  useEffect(() => {

    fetchReport()

  }, [])

  const fetchReport = async () => {

    try {

      const res = await axios.get(
        `http://127.0.0.1:8000/reports/${id}`
      )

      setData(res.data)

    } catch (err) {

      console.error(err)
    }
  }

  if (!data) {

    return (
      <div className="p-10 text-white">
        Loading investigation...
      </div>
    )
  }

  const { risk_assessment, indicators } = data

  const getVerdictColor = (v) => {

    if (v === "Phishing") return "text-red-500"

    if (v === "Suspicious") return "text-yellow-400"

    return "text-green-400"
  }

  const getRiskColor = (score) => {

    if (score >= 80) return "border-red-500"

    if (score >= 50) return "border-yellow-400"

    return "border-green-400"
  }

  return (

    <div className="p-8 text-white space-y-6">

      {/* HEADER */}
      <div className="bg-slate-800 rounded-2xl p-6">

        <div className="flex justify-between items-center">

          <div>

            <h1 className="text-4xl font-bold">
              Investigation #{id}
            </h1>

            <p className="text-gray-400 mt-2">
              {data.parsed_email?.sender}
            </p>

          </div>

          <div className={`text-2xl font-bold ${getVerdictColor(risk_assessment.verdict)}`}>
            {risk_assessment.verdict}
          </div>

        </div>

      </div>

      {/* SCORE */}
      <div className="flex justify-center">

        <div className={`
          w-48 h-48 rounded-full border-8
          flex flex-col items-center justify-center
          bg-slate-800
          ${getRiskColor(risk_assessment.score)}
        `}>

          <p className="text-5xl font-bold">
            {risk_assessment.score}
          </p>

          <p className="text-gray-400">
            Risk Score
          </p>

        </div>

      </div>

      {/* EXPLANATION */}
      <div className="bg-slate-800 rounded-2xl p-6">

        <h2 className="text-2xl font-bold mb-4">
          Investigation Summary
        </h2>

        <p className="text-red-400 text-lg font-semibold">
          {data.explanation?.summary}
        </p>

        <div className="mt-4 space-y-2">

          {data.explanation?.reasons?.map((r, i) => (

            <div
              key={i}
              className="bg-slate-700 p-3 rounded-lg"
            >
              • {r}
            </div>

          ))}

        </div>

      </div>

      {/* TABS */}
      <div className="flex gap-4">

        {["overview", "urls", "raw"].map(tab => (

          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`
              px-4 py-2 rounded-lg capitalize
              ${activeTab === tab
                ? "bg-blue-600"
                : "bg-slate-700"}
            `}
          >
            {tab}
          </button>

        ))}

      </div>

      {/* OVERVIEW */}
      {activeTab === "overview" && (

        <div className="grid grid-cols-2 gap-6">

          {/* AUTH */}
          <div className="bg-slate-800 p-6 rounded-2xl">

            <h2 className="text-xl font-bold mb-4">
              Authentication
            </h2>

            <div className="space-y-3">

              <div className="bg-slate-700 p-3 rounded-lg">
                SPF: {String(indicators.headers?.spf)}
              </div>

              <div className="bg-slate-700 p-3 rounded-lg">
                DKIM: {String(indicators.headers?.dkim)}
              </div>

              <div className="bg-slate-700 p-3 rounded-lg">
                DMARC: {String(indicators.headers?.dmarc)}
              </div>

            </div>

          </div>

          {/* DOMAIN */}
          <div className="bg-slate-800 p-6 rounded-2xl">

            <h2 className="text-xl font-bold mb-4">
              Domain Intelligence
            </h2>

            <div className="space-y-3">

              <div className="bg-slate-700 p-3 rounded-lg">
                Domain: {indicators.domain?.domain}
              </div>

              <div className="bg-slate-700 p-3 rounded-lg">
                Age: {indicators.domain?.age_days || "N/A"} days
              </div>

              <div className="bg-slate-700 p-3 rounded-lg">
                MX Records:
                {" "}
                {String(indicators.domain?.has_mx_records)}
              </div>

            </div>

          </div>

          {/* NLP */}
          <div className="bg-slate-800 p-6 rounded-2xl">

            <h2 className="text-xl font-bold mb-4">
              Social Engineering Detection
            </h2>

            <div className="space-y-2">

              {indicators.nlp?.reasons?.map((r, i) => (

                <div
                  key={i}
                  className="bg-yellow-900/30 border border-yellow-500 p-3 rounded-lg"
                >
                  {r}
                </div>

              ))}

            </div>

          </div>

          {/* HTML */}
          <div className="bg-slate-800 p-6 rounded-2xl">

            <h2 className="text-xl font-bold mb-4">
              HTML Analysis
            </h2>

            <div className="space-y-3">

              <div className="bg-slate-700 p-3 rounded-lg">
                Forms:
                {" "}
                {String(indicators.html?.has_forms)}
              </div>

              <div className="bg-slate-700 p-3 rounded-lg">
                JavaScript:
                {" "}
                {String(indicators.html?.has_javascript)}
              </div>

              <div className="bg-slate-700 p-3 rounded-lg">
                Hidden Elements:
                {" "}
                {indicators.html?.hidden_elements?.length || 0}
              </div>

            </div>

          </div>

        </div>
      )}

      {/* URL TAB */}
      {activeTab === "urls" && (

        <div className="bg-slate-800 rounded-2xl p-6">

          <h2 className="text-2xl font-bold mb-4">
            URL Intelligence
          </h2>

          <div className="space-y-4">

            {indicators.urls?.map((u, i) => (

              <div
                key={i}
                className="bg-slate-700 p-4 rounded-xl"
              >

                <a
                  href={u.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue-400 break-all underline"
                >
                  {u.url}
                </a>

                <div className="mt-3 flex gap-4">

                  <span className={`
                    px-3 py-1 rounded-full text-sm
                    ${u.suspicious
                      ? "bg-red-500"
                      : "bg-green-600"}
                  `}>

                    {u.suspicious
                      ? "Suspicious"
                      : "Safe"}

                  </span>

                </div>

              </div>

            ))}

          </div>

        </div>
      )}

      {/* RAW EMAIL */}
      {activeTab === "raw" && (

        <div className="bg-black rounded-2xl p-6 border border-slate-700">

          <h2 className="text-2xl font-bold mb-4">
            Raw Email Source
          </h2>

          <pre className="
            text-sm
            text-green-400
            overflow-auto
            whitespace-pre-wrap
            break-words
            max-h-[700px]
          ">
            {data.parsed_email?.body || "No raw email available"}
          </pre>

        </div>
      )}

    </div>
  )
}