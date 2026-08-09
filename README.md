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