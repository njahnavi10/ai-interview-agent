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

  |

```


## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Pydantic

### AI

- Grok

### Data

- Candidate Profiles JSON
- 31-Day AI Cohort Curriculum JSON

### Development

- Git
- GitHub
- VS Code

## Key API Endpoints

### Health Check

```http
GET /
```

### Get Candidates

```http
GET /api/candidates
```

Returns the available candidate profiles.

### Interview

```http
POST /api/interview
```

The same endpoint is used to start and continue an interview.

### Start Interview

```json
{
  "sessionId": "frontend-123456",
  "candidate": {}
}
```

### Submit Answer

```json
{
  "sessionId": "frontend-123456",
  "message": "Candidate answer"
}
```

## Project Structure

```text
ai-interview-agent/
|
+-- backend/
|   +-- app/
|       +-- main.py
|       +-- models.py
|       +-- services/
|           +-- data_loader.py
|           +-- candidate_analyzer.py
|           +-- planner.py
|           +-- session_manager.py
|           +-- ai_interviewer.py
|           +-- answer_evaluator.py
|           +-- feedback_generator.py
|   +-- requirements.txt
|
+-- frontend/
|   +-- src/
|       +-- App.jsx
|       +-- App.css
|       +-- main.jsx
|   +-- package.json
|
+-- PROMPTS.md
+-- README.md
```

## Running Locally

### Backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## AI Usage Log

The AI-assisted development process is documented in:

[**PROMPTS.md**](PROMPTS.md)

The log covers architecture planning, implementation, debugging, LLM
integration, frontend development, testing, and refinement.

## Live Demo

https://ai-interview-agent-frontend-6uuq.onrender.com/
