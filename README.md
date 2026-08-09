# 🤖 AI Interview Agent

> **Build the interviewer, not the interview.**

An AI-powered technical interview platform that conducts personalized,
multi-turn technical interviews based on a candidate's learning journey
through the 31-day AI Cohort curriculum.

The system analyzes candidate progress, creates a personalized interview
plan, generates technical questions, evaluates answers, asks adaptive
follow-up questions, and provides structured feedback at the end.

---

## 🎯 Problem Statement

The AI Cohort covers modern AI engineering topics including:

- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Prompt Engineering
- Agentic AI
- Model Context Protocol (MCP)
- AI Deployment
- Production AI Systems

After completing the cohort, learners should be able to confidently explain
the systems they built and the engineering decisions behind them.

The **AI Interview Agent** provides a realistic technical interview
experience based on each candidate's actual learning journey.

---

## ✨ Key Features

### 👤 Personalized Interviews

The interview is personalized using the selected candidate's:

- Learning progress
- Completed missions
- Attempts
- Skipped topics
- Learning signals
- Curriculum coverage

### 📚 Curriculum-Based Questions

Questions are generated from the provided 31-day AI Cohort curriculum
instead of using a fixed question bank.

### 🔄 Adaptive Follow-Up Questions

Candidate answers are evaluated during the interview.

If an answer requires clarification or deeper technical exploration, the
agent generates an adaptive follow-up question.

The system allows a maximum of one follow-up per curriculum topic.

### 💬 Multi-Turn Conversation

The backend maintains the interview context using a session ID.

Each session maintains:

- Candidate information
- Interview plan
- Current question
- Previous questions
- Candidate answers
- Evaluations
- Transcript
- Follow-up state
- Completion state
- Final feedback

### 📊 Structured Evaluation

Every candidate answer is evaluated by the AI system.

### 📝 Final Feedback

At the end of the interview, the candidate receives structured feedback
including:

- Overall score
- Technical strengths
- Knowledge gaps
- Topics to revisit
- Communication assessment
- Recommendation
- Summary

### 👥 Multiple Candidates

The frontend retrieves the available candidate profiles and allows the user
to select a candidate before starting an interview.

---

## 🏗️ System Architecture

```text
┌─────────────────────────────────────────┐
│             React Frontend              │
│                                         │
│  Candidate Selection                    │
│  Interview Interface                    │
│  Progress Tracking                      │
│  Final Feedback                         │
└───────────────────┬─────────────────────┘
                    │
                    │ HTTP
                    ▼
┌─────────────────────────────────────────┐
│            FastAPI Backend              │
│                                         │
│  GET  /                                 │
│  GET  /api/candidates                   │
│  POST /api/interview                    │
└───────────────────┬─────────────────────┘
                    │
       ┌────────────┼────────────┐
       │            │            │
       ▼            ▼            ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ Candidate  │ │ Curriculum │ │  Session   │
│ Analyzer   │ │   Loader   │ │  Manager   │
└─────┬──────┘ └─────┬──────┘ └─────┬──────┘
      │              │              │
      └──────────────┼──────────────┘
                     ▼
            ┌─────────────────┐
            │ Interview       │
            │ Planner         │
            └────────┬────────┘
                     ▼
            ┌─────────────────┐
            │ AI Interviewer  │
            │                 │
            │ Question        │
            │ Follow-Up       │
            │ Generation      │
            └────────┬────────┘
                     ▼
            ┌─────────────────┐
            │ Answer          │
            │ Evaluator       │
            └────────┬────────┘
                     ▼
            ┌─────────────────┐
            │ Feedback        │
            │ Generator       │
            └─────────────────┘

## 🔄 Interview Flow
                    Select Candidate
                           │
                           ▼
                  Analyze Candidate
                           │
                           ▼
                Create Interview Plan
                           │
                           ▼
                  Generate Question
                           │
                           ▼
                   Candidate Answer
                           │
                           ▼
                    Evaluate Answer
                           │
                           ▼
                 ┌──────────────────┐
                 │ Follow-Up Needed?│
                 └────────┬─────────┘
                    Yes   │   No
                     │    │    │
                     ▼    │    ▼
              Generate    │  Next Topic
              Follow-Up   │
                     │    │
                     └────┴──────┐
                                 ▼
                        Continue Interview
                                 │
                                 ▼
                         8 Candidate Answers
                                 │
                                 ▼
                         Final Evaluation
                                 │
                                 ▼
                          Final Feedback

🛠️ Technology Stack

| Layer             | Technology                   |
| ----------------- | ---------------------------- |
| Frontend          | React, Vite, JavaScript, CSS |
| Backend           | Python, FastAPI, Pydantic    |
| AI                | Grok                         |
| Data              | JSON                         |
| API Communication | REST                         |
| Version Control   | Git, GitHub                  |

📁 Project Structure

ai-interview-agent/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   │
│   │   └── services/
│   │       ├── data_loader.py
│   │       ├── candidate_analyzer.py
│   │       ├── planner.py
│   │       ├── session_manager.py
│   │       ├── ai_interviewer.py
│   │       ├── answer_evaluator.py
│   │       └── feedback_generator.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── PROMPTS.md
└── README.md

🔌 API Endpoints
Health Check

GET /
Returns:

{
  "message": "AI Interview Agent is running 🚀"
}
Get Candidates
GET /api/candidates

Returns the available candidate profiles.

Start Interview
POST /api/interview

Example:

{
  "sessionId": "frontend-123456",
  "candidate": {}
}
Submit Answer

The same endpoint is used to continue an existing interview:

POST /api/interview

Example:

{
  "sessionId": "frontend-123456",
  "message": "Candidate's answer"
}

The API returns either the next interview question or the final feedback
when the interview is complete.

💻 Running Locally
Backend
cd backend
python -m venv venv

Activate the environment on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start the FastAPI server:

uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000
Frontend

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173
🤖 AI Usage

AI assistance was used throughout development for:

Architecture planning
Candidate personalization
Interview planning
Adaptive follow-up logic
LLM integration
Backend development
React frontend development
Debugging
Testing
UI refinement

The detailed AI usage log is available here:

👉 PROMPTS.md

🧪 Interview Validation

The complete interview flow was tested end-to-end:

Select a candidate
Analyze candidate profile
Generate personalized interview plan
Generate technical question
Submit candidate answer
Evaluate answer
Generate adaptive follow-up when required
Continue through curriculum topics
Complete the interview
Generate final feedback

The system was also tested with different candidate profiles.

🚀 Live Demo

Coming soon

The live demo URL will be added here after deployment.

🏆 Hackathon

Built for the AI Cohort Hackathon

Challenge

The Interview Agent

Build the interviewer, not the interview.