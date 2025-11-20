from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from pathlib import Path
import json
import requests
import datetime

app = FastAPI(
    title="Career Skill Gap & Roadmap API",
    description="Backend for CodeAtRandom Full Stack Assignment",
    version="1.0.0",
)

# ---------- CORS (allow frontend on localhost:3000) ----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Data & Storage ----------

ROLE_SKILLS = {
    "frontend developer": ["HTML", "CSS", "JavaScript", "React", "Git"],
    "backend developer": ["Java", "Spring Boot", "SQL", "APIs", "Git"],
    "data analyst": ["Excel", "SQL", "Python", "Dashboards", "Statistics"],
}

ROADMAPS = {
    "backend developer": [
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
            "items": ["Deployment basics", "Personal projects", "System design basics"],
        },
    ],
    "frontend developer": [
        {
            "phase": "Phase 1 (1–2 months)",
            "focus": "HTML/CSS/JS",
            "items": ["Semantic HTML", "CSS layouts", "Core JavaScript"],
        },
        {
            "phase": "Phase 2 (2 months)",
            "focus": "React",
            "items": ["React basics", "State & props", "Routing", "API calls"],
        },
        {
            "phase": "Phase 3 (1–2 months)",
            "focus": "Advanced & Projects",
            "items": ["Performance basics", "Deployment (Vercel)", "Portfolio projects"],
        },
    ],
    "data analyst": [
        {
            "phase": "Phase 1 (1–2 months)",
            "focus": "Tools",
            "items": ["Excel basics", "SQL fundamentals"],
        },
        {
            "phase": "Phase 2 (2 months)",
            "focus": "Programming & Dashboards",
            "items": ["Python for analysis", "Pandas basics", "Dashboard tools"],
        },
        {
            "phase": "Phase 3 (1–2 months)",
            "focus": "Projects & Storytelling",
            "items": ["Case studies", "End-to-end reports", "Portfolio projects"],
        },
    ],
}

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
USER_INPUTS_FILE = DATA_DIR / "user_inputs.json"

if not USER_INPUTS_FILE.exists():
    USER_INPUTS_FILE.write_text("[]", encoding="utf-8")


def save_user_input(entry: Dict[str, Any]) -> None:
    """Append user input to JSON file (bonus requirement)."""
    try:
        existing = json.loads(USER_INPUTS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        existing = []
    existing.append(entry)
    USER_INPUTS_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")


# ---------- Pydantic Models ----------

class SkillGapRequest(BaseModel):
    target_role: str
    current_skills: List[str]


class SkillGapResponse(BaseModel):
    target_role: str
    required_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]
    suggested_learning_order: List[str]


class RoadmapRequest(BaseModel):
    target_role: str


class RoadmapPhase(BaseModel):
    phase: str
    focus: str
    items: List[str]


class RoadmapResponse(BaseModel):
    target_role: str
    phases: List[RoadmapPhase]


# ---------- Helper Functions ----------

def normalize(s: str) -> str:
    return s.strip().lower()


# ---------- Skill Gap API ----------

@app.post("/api/skill-gap", response_model=SkillGapResponse)
def skill_gap_analyzer(payload: SkillGapRequest):
    target_key = normalize(payload.target_role)
    if target_key not in ROLE_SKILLS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unknown target role '{payload.target_role}'. "
                f"Supported roles: {', '.join(ROLE_SKILLS.keys())}"
            ),
        )

    required_skills = ROLE_SKILLS[target_key]

    current_normalized = [normalize(s) for s in payload.current_skills]
    matched = [
        skill for skill in required_skills
        if normalize(skill) in current_normalized
    ]
    missing = [skill for skill in required_skills if skill not in matched]

    recommendations = [
        f"Learn {skill} next to move closer to a {payload.target_role} role."
        for skill in missing
    ]

    suggested_learning_order = missing.copy()

    # Save to JSON file (bonus)
    save_user_input({
        "type": "skill-gap",
        "target_role": payload.target_role,
        "current_skills": payload.current_skills,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    })

    return SkillGapResponse(
        target_role=payload.target_role,
        required_skills=required_skills,
        matched_skills=matched,
        missing_skills=missing,
        recommendations=recommendations,
        suggested_learning_order=suggested_learning_order,
    )


# ---------- Roadmap API ----------

@app.post("/api/roadmap", response_model=RoadmapResponse)
def career_roadmap(payload: RoadmapRequest):
    target_key = normalize(payload.target_role)

    if target_key in ROADMAPS:
        phases_data = ROADMAPS[target_key]
    else:
        # Generic roadmap if role is not predefined
        phases_data = [
            {
                "phase": "Phase 1 (1–2 months)",
                "focus": "Foundations",
                "items": ["Programming basics", "Git", "Problem-solving"],
            },
            {
                "phase": "Phase 2 (2 months)",
                "focus": "Core Skills",
                "items": [f"Core skills for {payload.target_role}", "Projects"],
            },
            {
                "phase": "Phase 3 (1–2 months)",
                "focus": "Portfolio & Interviews",
                "items": ["Portfolio building", "Mock interviews", "Job applications"],
            },
        ]

    phases = [RoadmapPhase(**p) for p in phases_data]

    # Save to JSON file (bonus)
    save_user_input({
        "type": "roadmap",
        "target_role": payload.target_role,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    })

    return RoadmapResponse(target_role=payload.target_role, phases=phases)


# ---------- HackerNews Tech News API ----------

HACKER_NEWS_TOPSTORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HACKER_NEWS_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"


@app.get("/api/tech-news")
def get_tech_news(limit: int = 5):
    try:
        ids_resp = requests.get(HACKER_NEWS_TOPSTORIES_URL, timeout=5)
        ids_resp.raise_for_status()
        top_ids = ids_resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch top stories: {e}")

    stories = []
    for story_id in top_ids[:30]:  # Try first 30 IDs, keep valid stories only
        try:
            item_resp = requests.get(
                HACKER_NEWS_ITEM_URL.format(id=story_id),
                timeout=5
            )
            item_resp.raise_for_status()
            data = item_resp.json()
            if not data or data.get("type") != "story":
                continue

            ts = data.get("time")
            if ts:
                dt = datetime.datetime.utcfromtimestamp(ts)
                human_time = dt.strftime("%Y-%m-%d %H:%M UTC")
            else:
                human_time = None

            stories.append({
                "id": data.get("id"),
                "title": data.get("title"),
                "url": data.get("url"),
                "score": data.get("score"),
                "time": human_time,
                "type": data.get("type"),
                "by": data.get("by"),
            })
            if len(stories) >= limit:
                break
        except Exception:
            continue

    return {"count": len(stories), "stories": stories}
