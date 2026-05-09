import { useState } from "react"
import axios from "axios"

export default function UploadPage() {

  const [file, setFile] = useState(null)

  const [result, setResult] = useState(null)

  const handleUpload = async () => {

    if (!file) {
      alert("Please select an .eml file first")
      return
    }

    const formData = new FormData()

    formData.append("file", file)

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze-email",
        formData
      )

      console.log(response.data)

      setResult(response.data)

      alert("Email analyzed successfully!")
      window.location.href = "/"

    } catch (error) {

      console.error(error)
    }
  }

  return (

    <div className="p-8">

      <h1 className="text-4xl font-bold mb-8">
        Upload Email for Analysis
      </h1>

      {/* DROP ZONE */}
      <div className="bg-slate-800 p-10 rounded-xl border-2 border-dashed border-slate-600 text-center">

        <p className="mb-4 text-gray-300">
          Drag & drop your .eml file here or select it manually
        </p>

        <input
          type="file"
          accept=".eml"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-6"
        />

        {file && (
          <p className="text-green-400 mb-4">
            Selected: {file.name}
          </p>
        )}

        <button
          onClick={handleUpload}
          className="bg-blue-600 px-6 py-2 rounded-lg hover:bg-blue-700"
        >
          Analyze Email
        </button>

      </div>

      {/* RESULT */}
      {result && (

        <div className="mt-8 bg-slate-800 p-6 rounded-xl">

          <h2 className="text-2xl font-bold mb-4">
            Analysis Result
          </h2>

          <p>
            <strong>Verdict:</strong>{" "}
            {result.risk_assessment.verdict}
          </p>

          <p>
            <strong>Risk Score:</strong>{" "}
            {result.risk_assessment.score}
          </p>

        </div>
      )}

    </div>
  )
}