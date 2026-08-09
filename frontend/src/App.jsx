import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  // ============================================================
  // STATE
  // ============================================================

  const [candidates, setCandidates] = useState([]);
  const [candidate, setCandidate] = useState(null);
  const [loadingCandidates, setLoadingCandidates] = useState(true);

  const [sessionId, setSessionId] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState(null);

  const [started, setStarted] = useState(false);
  const [done, setDone] = useState(false);

  const [loading, setLoading] = useState(false);
  const [questionNumber, setQuestionNumber] = useState(0);

  const [error, setError] = useState("");

  // ============================================================
  // LOAD CANDIDATES FROM BACKEND
  // ============================================================

  useEffect(() => {
    const loadCandidates = async () => {
      try {
        setLoadingCandidates(true);
        setError("");

        const response = await fetch(`${API_URL}/api/candidates`);

        if (!response.ok) {
          throw new Error("Failed to load candidates");
        }

        const data = await response.json();

        setCandidates(data.candidates || []);
      } catch (err) {
        setError(
          err.message || "Unable to load candidates from the backend."
        );
      } finally {
        setLoadingCandidates(false);
      }
    };

    loadCandidates();
  }, []);

  // ============================================================
  // START INTERVIEW
  // ============================================================

  const startInterview = async () => {
    if (!candidate) {
      setError("Please select a candidate first.");
      return;
    }

    setLoading(true);
    setError("");
    setFeedback(null);
    setDone(false);

    const newSessionId = `frontend-${Date.now()}`;

    setSessionId(newSessionId);

    try {
      const response = await fetch(`${API_URL}/api/interview`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sessionId: newSessionId,
          candidate: candidate,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.error ||
            "Unable to start interview"
        );
      }

      if (data.error) {
        throw new Error(data.error);
      }

      setQuestion(data.reply);
      setStarted(true);
      setQuestionNumber(1);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the interview server."
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // SUBMIT ANSWER
  // ============================================================

  const submitAnswer = async () => {
    if (!answer.trim()) {
      setError("Please enter your answer before submitting.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/api/interview`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sessionId: sessionId,
          message: answer,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.error ||
            "Unable to submit answer"
        );
      }

      if (data.error) {
        throw new Error(data.error);
      }

      setAnswer("");

      // Interview completed
      if (data.done) {
        setDone(true);
        setStarted(false);
        setFeedback(data.feedback || null);
        return;
      }

      // Next question / follow-up
      setQuestion(data.reply);

      setQuestionNumber(
        (previous) => previous + 1
      );
    } catch (err) {
      setError(
        err.message ||
          "Something went wrong while submitting your answer."
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // RESTART
  // ============================================================

  const restartInterview = () => {
    setSessionId("");
    setQuestion("");
    setAnswer("");
    setFeedback(null);

    setStarted(false);
    setDone(false);

    setQuestionNumber(0);
    setError("");
  };

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className="app">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <header className="header">

        <div>
          <h1>AI Interview Agent</h1>

          <p>
            Adaptive technical interview platform
          </p>
        </div>

        {started && !done && (
          <div className="progress">
            Question {questionNumber} / 8
          </div>
        )}

      </header>

      <main className="container">

        {/* ====================================================
            CANDIDATE SELECTION
        ==================================================== */}

        {!started && !done && (

          <section className="card welcome-card">

            <div className="badge">
              AI POWERED INTERVIEW
            </div>

            <h2>
              Select Candidate
            </h2>

            <p className="description">
              Select a candidate to begin a personalized
              AI-powered technical interview.
            </p>

            {/* Candidate dropdown */}

            <div className="candidate-selector">

              <label htmlFor="candidate">
                Candidate
              </label>

              {loadingCandidates ? (

                <p>
                  Loading candidates...
                </p>

              ) : (

                <select
                  id="candidate"
                  value={
                    candidate?.member?.id || ""
                  }
                  onChange={(event) => {

                    const selectedCandidate =
                      candidates.find(
                        (item) =>
                          item.member.id ===
                          event.target.value
                      );

                    setCandidate(
                      selectedCandidate || null
                    );

                    setError("");
                  }}
                >

                  <option value="">
                    Select a candidate
                  </option>

                  {candidates.map((item) => (

                    <option
                      key={item.member.id}
                      value={item.member.id}
                    >
                      {item.member.name} -{" "}
                      {item.member.jobRole}
                    </option>

                  ))}

                </select>

              )}

            </div>

            {/* Candidate information */}

            {candidate && (

              <div className="candidate-grid">

                <div>
                  <span>Name</span>

                  <strong>
                    {candidate.member.name}
                  </strong>
                </div>

                <div>
                  <span>Role</span>

                  <strong>
                    {candidate.member.jobRole}
                  </strong>
                </div>

                <div>
                  <span>Experience</span>

                  <strong>
                    {candidate.member.yearsExperience} years
                  </strong>
                </div>

                <div>
                  <span>Education</span>

                  <strong>
                    {candidate.member.education}
                  </strong>
                </div>

                <div>
                  <span>Candidate ID</span>

                  <strong>
                    {candidate.member.id}
                  </strong>
                </div>

                <div>
                  <span>Missions Completed</span>

                  <strong>
                    {candidate.signals?.missionsCompleted ??
                      "N/A"}
                  </strong>
                </div>

              </div>

            )}

            {/* Error */}

            {error && (
              <div className="error">
                {error}
              </div>
            )}

            {/* Start button */}

            <button
              className="primary-button"
              onClick={startInterview}
              disabled={
                loading ||
                loadingCandidates ||
                !candidate
              }
            >

              {loading
                ? "Starting Interview..."
                : "Start Interview"}

            </button>

          </section>

        )}

        {/* ====================================================
            INTERVIEW
        ==================================================== */}

        {started && !done && (

          <section className="interview-layout">

            {/* Question */}

            <div className="card question-card">

              <div className="question-label">
                TECHNICAL QUESTION
              </div>

              <h2>
                Question {questionNumber}
              </h2>

              <div className="question">
                {question}
              </div>

              <textarea
                value={answer}
                onChange={(event) =>
                  setAnswer(event.target.value)
                }
                placeholder="Type your answer here..."
                rows="9"
                disabled={loading}
              />

              {error && (
                <div className="error">
                  {error}
                </div>
              )}

              <button
                className="primary-button"
                onClick={submitAnswer}
                disabled={loading}
              >

                {loading
                  ? "Evaluating..."
                  : "Submit Answer"}

              </button>

            </div>

            {/* Progress sidebar */}

            <aside className="card info-card">

              <h3>
                Interview Progress
              </h3>

              <div className="progress-bar">

                <div
                  className="progress-fill"
                  style={{
                    width: `${Math.min(
                      (questionNumber / 8) * 100,
                      100
                    )}%`,
                  }}
                />

              </div>

              <p>
                The interview dynamically adapts
                based on the candidate's previous
                learning performance and answers.
              </p>

              <div className="tip">

                <strong>
                  Tip
                </strong>

                <p>
                  Explain your approach clearly and
                  mention practical implementation
                  details where possible.
                </p>

              </div>

            </aside>

          </section>

        )}

        {/* ====================================================
            FINAL FEEDBACK
        ==================================================== */}

        {done && (

          <section className="card feedback-card">

            <div className="success-icon">
              ✓
            </div>

            <h2>
              Interview Complete
            </h2>

            <p className="description">
              Thank you for completing the AI interview.
            </p>

            {feedback && (

              <div className="feedback">

                {/* Overall score */}

                {feedback.overall_score !==
                  undefined && (

                  <div className="score">

                    <span>
                      Overall Score
                    </span>

                    <strong>
                      {feedback.overall_score}
                    </strong>

                    <small>
                      / 10
                    </small>

                  </div>

                )}

                {/* Technical strengths */}

                <div className="feedback-section">

                  <h3>
                    Technical Strengths
                  </h3>

                  <ul>

                    {(feedback.technical_strengths ||
                      []).map(
                      (item, index) => (

                        <li key={index}>
                          {item}
                        </li>

                      )
                    )}

                  </ul>

                </div>

                {/* Knowledge gaps */}

                <div className="feedback-section">

                  <h3>
                    Knowledge Gaps
                  </h3>

                  <ul>

                    {(feedback.knowledge_gaps ||
                      []).map(
                      (item, index) => (

                        <li key={index}>
                          {item}
                        </li>

                      )
                    )}

                  </ul>

                </div>

                {/* Topics */}

                <div className="feedback-section">

                  <h3>
                    Topics to Revisit
                  </h3>

                  <ul>

                    {(feedback.topics_to_revisit ||
                      []).map(
                      (item, index) => (

                        <li key={index}>
                          {item}
                        </li>

                      )
                    )}

                  </ul>

                </div>

                {/* Communication */}

                {feedback.communication_assessment && (

                  <div className="feedback-section">

                    <h3>
                      Communication Assessment
                    </h3>

                    <p>
                      {feedback.communication_assessment}
                    </p>

                  </div>

                )}

                {/* Recommendation */}

                {feedback.recommendation && (

                  <div className="recommendation">

                    <h3>
                      Recommendation
                    </h3>

                    <p>
                      {feedback.recommendation}
                    </p>

                  </div>

                )}

                {/* Summary */}

                {feedback.summary && (

                  <div className="feedback-section">

                    <h3>
                      Summary
                    </h3>

                    <p>
                      {feedback.summary}
                    </p>

                  </div>

                )}

              </div>

            )}

            <button
              className="primary-button"
              onClick={restartInterview}
            >
              Start New Interview
            </button>

          </section>

        )}

      </main>

    </div>
  );
}

export default App;