import React, { useEffect, useState } from "react";

import "./App.css";

import Login from "./Login";

import Register from "./Register";



function App() {

  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  const [skillGapResult, setSkillGapResult] = useState(null);

  const [improvementAnalysis, setImprovementAnalysis] = useState(null);

  const [error, setError] = useState("");

  const [jobDescription, setJobDescription] = useState("");

  const [jobMatch, setJobMatch] = useState(null);

  const [jobLoading, setJobLoading] = useState(false);

  const [jobError, setJobError] = useState("");

  const [history, setHistory] = useState([]);

  const [showHistory, setShowHistory] = useState(false);

  
  

  const [selectedAnalysis, setSelectedAnalysis] = useState(null);

  
  const [analysisLoading, setAnalysisLoading] = useState(false);

  const [historyLoading, setHistoryLoading] = useState(false);



  const [user, setUser] = useState(() => {

    if (typeof window === "undefined") return null;

    const savedUser = localStorage.getItem("user");

    return savedUser ? JSON.parse(savedUser) : null;

  });



  const [token, setToken] = useState(() => {

    if (typeof window === "undefined") return "";

    return localStorage.getItem("token") || "";

  });



  const [authMode, setAuthMode] = useState("login");
  const [authError, setAuthError] = useState("");



  const handleRegister = async (name, email, password) => {
    try {
      setAuthError("");
      setError("");

    const response = await fetch("https://ai-resume-analyzer-ypnq.onrender.com/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.message || "Registration failed.");
      }

      localStorage.setItem("token", data.token);
      setToken(data.token);

      // If backend returns the new user, log in immediately.
      if (data.user) {
        localStorage.setItem("user", JSON.stringify(data.user));
        setUser(data.user);
      } else {
        // Fallback for the current backend: go to Login.
        setAuthMode("login");
      }

      return true;
    } catch (err) {
      console.error(err);
      setAuthError(err.message || "Registration failed.");
      return false;
    }
  };


  const handleLogin = async (email, password) => {
    try {
      setAuthError("");
      setError("");

      const response = await fetch("https://ai-resume-analyzer-ypnq.onrender.com/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.message || "Login failed.");
      }

      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));

      setAuthError("");
      setToken(data.token);
      setUser(data.user);
      return data;
    } catch (err) {
      console.error(err);
      setAuthError(err.message || "Login failed.");
      return false;
    }
  };


  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    setToken("");
    setUser(null);
    setAuthError("");
    setError("");
    setAuthMode("login");
  };

const loadHistory = async (openHistory = true) => {
  try {
    const response = await fetch(
  "https://ai-resume-analyzer-ypnq.onrender.com/history",
  {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`
    }
  }
);

    if (!response.ok) {
      throw new Error("Failed to load history.");
    }

    const data = await response.json();

    setHistory(data.history || []);

    if (openHistory) {
      setShowHistory(true);
    }
  } catch (error) {
    console.error(error);
    setError("Failed to load analysis history.");
  }
};

const viewPreviousAnalysis = async (analysisId) => {
  try {
    setAnalysisLoading(true);
    setError("");
    const token = localStorage.getItem("token");

    console.log("Token exists:", !!token);

    const response = await fetch(
      `https://ai-resume-analyzer-ypnq.onrender.com/history/${analysisId}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    console.log("Analysis ID:", analysisId);
    console.log("Token:", localStorage.getItem("token"));
    console.log("Response status:", response.status);

    if (!response.ok) {
      throw new Error("Failed to load previous analysis.");
    }

    const data = await response.json();

    setSelectedAnalysis(data.analysis);
  } catch (error) {
    console.error(error);
    setError("Failed to load previous analysis.");
  } finally {
    setAnalysisLoading(false);
  }
};




useEffect(() => {
  loadHistory(false);
}, []);



  
const viewAnalysis = async (analysisId) => {
  try {
    setHistoryLoading(true);
    setError("");

    const token = localStorage.getItem("token");

    if (!token) {
      throw new Error("Please log in again to view this analysis.");
    }

    const response = await fetch(
      `https://ai-resume-analyzer-ypnq.onrender.com/history/${analysisId}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || data.message || "Failed to load previous analysis."
      );
    }

    if (!data.analysis) {
      throw new Error("Analysis data was not found.");
    }

    setSelectedAnalysis(data.analysis);
  } catch (err) {
    console.error("View analysis error:", err);
    setError(err.message || "Failed to load previous analysis.");
  } finally {
    setHistoryLoading(false);
  }
};




  const checkJobMatch = async () => {

    if (!result?.text || !jobDescription.trim()) {

      setJobError("Please analyze your resume and enter a job description.");

      return;

    }



    try {

      const skillGapResponse = await fetch("https://ai-resume-analyzer-ypnq.onrender.com/skill-gap", {

        method: "POST",

        headers: {

          "Content-Type": "application/json",

        },

        body: JSON.stringify({

          resume_text: result.text,

          job_description: jobDescription,

        }),

      });



      if (!skillGapResponse.ok) {

        throw new Error("Skill gap analysis failed.");

      }



      const skillGapData = await skillGapResponse.json();



      if (skillGapData.success) {

        setSkillGapResult(skillGapData.skill_gap);

      }

    } catch (err) {

      setJobError(err.message);

    }

  };



  const downloadReport = async () => {

    if (!result) {

      setError("Please analyze your resume first.");

      return;

    }



    try {

      const response = await fetch("https://ai-resume-analyzer-ypnq.onrender.com/generate-report", {

        method: "POST",

        headers: {

          "Content-Type": "application/json",

        },

        body: JSON.stringify({

          resume: result.resume,

          ai_analysis: result.ai_analysis,

          skill_gap: skillGapResult,

          improvement_analysis: improvementAnalysis,

        }),

      });



      if (!response.ok) {

        throw new Error("Report generation failed");

      }



      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");



      link.href = url;

      link.download = "AI_Resume_Analysis_Report.pdf";



      document.body.appendChild(link);

      link.click();

      link.remove();



      window.URL.revokeObjectURL(url);

    } catch (err) {

      console.error(err);

      setError("Failed to generate report.");

    }

  };



  const uploadResume = async () => {

    if (!file) {

      setError("Please select a PDF resume.");

      return;

    }



    setLoading(true);

    setError("");

    setResult(null);



    const formData = new FormData();

    formData.append("file", file);



    try {
const response = await fetch(
  "https://ai-resume-analyzer-ypnq.onrender.com/upload-resume",
  {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`
    },
    body: formData
  }
);

      if (!response.ok) {

        throw new Error("Resume analysis failed.");

      }



      const data = await response.json();

      setResult(data);

      setImprovementAnalysis(data.improvement_analysis);

    } catch (err) {

      setError(err.message);

    } finally {

      setLoading(false);

    }

  };



  const matchJob = async () => {

    if (!result?.resume) {

      setJobError("Please analyze your resume first.");

      return;

    }



    if (!jobDescription.trim()) {

      setJobError("Please paste a job description.");

      return;

    }



    setJobLoading(true);

    setJobError("");

    setJobMatch(null);



    try {

      const response = await fetch("https://ai-resume-analyzer-ypnq.onrender.com/match-job", {

        method: "POST",

        headers: {

          "Content-Type": "application/json",

        },

        body: JSON.stringify({

          resume: result.resume,

          job_description: jobDescription,

        }),

      });



      if (!response.ok) {

        throw new Error("Job matching failed.");

      }



      const data = await response.json();

      setJobMatch(data.match);

    } catch (err) {

      setJobError(err.message);

    } finally {

      setJobLoading(false);

    }

  };



  if (!user) {
    if (authMode === "register") {
      return (
        <Register
          onRegister={async (name, email, password) => {
            await handleRegister(name, email, password);
          }}
          onLogin={() => {
            setAuthError("");
            setAuthMode("login");
          }}
          error={authError}
        />
      );
    }

    return (
      <Login
        onLogin={handleLogin}
        onRegister={() => {
          setAuthError("");
          setAuthMode("register");
        }}
        error={authError}
      />
    );
  }


  return (

    <div className="app">

      <header className="header">

        <h1>AI Resume Analyzer 🚀</h1>

        <p>Upload your resume and get AI-powered feedback instantly.</p>
        {user && (
  <div className="user-welcome">
    👋 Welcome back, <strong>{user.name || "User"}</strong>
    <span>{user.email}</span>
  </div>
)}



        <div className="header-actions">

          <button className="history-button" onClick={loadHistory}>

            📚 Analysis History

          </button>



          <button className="logout-button" onClick={handleLogout}>

            🚪 Logout

          </button>

        </div>

      </header>
      <div className="dashboard-stats">
  <div className="stat-card">
    <div className="stat-icon">📄</div>
    <div>
      <h3>{history.length}</h3>
      <p>Total Resumes</p>
    </div>
  </div>

  <div className="stat-card">
    <div className="stat-icon">⭐</div>
    <div>
      <h3>
        {history.length > 0
          ? Math.round(
              history.reduce(
                (sum, item) => sum + (item.overall_score || 0),
                0
              ) / history.length
            )
          : 0}
      </h3>
      <p>Average Score</p>
    </div>
  </div>

  <div className="stat-card">
    <div className="stat-icon">🎯</div>
    <div>
      <h3>{history.length}</h3>
      <p>Total Analyses</p>
    </div>
  </div>
</div>



      <main className="container">

        <section className="upload-card">

          <h2>Analyze Your Resume 📄</h2>

          <p>

            Upload your PDF resume and let AI find strengths, weaknesses and

            missing skills.

          </p>



          <input

            className="file-input"

            type="file"

            accept=".pdf"

            onChange={(e) => setFile(e.target.files[0])}

          />



          <br />



          <button

            className="analyze-btn"

            onClick={uploadResume}

            disabled={loading}

          >

            {loading ? "Analyzing with AI... 🧠" : "Analyze Resume 🚀"}

          </button>



          {error && <p className="error">❌ {error}</p>}



          {loading && (

            <div className="loading-card">

              <div className="loading-icon">🧠</div>

              <h3>AI is analyzing your resume...</h3>

              <p>Please wait while Llama AI analyzes your resume.</p>



              <div className="loading-steps">

                <div>📄 Reading resume</div>

                <div>🔍 Checking ATS compatibility</div>

                <div>🧠 Analyzing skills</div>

                <div>📊 Generating recommendations</div>

              </div>



              <div className="loading-dots">

                <span></span>

                <span></span>

                <span></span>

              </div>

            </div>

          )}

        </section>



        {showHistory && (

          <section className="history-section">

            <div className="history-header">

              <h2>📚 Analysis History</h2>

              <button className="close-history" onClick={() => setShowHistory(false)}>

                ✕

              </button>

            </div>



            {history.length === 0 ? (

              <p className="empty-history">No previous analyses found.</p>

            ) : (

              <div className="history-list">

                {history.map((item) => (

                  <div className="history-card" key={item.id}>

                    <div>

                      <h3>{item.filename}</h3>

                      <p>{item.name || "Unknown candidate"}</p>

                      <small>{item.created_at}</small>

                    </div>



                    <div className="history-scores">

                      <span>

                        Overall: <strong>{item.overall_score}/100</strong>

                      </span>

                      <span>

                        ATS: <strong>{item.ats_score}/100</strong>

                      </span>

                      <button

                        className="view-analysis-button"

                        onClick={() => viewAnalysis(item.id)}

                      >

                        👁 View Analysis

                      </button>

                    </div>

                  </div>

                ))}

              </div>

            )}

          </section>

        )}



        {selectedAnalysis && (

          <section className="previous-analysis-section">

            <div className="previous-analysis-header">

              <h2>📊 Previous Analysis</h2>

              <button

                className="close-history"

                onClick={() => setSelectedAnalysis(null)}

              >

                ✕

              </button>

            </div>



            <div className="previous-analysis-content">

              <h3>👤 Resume Details</h3>

              <p>

                <strong>Name:</strong> {selectedAnalysis.resume?.name || "N/A"}

              </p>

              <p>

                <strong>Email:</strong> {selectedAnalysis.resume?.email || "N/A"}

              </p>

              <p>

                <strong>Phone:</strong> {selectedAnalysis.resume?.phone || "N/A"}

              </p>



              <h3>📊 Scores</h3>

              <div className="previous-score-grid">

                <div>

                  <span>Overall Score</span>

                  <strong>{selectedAnalysis.ai_analysis?.overall_score || 0}/100</strong>

                </div>

                <div>

                  <span>ATS Score</span>

                  <strong>{selectedAnalysis.ai_analysis?.ats_score || 0}/100</strong>

                </div>

                <div>

                  <span>Quality Score</span>

                  <strong>{selectedAnalysis.quality_analysis?.quality_score || 0}/100</strong>

                </div>

              </div>



              <h3>💪 Strengths</h3>

              <ul>

                {(selectedAnalysis.ai_analysis?.strengths || []).map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>



              <h3>⚠️ Weaknesses</h3>

              <ul>

                {(selectedAnalysis.ai_analysis?.weaknesses || []).map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>



              <h3>🎯 Skill Gap</h3>

              <p>

                <strong>Skill Match:</strong>{" "}

                {selectedAnalysis.skill_gap?.match_percentage || 0}%

              </p>

              <ul>

                {(selectedAnalysis.skill_gap?.missing_skills || []).map((skill, index) => (

                  <li key={index}>{skill}</li>

                ))}

              </ul>



              <h3>🚀 Improvement Plan</h3>

              <ul>

                {(selectedAnalysis.improvement_analysis?.priority_improvements || []).map(

                  (item, index) => (

                    <li key={index}>{item}</li>

                  )

                )}

              </ul>

            </div>

          </section>

        )}



        {result && result.ai_analysis && (

          <section className="results">

            <h2>Resume Analysis 📊</h2>



            <div className="score-grid">

              <div className="score-card">

                <h3>Overall Score</h3>

                <div

                  className="score-circle"

                  style={{

                    "--score": `${result.ai_analysis.overall_score * 3.6}deg`,

                  }}

                >

                  <div className="score-circle-inner">

                    <span className="score-number">

                      {result.ai_analysis.overall_score}

                    </span>

                    <span className="score-total">/100</span>

                  </div>

                </div>

                <p className="score-label">Resume Quality</p>

              </div>



              <div className="score-card">

                <h3>ATS Score</h3>

                <div

                  className="score-circle"

                  style={{

                    "--score": `${result.ai_analysis.ats_score * 3.6}deg`,

                  }}

                >

                  <div className="score-circle-inner">

                    <span className="score-number">{result.ai_analysis.ats_score}</span>

                    <span className="score-total">/100</span>

                  </div>

                </div>

                <p className="score-label">ATS Compatibility</p>

              </div>

            </div>



            <div className="analysis-card">

              <h3>💪 Strengths</h3>

              <ul>

                {result.ai_analysis.strengths?.map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>

            </div>



            <div className="analysis-card">

              <h3>⚠️ Weaknesses</h3>

              <ul>

                {result.ai_analysis.weaknesses?.map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>

            </div>



            <div className="analysis-card">

              <h3>🧠 Missing Skills</h3>

              <ul>

                {result.ai_analysis.missing_skills?.map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>

            </div>



            <div className="analysis-card">

              <h3>🚀 Suggestions</h3>

              <ul>

                {result.ai_analysis.suggestions?.map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>

            </div>

          </section>

        )}



        {improvementAnalysis && (

          <section className="improvement-section">

            <div className="improvement-header">

              <h2>📝 Resume Improvement Plan</h2>

              <p>AI-powered suggestions to make your resume stronger and more ATS-friendly.</p>

            </div>



            <div className="improvement-card">

              <h3>🎯 Priority Improvements</h3>

              <ul>

                {improvementAnalysis.priority_improvements.map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>

            </div>



            <div className="improvement-card">

              <h3>📌 Section-wise Suggestions</h3>



              <div className="suggestion-section">

                <h4>👤 Summary</h4>

                <ul>

                  {improvementAnalysis.section_suggestions.summary.map((item, index) => (

                    <li key={index}>{item}</li>

                  ))}

                </ul>

              </div>



              <div className="suggestion-section">

                <h4>💻 Skills</h4>

                <ul>

                  {improvementAnalysis.section_suggestions.skills.map((item, index) => (

                    <li key={index}>{item}</li>

                  ))}

                </ul>

              </div>



              <div className="suggestion-section">

                <h4>🚀 Projects</h4>

                <ul>

                  {improvementAnalysis.section_suggestions.projects.map((item, index) => (

                    <li key={index}>{item}</li>

                  ))}

                </ul>

              </div>



              <div className="suggestion-section">

                <h4>💼 Experience</h4>

                <ul>

                  {improvementAnalysis.section_suggestions.experience.map((item, index) => (

                    <li key={index}>{item}</li>

                  ))}

                </ul>

              </div>



              <div className="suggestion-section">

                <h4>🏆 Certifications</h4>

                <ul>

                  {improvementAnalysis.section_suggestions.certifications.map((item, index) => (

                    <li key={index}>{item}</li>

                  ))}

                </ul>

              </div>

            </div>



            <div className="improvement-card">

              <h3>🤖 ATS Improvements</h3>

              <ul>

                {improvementAnalysis.ats_improvements.map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>

            </div>



            <div className="improvement-card">

              <h3>🔑 Keyword Suggestions</h3>

              <ul>

                {improvementAnalysis.keyword_suggestions.map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>

            </div>



            <div className="improvement-card final-advice">

              <h3>💡 Final Advice</h3>

              <ul>

                {improvementAnalysis.final_advice.map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>

            </div>

          </section>

        )}



        {result && (

          <div className="download-report-container">

            <button onClick={downloadReport} className="download-report-button">

              📥 Download Full Report

            </button>

          </div>

        )}



        {result && result.quality_analysis && (

          <section className="quality-section">

            <div className="quality-header">

              <h2>📋 Resume Quality</h2>

              <p>A detailed check of your resume structure and content quality.</p>

            </div>



            <div className="quality-score-card">

              <h3>Quality Score</h3>

              <div className="quality-score">

                {result.quality_analysis.quality_score}/100

              </div>

            </div>



            <div className="quality-grid">

              <div className="quality-card">

                <h3>📞 Contact Information</h3>

                <ul>

                  <li>

                    Email:

                    {result.quality_analysis.contact_information.email

                      ? " ✅ Present"

                      : " ❌ Missing"}

                  </li>

                  <li>

                    Phone:

                    {result.quality_analysis.contact_information.phone

                      ? " ✅ Present"

                      : " ❌ Missing"}

                  </li>

                  <li>

                    LinkedIn:

                    {result.quality_analysis.contact_information.linkedin

                      ? " ✅ Present"

                      : " ❌ Missing"}

                  </li>

                  <li>

                    GitHub:

                    {result.quality_analysis.contact_information.github

                      ? " ✅ Present"

                      : " ❌ Missing"}

                  </li>

                </ul>

              </div>



              <div className="quality-card">

                <h3>📑 Resume Sections</h3>

                <ul>

                  {Object.entries(result.quality_analysis.sections).map(([section, present]) => (

                    <li key={section}>

                      {section}: {present ? " ✅ Present" : " ❌ Missing"}

                    </li>

                  ))}

                </ul>

              </div>

            </div>



            <div className="quality-card content-quality">

              <h3>📊 Content Quality</h3>

              <div className="content-stats">

                <div>

                  <strong>{result.quality_analysis.content_quality.action_verbs}</strong>

                  <span>Action Verbs</span>

                </div>

                <div>

                  <strong>{result.quality_analysis.content_quality.quantified_achievements}</strong>

                  <span>Measurable Results</span>

                </div>

                <div>

                  <strong>{result.quality_analysis.content_quality.word_count}</strong>

                  <span>Words</span>

                </div>

                <div>

                  <strong>{result.quality_analysis.content_quality.project_count}</strong>

                  <span>Projects</span>

                </div>

                <div>

                  <strong>{result.quality_analysis.content_quality.skill_count}</strong>

                  <span>Skills</span>

                </div>

              </div>

            </div>



            <div className="quality-card">

              <h3>💪 Strengths</h3>

              <ul>

                {result.quality_analysis.strengths.map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>

            </div>



            <div className="quality-card">

              <h3>⚠️ Issues</h3>

              <ul>

                {result.quality_analysis.issues.map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>

            </div>



            <div className="quality-card">

              <h3>💡 Recommendations</h3>

              <ul>

                {result.quality_analysis.recommendations.map((item, index) => (

                  <li key={index}>{item}</li>

                ))}

              </ul>

            </div>

          </section>

        )}



        {result && result.resume && (

          <section className="job-match">

            <div className="job-match-header">

              <h2>🎯 Job Match Analyzer</h2>

              <p>Paste a job description to see how well your resume matches the role.</p>

            </div>



            <textarea

              className="job-description-input"

              placeholder="Paste the job description here..."

              value={jobDescription}

              onChange={(e) => setJobDescription(e.target.value)}

              rows={10}

            />



            <button

              className="match-btn"

              onClick={matchJob}

              disabled={jobLoading}

            >

              {jobLoading ? "Matching with AI... 🧠" : "Check Job Match 🎯"}

            </button>



            {jobError && <p className="error">❌ {jobError}</p>}



            {jobLoading && (

              <div className="job-loading">

                🧠 AI is comparing your resume with the job...

              </div>

            )}



            {jobMatch && (

              <div className="job-match-results">

                <div className="match-score-card">

                  <h3>Job Match Score</h3>

                  <div className="match-score">{jobMatch.match_score}%</div>

                  <p>Resume ↔ Job Compatibility</p>

                </div>



                <div className="job-result-card">

                  <h3>✅ Matched Skills</h3>

                  <div className="skill-list">

                    {jobMatch.matched_skills?.map((skill, index) => (

                      <span className="matched-tag" key={index}>

                        {skill}

                      </span>

                    ))}

                  </div>

                </div>



                <div className="job-result-card">

                  <h3>❌ Missing Skills</h3>

                  <div className="skill-list">

                    {jobMatch.missing_skills?.map((skill, index) => (

                      <span className="missing-tag" key={index}>

                        {skill}

                      </span>

                    ))}

                  </div>

                </div>



                <div className="job-result-card">

                  <h3>💪 Your Strengths</h3>

                  <ul>

                    {jobMatch.strengths?.map((item, index) => (

                      <li key={index}>{item}</li>

                    ))}

                  </ul>

                </div>



                <div className="job-result-card">

                  <h3>⚠️ Areas to Improve</h3>

                  <ul>

                    {jobMatch.weaknesses?.map((item, index) => (

                      <li key={index}>{item}</li>

                    ))}

                  </ul>

                </div>



                <div className="job-result-card">

                  <h3>🚀 Recommendations</h3>

                  <ul>

                    {jobMatch.recommendations?.map((item, index) => (

                      <li key={index}>{item}</li>

                    ))}

                  </ul>

                </div>

              </div>

            )}

          </section>

        )}



        {skillGapResult && (

          <section className="skill-gap-section">

            <div className="skill-gap-header">

              <h2>🧠 Skill Gap Analysis</h2>

              <p>See which skills you already have and which skills you need for this job.</p>

            </div>



            <div className="skill-match-score">

              <h3>Skill Match</h3>

              <div className="skill-score">{skillGapResult.match_percentage}%</div>

            </div>



            <div className="skill-gap-grid">

              <div className="skill-card">

                <h3>✅ Your Skills</h3>

                <ul>

                  {skillGapResult.resume_skills?.map((skill, index) => (

                    <li key={index}>{skill}</li>

                  ))}

                </ul>

              </div>



              <div className="skill-card">

                <h3>🎯 Matched Skills</h3>

                <ul>

                  {skillGapResult.matched_skills?.map((skill, index) => (

                    <li key={index}>{skill}</li>

                  ))}

                </ul>

              </div>



              <div className="skill-card missing-skills">

                <h3>❌ Missing Skills</h3>

                {skillGapResult.missing_skills?.length > 0 ? (

                  <ul>

                    {skillGapResult.missing_skills.map((skill, index) => (

                      <li key={index}>{skill}</li>

                    ))}

                  </ul>

                ) : (

                  <p>🎉 Excellent! No major skill gaps detected.</p>

                )}

              </div>

            </div>



            <div className="skill-gap-summary">

              <h3>📊 Skill Gap Summary</h3>

              <p>

                You are missing <strong>{skillGapResult.skill_gap_count}</strong>{" "}

                required skill(s) for this job.

              </p>

            </div>

          </section>

        )}

      </main>

    </div>

  );

}



export default App;