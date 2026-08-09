# AI Interview Agent

An AI-powered technical interview platform that conducts personalized,
multi-turn interviews based on a candidate's learning journey through the
31-day AI Cohort curriculum.

The system analyzes the candidate's learning progress, creates a
personalized interview plan, generates technical questions, evaluates
answers, asks adaptive follow-up questions, and provides structured
feedback at the end of the interview.

---

## Problem Statement

### The Interview Agent

Build the interviewer, not the interview.

The AI Cohort covers modern AI engineering topics including:

- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Prompt Engineering
- Agentic AI
- Model Context Protocol (MCP)
- AI Deployment
- Production AI Systems

After completing the cohort, learners need to be able to explain the
systems they built and the engineering decisions behind them.

The AI Interview Agent addresses this by conducting personalized technical
interviews based on each candidate's learning journey.

---

## Key Features

### Personalized Interviews

The interview is generated based on the selected candidate's profile,
learning progress, completed missions, and curriculum information.

### Curriculum-Based Questions

Questions are generated using topics from the provided 31-day AI Cohort
curriculum.

### Adaptive Follow-Ups

Candidate answers are evaluated during the interview. When additional
clarification or deeper evaluation is needed, the system generates a
follow-up question.

The implementation limits follow-ups to one per curriculum topic.

### Multi-Turn Conversation

The backend maintains interview state using a session ID.

The session stores:

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

### Structured Evaluation

Each candidate answer is evaluated by the AI system.

### Final Feedback

After the interview, the candidate receives structured feedback including:

- Overall score
- Technical strengths
- Knowledge gaps
- Topics to revisit
- Communication assessment
- Recommendation
- Summary

### Multiple Candidates

The frontend retrieves the available candidate profiles and allows the
interviewer to select a candidate before starting the interview.

---

## System Architecture

```text
                 ┌──────────────────────┐
                 │    React Frontend    │
                 │                      │
                 │ Candidate Selection  │
                 │ Interview Interface  │
                 │ Final Feedback       │
                 └──────────┬───────────┘
                            │
                            │ HTTP
                            ▼
                 ┌──────────────────────┐
                 │   FastAPI Backend    │
                 │                      │
                 │ /api/candidates      │
                 │ /api/interview       │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
      Candidate         Curriculum       Session
       Analyzer           Loader         Manager
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Interview Planner    │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │    AI Interviewer    │
                 │                      │
                 │ Question Generation  │
                 │ Follow-Up Questions  │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │  Answer Evaluator    │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Feedback Generator   │
                 └──────────────────────┘

Interview Flow
Select Candidate
       ↓
Analyze Candidate
       ↓
Create Personalized Interview Plan
       ↓
Select Curriculum Topic
       ↓
Generate Technical Question
       ↓
Candidate Answers
       ↓
Evaluate Answer
       ↓
Follow-Up Needed?
    ↙       ↘
  Yes        No
   ↓          ↓
Follow-Up   Next Topic
   ↓          ↓
   └──────────┘
       ↓
8 Candidate Answers
       ↓
Final Evaluation
       ↓
Structured Feedback
Technology Stack
Frontend
React
Vite
JavaScript / JSX
CSS
Backend
Python
FastAPI
Pydantic
AI
LLM-based question generation
LLM-based answer evaluation
LLM-based adaptive follow-ups
LLM-based final feedback generation
Data
Candidate Profiles JSON
31-Day AI Cohort Curriculum JSON
Development
Git
GitHub
VS Code
Project Structure
AI-Interview-Agent/
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
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── PROMPTS.md
├── README.md
└── ...
API Endpoints
Health Check
GET /

Returns:

{
  "message": "AI Interview Agent is running 🚀"
}
Get Candidates
GET /api/candidates

Returns the available candidate profiles.

Interview
POST /api/interview

The same endpoint is used to start and continue an interview.

Start Interview

Example request:

{
  "sessionId": "frontend-123456",
  "candidate": {
    "member": {
      "name": "Candidate Name"
    }
  }
}
Continue Interview

Example request:

{
  "sessionId": "frontend-123456",
  "message": "Candidate's answer"
}

The response contains the next question or final feedback when the
interview is complete.

Interview Constraints

The current implementation uses:

8 candidate answers as the maximum interview length
Maximum one adaptive follow-up per curriculum topic
Session-based interview state
Curriculum-based topic selection
Candidate-specific interview planning

These constraints keep the interview focused while still allowing
adaptive interaction.

Running Locally
Backend

Navigate to the backend:

cd backend

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start FastAPI:

uvicorn app.main:app --reload

The backend will run at:

http://127.0.0.1:8000
Frontend

Open another terminal:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will normally be available at:

http://localhost:5173
Environment Variables

API credentials and other sensitive configuration should be stored as
environment variables and should not be committed to Git.

Example:

LLM_API_KEY=your_api_key

Do not place real API keys in:

GitHub
React source code
README files
PROMPTS.md
Screenshots
AI Usage Log

The AI-assisted development process used during the hackathon is documented
in:

PROMPTS.md

The log covers architecture planning, implementation, debugging, frontend
development, LLM integration, testing, and refinement.

Testing

The complete application was tested through the full interview flow:

Candidate selection
Candidate analysis
Personalized interview planning
Initial question generation
Candidate answer submission
Answer evaluation
Adaptive follow-up generation
Progression through curriculum topics
Interview completion
Final feedback generation

The system was also tested with different candidate profiles.

LLM Provider During Development

The initial implementation used the Gemini API.

During development and repeated testing, the available Gemini API quota was
exceeded and the API returned a 429 RESOURCE_EXHAUSTED response.

To continue development and testing, the LLM provider was changed to Grok.

The core interview architecture remained unchanged. The LLM provider is
used behind dedicated service functions for:

Question generation
Follow-up generation
Answer evaluation
Final feedback generation
Security Considerations

The application follows basic security practices for the development
environment:

API keys are kept outside source code.
User input is validated using Pydantic models.
LLM API credentials are handled by the backend rather than the frontend.
The React application communicates with the FastAPI backend through HTTP.
CORS is configured for the frontend development origin.
Future Improvements

Possible future improvements include:

Persistent database-backed interview sessions
Authentication and authorization
More advanced candidate analytics
Retrieval-Augmented Generation for curriculum grounding
More sophisticated interview difficulty adaptation
Interview history and analytics dashboard
Production deployment and monitoring
Automated evaluation benchmarks
Hackathon

This project was developed for the AI Cohort hackathon challenge:

The Interview Agent