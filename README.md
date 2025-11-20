Here is your README fully rewritten, clean, professional, and including the important clarification:

Frontend supports 25 job roles

Backend intentionally supports only 3 roles for this assignment demo

No emojis, no AI-generated feel

Everything structured clearly for CodeAtRandom reviewers

You can paste this entire block directly into your README.md.

Career Skill Gap & Roadmap Assistant

A full-stack project built as part of the CodeAtRandom Full Stack Intern Assignment.
This application analyzes a user’s target career role, identifies matching and missing skills, generates a phase-wise learning roadmap, and displays current tech news using the HackerNews public API.

Project Summary

The frontend of this project is designed to support 25 different technology job roles such as Software Engineer, Full Stack Developer, Machine Learning Engineer, Cloud Engineer, Cybersecurity Analyst, UI/UX Designer, Business Analyst, and many more.

However, the backend is intentionally limited to three roles to keep the assignment light, fast, and within the expected evaluation scope:

Frontend Developer

Backend Developer

Data Analyst

These three roles are fully implemented end-to-end with:

Required skills

Skill gap matching

Recommendations

Learning order

Career roadmap

The architecture is built so additional roles can be enabled easily by expanding the backend templates in main.py.

Features
1. Career Goal Input Page

Users can enter:

Target Role (example: Backend Developer)

Current Skills (comma-separated)

Clicking Analyze My Career Path triggers the backend API.

2. Skill Gap Analysis API

POST /api/skill-gap

Returns:

Required skills for the target role

Matched skills

Missing skills

Recommendations

Suggested learning order

3. Career Roadmap API

POST /api/roadmap

Returns a structured 3-phase learning plan:

Phase 1 – Foundations

Phase 2 – Core Skills

Phase 3 – Advanced Topics, Deployment, Projects

Roadmap logic is predefined and consistent for assignment demo purposes.

4. Public API Integration – HackerNews

GET /api/tech-news

Displays the latest technology stories, including:

Title

URL

Score

Time

Author

Type

5. Combined Dashboard

After submitting the form:

Left panel shows the Skill Gap Analysis

Right panel shows the Career Roadmap

Bottom section shows HackerNews Technology Stories

Technology Stack
Frontend

Next.js (React Framework)

CSS (custom minimal styling)

Axios

Backend

FastAPI (Python)

Uvicorn (ASGI Server)

Requests (HackerNews API)

CORS Enabled

Storage

JSON file (user_inputs.json) used to save user inputs
(as an optional bonus requirement instead of a full database)

Project Structure
fullstack-career-assistant/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── data/
│       └── user_inputs.json
│
└── frontend/
    ├── package.json
    ├── next.config.js
    ├── pages/
    │   ├── index.js
    │   └── _app.js
    └── styles/
        └── globals.css

How to Run the Project Locally (Optional)

Running locally is optional because both frontend and backend are already deployed live.

1. Clone the Repository
git clone <your-repo-link>
cd fullstack-career-assistant

Backend Setup (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000


API Docs available at:

http://127.0.0.1:8000/docs

Frontend Setup (Next.js)
cd frontend
npm install
npm run dev


Local frontend:

http://localhost:3000/

Deployment (Assignment Requirement)
Frontend Deployment – Vercel

Deployed via Vercel Dashboard:
https://fullstack-career-assistant.vercel.app

Backend Deployment – Render

Steps used:

Create Web Service

Runtime: Python

Build Command:

pip install -r requirements.txt


Start Command:

uvicorn main:app --host 0.0.0.0 --port $PORT


Live backend:
https://fullstack-career-assistant.onrender.com

The frontend is configured to use the deployed backend.

API Documentation
POST /api/skill-gap

Example Request:

{
  "target_role": "Backend Developer",
  "current_skills": ["Java", "SQL", "Git"]
}

POST /api/roadmap

Example Request:

{
  "target_role": "Backend Developer"
}

GET /api/tech-news

Returns:

id

title

score

url

time

type

by

Assumptions

Backend supports only three predefined roles:

Frontend Developer

Backend Developer

Data Analyst

Roadmaps are predefined and not AI-generated

JSON file storage is used instead of a database (acceptable for assignment)

Frontend is capable of handling 25+ roles, but backend responses are limited intentionally for the demo
