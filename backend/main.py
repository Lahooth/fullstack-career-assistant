from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import requests

app = FastAPI()

# -------------------------------------------------
# CORS – allow Vercel + local dev (and others)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # keep it simple for assignment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Data Models
# -------------------------------------------------
class SkillGapRequest(BaseModel):
    target_role: str
    current_skills: List[str]


class RoadmapRequest(BaseModel):
    target_role: str


# -------------------------------------------------
# Static career data used for analysis
# -------------------------------------------------
CAREER_ROLES: Dict[str, Dict[str, Any]] = {
    "Backend Developer": {
        "required_skills": ["Java", "Spring Boot", "SQL", "APIs", "Git"],
        "recommendations": [
            "Learn Spring Boot next to move closer to a Backend Developer role.",
            "Practice designing and calling REST APIs.",
        ],
        "learning_order": ["Spring Boot", "APIs"],
        "roadmap": [
            {
                "phase": "Phase 1 (1–2 months)",
                "focus": "Foundations",
                "items": ["Java basics", "OOP concepts", "Git fundamentals"],
            },
            {
                "phase": "Phase 2 (2 months)",
                "focus": "Backend Core",
                "items": ["Spring Boot", "SQL & Joins", "REST APIs"],
            },
            {
                "phase": "Phase 3 (1–2 months)",
                "focus": "Production Readiness",
                "items": [
                    "Deployment basics",
                    "Personal projects",
                    "System design basics",
                ],
            },
        ],
    },
    "Frontend Developer": {
        "required_skills": ["HTML", "CSS", "JavaScript", "React", "Git"],
        "recommendations": [
            "Strengthen JavaScript fundamentals before diving deep into React.",
            "Build 2–3 small React projects and host them online.",
        ],
        "learning_order": ["HTML & CSS", "JavaScript", "React"],
        "roadmap": [
            {
                "phase": "Phase 1 (1–2 months)",
                "focus": "Web Basics",
                "items": ["HTML semantics", "Modern CSS", "Responsive layouts"],
            },
            {
                "phase": "Phase 2 (2 months)",
                "focus": "Frontend Core",
                "items": ["JavaScript ES6+", "React basics", "Git & GitHub"],
            },
            {
                "phase": "Phase 3 (1–2 months)",
                "focus": "Advanced UI",
                "items": ["React hooks", "State management", "Frontend deployment"],
            },
        ],
    },
    "Data Analyst": {
        "required_skills": ["Excel", "SQL", "Python", "Dashboards", "Statistics"],
        "recommendations": [
            "Practice writing complex SQL queries and joins.",
            "Build a small dashboard using Excel or a BI tool.",
        ],
        "learning_order": ["Excel", "SQL", "Python", "Dashboards"],
        "roadmap": [
            {
                "phase": "Phase 1 (1–2 months)",
                "focus": "Tools",
                "items": ["Excel basics", "Data cleaning", "Simple charts"],
            },
            {
                "phase": "Phase 2 (2 months)",
                "focus": "Analysis",
                "items": ["SQL queries", "Joins & aggregation", "Python for data"],
            },
            {
                "phase": "Phase 3 (1–2 months)",
                "focus": "Reporting",
                "items": ["Dashboards", "Storytelling with data", "Case studies"],
            },
        ],
    },
}


# -------------------------------------------------
# /api/skill-gap – main analysis endpoint
# -------------------------------------------------
@app.post("/api/skill-gap")
def analyze_skill_gap(payload: SkillGapRequest):
    target = payload.target_role.strip()
    skills = [s.strip() for s in payload.current_skills]

    role_info = CAREER_ROLES.get(target)
    if not role_info:
        return JSONResponse(
            status_code=400,
            content={"detail": f"Unsupported role: {target}"},
        )

    required = role_info["required_skills"]
    matched = [s for s in skills if s in required]
    missing = [s for s in required if s not in matched]

    return {
        "target_role": target,
        "required_skills": required,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": role_info["recommendations"],
        "suggested_learning_order": role_info["learning_order"],
    }


# -------------------------------------------------
# /api/roadmap – returns phased roadmap
# -------------------------------------------------
@app.post("/api/roadmap")
def get_roadmap(payload: RoadmapRequest):
    target = payload.target_role.strip()
    role_info = CAREER_ROLES.get(target)

    if not role_info:
        return JSONResponse(
            status_code=400,
            content={"detail": f"Unsupported role: {target}"},
        )

    return {
        "target_role": target,
        "phases": role_info["roadmap"],
    }


# -------------------------------------------------
# /api/tech-news – HackerNews stories
# -------------------------------------------------
@app.get("/api/tech-news")
def get_tech_news():
    url = "https://hn.algolia.com/api/v1/search?query=programming&tags=story"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except Exception:
        # Fail silently but keep API shape
        return {"stories": []}

    data = resp.json()
    stories = []
    for hit in data.get("hits", [])[:10]:
        stories.append(
            {
                "id": hit.get("objectID"),
                "title": hit.get("title"),
                "url": hit.get("url"),
                "score": hit.get("points"),
                "by": hit.get("author"),
                "type": "story",
                "time": hit.get("created_at"),
            }
        )
    return {"stories": stories}


# -------------------------------------------------
# Health check root
# -------------------------------------------------
@app.get("/")
def root():
    return {"message": "Career assistant backend is running"}
