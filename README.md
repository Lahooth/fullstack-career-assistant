 Career Skill Gap & Roadmap Assistant

A full-stack project built as part of the CodeAtRandom Full Stack Intern Assignment.
This application analyzes a user’s target career role, identifies skill gaps, generates a 3-phase learning roadmap, and displays the latest tech news using the HackerNews public API.

 Features
1. Career Goal Input Page

Users can enter:

 Target Role (ex: Backend Developer)

 Current Skills (comma-separated)

Click Analyze My Career Path

2. Skill Gap Analysis API

POST /api/skill-gap
Returns:

Required skills for the role

Matched skills

Missing skills

Recommendations

Suggested learning order

3. Career Roadmap API

POST /api/roadmap
Returns a 3-phase learning roadmap (mock AI logic):

Phase 1 → Foundations

Phase 2 → Core Skills

Phase 3 → Advanced topics, Deployment & Projects

4. Public API Integration (HackerNews)

GET /api/tech-news
Shows latest 5 tech stories with:

Title

URL

Score

Time

Author

Type

5. Combined Dashboard

After submitting the form:

Left side → Skill Gap Analysis

Right side → Roadmap

Bottom → HackerNews stories

 Tech Stack
Frontend

Next.js (React Framework)

CSS (minimal custom styling)

Backend

FastAPI (Python)

Uvicorn (ASGI Server)

Requests (for HackerNews API)

Storage

JSON file (user_inputs.json) to store all input logs (bonus requirement)

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

 How to Run the Project Locally
 1. Clone the Repository
git clone <your-repo-link>
cd fullstack-career-assistant

 Backend Setup (FastAPI)
1. Move into backend folder
cd backend

2. Install backend dependencies
pip install -r requirements.txt

3. Run FastAPI server
uvicorn main:app --reload --port 8000

4. API Docs

Open in browser:

 http://127.0.0.1:8000/docs

 Frontend Setup (Next.js)
1. Move into frontend folder
cd frontend

2. Install frontend dependencies
npm install

3. Start Next.js dev server
npm run dev

4. Visit app

 http://localhost:3000/

 Deployment (Required Deliverable)
 Frontend Deployment (Vercel)

Install Vercel CLI (optional)

npm i -g vercel


Run:

vercel


Or deploy directly from Vercel dashboard.

 Backend Deployment (Render)

Create a new Web Service

Choose your backend folder

Runtime → Python

Build Command:

pip install -r requirements.txt


Start Command:

uvicorn main:app --host 0.0.0.0 --port $PORT


Deploy → Copy your Render URL
Example:

https://career-backend.onrender.com


Update frontend to use deployed backend:

Open frontend/pages/index.js:

const BACKEND_BASE_URL = "https://<your-render-url>";

 API Documentation
POST /api/skill-gap

Body Example

{
  "target_role": "Backend Developer",
  "current_skills": ["Java", "SQL", "Git"]
}

POST /api/roadmap
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

Only 3 predefined roles included:

Frontend Developer

Backend Developer

Data Analyst

Roadmaps are mock-generated (static logic, not AI-generated)

JSON file is used instead of a full database (allowed + bonus)