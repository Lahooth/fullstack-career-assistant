from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import requests

app = FastAPI()

# -------------------------------------
# ✅ CORS SETTINGS (VERY IMPORTANT)
# -------------------------------------
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://fullstack-career-assistant.vercel.app",  # Vercel frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------
# Models
# -------------------------------------
class CareerRequest(BaseModel):
    target_role: str
    current_skills: str

# -------------------------------------
# Helper Functions
# -------------------------------------
def load_json_file(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "r") as f:
        return json.load(f)

career_data = load_json_file("career_data.json")


# -------------------------------------
# API ROUTE: Analyze skills
# -------------------------------------
@app.post("/analyze")
def analyze_career(request: CareerRequest):
    target = request.target_role.strip()
    skills = [s.strip() for s in request.current_skills.split(",")]

    if target not in career_data:
        return {"error": "Role not found"}

    required_skills = career_data[target]["required_skills"]
    roadmap = career_data[target]["roadmap"]

    matched = [s for s in skills if s in required_skills]
    missing = [s for s in required_skills if s not in matched]

    return {
        "target_role": target,
        "required_skills": required_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": career_data[target]["recommendations"],
        "learning_order": career_data[target]["learning_order"],
        "roadmap": roadmap
    }


# -------------------------------------
# API ROUTE: Fetch Tech News
# -------------------------------------
@app.get("/news")
def get_tech_news():
    url = "https://hn.algolia.com/api/v1/search?query=technology&tags=story"
    res = requests.get(url)

    if res.status_code != 200:
        return {"error": "Failed to fetch news"}

    data = res.json()
    return {"news": data.get("hits", [])}


# -------------------------------------
# Root Route
# -------------------------------------
@app.get("/")
def root():
    return {"message": "Backend Running Successfully"}
