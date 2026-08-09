# AI Interview Agent - AI Usage Log

## Project

**AI Interview Agent**

## Purpose

This document records the AI-assisted development process used during the hackathon while building the AI Interview Agent.

AI assistance was used for system design, implementation guidance, debugging, API development, frontend development, testing, and refinement.

The AI-assisted development process was iterative. The application was implemented, tested, debugged, and refined throughout development.


# 1. Project Understanding and Architecture

### Prompt / Task

Understand the hackathon problem statement and design an AI Interview Agent that conducts a personalized, multi-turn technical interview based on a candidate's learning journey through the 31-day AI Cohort curriculum.

### Purpose

To define the overall architecture and interview flow before implementing the application.

### Result

The application was designed around the following flow:

Candidate Data
    ↓
Candidate Analysis
    ↓
Personalized Interview Plan
    ↓
Curriculum Topic Selection
    ↓
AI Question Generation
    ↓
Candidate Answer
    ↓
Answer Evaluation
    ↓
Adaptive Follow-Up
    ↓
Next Curriculum Topic
    ↓
Final Evaluation and Feedback

The system was designed to behave as an interviewer rather than a fixed questionnaire.

---

# 2. Candidate Data Integration

### Prompt / Task

Design the interview system so that it can fetch candidate information from the provided candidate profiles and personalize the interview according to the candidate's learning progress.

### Purpose

To avoid asking the same fixed questions to every candidate.

### Result

The backend loads candidate profiles and exposes them through:

    GET /api/candidates

The selected candidate is passed to the candidate analysis and interview planning stages.

Candidate information such as:

- Job role
- Years of experience
- Education
- Completed missions
- Mission attempts
- Skipped topics
- Learning signals

is used as input to the personalized interview planning process.

---

# 3. Curriculum Integration

### Prompt / Task

Design a mechanism for the interviewer to use the provided 31-day AI Cohort curriculum when generating technical interview questions.

### Purpose

To ensure that interview questions are based on topics the candidate has actually encountered during the cohort.

### Result

The backend loads the curriculum data and retrieves the relevant curriculum day before generating questions.

The interview planner selects curriculum topics and the AI interviewer receives the corresponding curriculum information when generating questions.

This allows questions to be grounded in the actual cohort topics.

---

# 4. Candidate Analysis

### Prompt / Task

Design a candidate analysis stage that converts the candidate's learning signals and mission history into information that can be used for interview planning.

### Purpose

To make the interview personalized according to the candidate's learning journey.

### Result

A dedicated candidate analyzer was implemented:

    analyze_candidate(candidate)

The resulting analysis is passed to the interview planner.

---

# 5. Personalized Interview Planning

### Prompt / Task

Create a personalized interview plan using the candidate analysis and curriculum information, with a target of at least eight interview
questions.

### Purpose

To determine the sequence of technical topics that the interviewer should cover.

### Result

A dedicated planner was implemented:

    create_interview_plan(analysis, num_questions=8)

The generated plan contains curriculum topics that are used sequentially during the interview.

A safety check was also added to handle the case where no topics are returned by the planner.

---

# 6. AI Question Generation

### Prompt / Task

Design an AI interviewer that generates technical questions based on the selected curriculum topic, candidate profile, previous answers, and
curriculum information.

### Purpose

To make the interview questions personalized rather than static.

### Result

The backend uses:

    generate_ai_question()

The function receives:

- Current curriculum topic
- Candidate information
- Previous answers
- Curriculum day

and generates the next technical interview question.

---

# 7. Multi-Turn Interview State

### Prompt / Task

Design a session-based mechanism so that the FastAPI backend can maintain context across multiple interview requests.

### Purpose

The interview needs to continue from the previous question rather than starting over with every HTTP request.

### Result

The application uses a session ID to maintain interview state.

The session stores information including:

- Candidate
- Candidate analysis
- Interview plan
- Current question
- Questions
- Answers
- Evaluations
- Transcript
- Follow-up state
- Interaction count
- Final feedback
- Completion status

The main API endpoint supports both starting a new interview and continuing an existing interview.

---

# 8. Adaptive Follow-Up Questions

### Prompt / Task

Design an adaptive interview flow where the interviewer can generate a follow-up question when a candidate's answer requires clarification or
deeper evaluation.

### Purpose

To make the interview conversational and adaptive instead of scripted.

### Result

Each candidate answer is evaluated before deciding whether a follow-up is required.

The evaluator can return information such as:

    follow_up_needed
    follow_up_focus

If a follow-up is required, the system calls:

    generate_follow_up_question()

The implementation limits follow-ups to one per curriculum topic to prevent the interview from becoming unnecessarily long.

---

# 9. Answer Evaluation

### Prompt / Task

Design an answer evaluation stage that evaluates a candidate's response against the current interview question, candidate profile, and relevant
curriculum content.

### Purpose

To determine the quality of the candidate's response and support adaptive interview behavior.

### Result

A dedicated evaluator was implemented:

    evaluate_answer()

The evaluation is stored in the interview session and transcript.

The evaluation can also influence whether a follow-up question is generated.

---

# 10. Interview Transcript

### Prompt / Task

Design a structured transcript so that the complete interview interaction can be used for final evaluation.

### Purpose

To preserve the relationship between each question, answer, evaluation, topic, and follow-up status.

### Result

Each transcript entry stores:

- Curriculum day
- Topic title
- Question
- Candidate answer
- Evaluation
- Whether the question was a follow-up

This transcript is later passed to the final feedback generator.

---

# 11. Interview Length and Safety Limit

### Prompt / Task

Add a mechanism to prevent adaptive follow-ups from causing an interview to continue indefinitely.

### Purpose

To guarantee that the interview remains within a reasonable length.

### Result

A hard limit of eight candidate answers was implemented.

The session maintains:

    total_interactions

When the number of candidate answers reaches eight, the interview is completed and final feedback is generated.

This works together with the per-topic follow-up limit.

---

# 12. Final Feedback Generation

### Prompt / Task

Design a final feedback stage that summarizes the candidate's interview performance and provides actionable areas for improvement.

### Purpose

To provide useful feedback after the interview instead of simply ending the conversation.

### Result

A dedicated feedback generator was implemented:

    generate_final_feedback()

The final feedback can contain:

- Overall score
- Technical strengths
- Knowledge gaps
- Topics to revisit
- Communication assessment
- Recommendation
- Summary

The feedback is returned to the React frontend after the interview is completed.

---

# 13. FastAPI Backend

### Prompt / Task

Design the FastAPI backend API for the AI Interview Agent and connect the different interview services.

### Purpose

To provide a clean HTTP interface between the React frontend and the interview logic.

### Result

The final backend exposes:

    GET  /
    GET  /api/candidates
    POST /api/interview

The root endpoint is used as a basic health check.

The candidate endpoint returns the available candidate profiles.

The interview endpoint handles both starting and continuing interviews.

---

# 14. React Frontend Integration

### Prompt / Task

Connect the React frontend to the FastAPI backend and create a flow that allows the user to select a candidate and conduct the interview.

### Purpose

To provide a complete user-facing interview application.

### Result

The React frontend was connected to the FastAPI API.

The frontend supports:

- Candidate selection
- Candidate information display
- Starting an interview
- Displaying questions
- Entering answers
- Submitting answers
- Displaying adaptive follow-up questions
- Interview progress
- Final feedback
- Starting another interview

---

# 15. Multiple Candidate Support

### Prompt / Task

Ensure that the application does not use a hard-coded candidate and can start an interview for different candidates from the provided candidate
data.

### Purpose

The hackathon provides multiple candidate profiles, so the interviewer should personalize the interview for whichever candidate is selected.

### Result

The frontend retrieves candidates from the backend and allows a candidate to be selected before starting the interview.

The selected candidate is sent in the first interview request and is then used throughout the interview session.

---

# 16. Frontend UI Development

### Prompt / Task

Improve the React interview interface so that it looks like a modern AI technical interview platform rather than a basic form.

### Purpose

To improve usability and presentation quality for the final demonstration.

### Result

The frontend was refined with:

- Dark visual theme
- Candidate information cards
- Interview progress indicator
- Question cards
- Answer input area
- Loading states
- Error messages
- Final feedback sections
- Score display
- Start New Interview functionality

---

# 17. Frontend Debugging

### Prompt / Task

Debug issues where the frontend could not communicate correctly with the FastAPI backend and verify the API endpoint and candidate data flow.

### Purpose

To ensure the React application could successfully start and continue interviews.

### Result

The frontend API calls were aligned with the FastAPI endpoints and the candidate/session request structure.

CORS configuration was added to allow the React development server to communicate with the FastAPI backend.

---

# 18. Gemini API Integration

### Prompt / Task

Integrate an LLM into the FastAPI backend for question generation, follow-up generation, answer evaluation, and final feedback.

### Purpose

To provide the AI reasoning and conversational capabilities required by the interviewer.

### Result

The AI functionality was separated into service functions rather than placing all model logic directly inside the FastAPI endpoint.

The backend uses dedicated services for:

- AI question generation
- Follow-up question generation
- Answer evaluation
- Final feedback generation

---

# 19. Gemini API Quota Issue

### Problem

During testing, the Gemini API returned a quota error:

    429 RESOURCE_EXHAUSTED

The available Gemini request quota was reached during repeated interview testing.

### AI-Assisted Debugging

The error was analyzed to determine whether the problem was caused by the FastAPI interview logic or the external LLM provider.

### Result

The error was identified as an external Gemini API quota limitation rather than an interview-state or frontend/backend integration issue.

---

# 20. LLM Provider Change

### Problem

Continued testing was blocked by the Gemini API quota limitation.

### Decision

The LLM provider was changed from Gemini to Grok so development and end-to-end testing could continue.

### Purpose

To avoid being blocked by an external provider quota while keeping the same interview pipeline.

### Result

The existing interview architecture was retained.

The LLM provider change did not require changing the core interview flow:

    Question Generation
          ↓
    Answer Evaluation
          ↓
    Follow-Up Generation
          ↓
    Final Feedback

The application was subsequently tested successfully with the alternative LLM provider.

---

# 21. Backend Cleanup

### Prompt / Task

Identify temporary testing endpoints and unused imports that could be removed from the final FastAPI backend without affecting the actual
application.

### Purpose

To clean up development-only code before submission.

### Result

Temporary testing endpoints were removed after the application had been successfully tested.

The final backend focuses on the actual application endpoints:

    /
    /api/candidates
    /api/interview

---

# 22. Error Handling

### Prompt / Task

Improve error handling for missing sessions, missing curriculum days, missing messages, unavailable interview topics, and completed sessions.

### Purpose

To prevent unexpected failures during the interview.

### Result

The backend now handles cases such as:

- Session not found
- Interview already completed
- Missing candidate message
- Missing curriculum day
- No interview topics
- Invalid interview state

The frontend displays returned errors to the user.

---

# 23. Testing the Complete Interview

### Prompt / Task

Perform an end-to-end test of the AI Interview Agent and verify that the interview can progress through multiple questions, use adaptive follow-ups,and produce final feedback.

### Purpose

To verify that the individual components work together as a complete application.

### Result

The complete interview flow was tested successfully.

The application was able to:

1. Select a candidate
2. Analyze the candidate
3. Create an interview plan
4. Generate an initial question
5. Accept an answer
6. Evaluate the answer
7. Generate adaptive follow-ups when required
8. Continue to additional curriculum topics
9. Complete the interview
10. Generate structured final feedback

A completed interview produced a final score and detailed feedback.

---

# 24. Final System Architecture

The final application follows this general architecture:

    React Frontend
          │
          │ HTTP
          ▼
    FastAPI Backend
          │
          ├── Candidate Data Loader
          │
          ├── Candidate Analyzer
          │
          ├── Interview Planner
          │
          ├── Session Manager
          │
          ├── Curriculum Loader
          │
          ├── AI Interviewer
          │
          ├── Answer Evaluator
          │
          └── Feedback Generator
                    │
                    ▼
                 LLM

The system uses the provided candidate profiles and curriculum to create
personalized technical interviews.

---

# 25. Final Validation

The application was tested end-to-end after the major backend and frontend
changes.

The final test verified:

- Candidate-specific interview behavior
- Curriculum-based questions
- Multi-turn conversation
- Adaptive follow-up questions
- Answer evaluation
- Interview completion
- Structured final feedback
- Multiple candidate support
- React/FastAPI integration

The application successfully completed a full interview and generated a
final evaluation.

---

# 26. Development Summary

AI assistance was used throughout the development lifecycle for:

- Understanding the problem statement
- Architecture planning
- Backend implementation
- Candidate and curriculum integration
- Interview planning
- Adaptive interview logic
- LLM integration
- Debugging API quota issues
- React frontend development
- UI refinement
- API integration
- Error handling
- Testing
- Code cleanup

The final implementation was iteratively developed and tested rather than
being generated as a single completed codebase.