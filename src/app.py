"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from enum import Enum

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports activities
    "Basketball Team": {
        "description": "Competitive basketball training and games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Swimming Club": {
        "description": "Swimming training and water sports",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    # Artistic activities
    "Art Studio": {
        "description": "Express creativity through painting and drawing",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Theater arts and performance training",
        "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": []
    },
    # Intellectual activities
    "Debate Team": {
        "description": "Learn public speaking and argumentation skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Science Club": {
        "description": "Hands-on experiments and scientific exploration",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


class ExperienceLevel(str, Enum):
    beginner = "beginner"
    advanced = "advanced"
    professional = "professional"


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, level: ExperienceLevel):
    """Sign up a student for an activity with experience level (beginner, advanced, professional)"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in [p["email"] if isinstance(p, dict) else p for p in activity["participants"]]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Add student with level
    activity["participants"].append({"email": email, "level": level.value})
    return {"message": f"Signed up {email} for {activity_name} as {level.value}"}


@app.get("/activities")
def get_activities():
    # Return activities with participants as dicts (always include email and level)
    result = {}
    for name, activity in activities.items():
        participants = []
        for p in activity["participants"]:
            if isinstance(p, dict):
                participants.append({"email": p["email"], "level": p.get("level")})
            else:
                participants.append({"email": p, "level": None})
        result[name] = {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": participants
        }
    return result


@app.get("/students/{email}/activities")
def get_student_activities(email: str):
    return [
        {"activity": name, "level": p["level"]}
        for name, activity in activities.items()
        for p in activity["participants"]
        if isinstance(p, dict) and p["email"] == email
    ]

@app.get("/activities/participants")
def get_activities_participants():
    """Return all activities with their participants (email and level if available)"""
    result = {}
    for name, activity in activities.items():
        participants = []
        for p in activity["participants"]:
            if isinstance(p, dict):
                participants.append({"email": p["email"], "level": p.get("level")})
            else:
                participants.append({"email": p, "level": None})
        result[name] = participants
    return result


@app.get("/students/gruber.christian%40gmail.com/activities")
def get_student_activities_gruber():
    email = "gruber.christian@gmail.com"
    return [
        {"activity": name, "level": p["level"]}
        for name, activity in activities.items()
        for p in activity["participants"]
        if isinstance(p, dict) and p["email"] == email
    ]


@app.get("/activities/participants")
def get_activities_participants():
    """Return all activities with their participants (email and level if available)"""
    result = {}
    for name, activity in activities.items():
        participants = []
        for p in activity["participants"]:
            if isinstance(p, dict):
                participants.append({"email": p["email"], "level": p.get("level")})
            else:
                participants.append({"email": p, "level": None})
        result[name] = participants
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)

