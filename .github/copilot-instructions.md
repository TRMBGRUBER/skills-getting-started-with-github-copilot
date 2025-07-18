# Copilot Instructions for Mergington High School Activities API

## Project Overview
- This is a FastAPI application for managing extracurricular activities at Mergington High School.
- Students can view available activities and sign up using their email.
- All data is stored in memory (no database); restarting the server resets all data.

## Key Files & Structure
- `src/app.py`: Main FastAPI app. Contains all API endpoints and in-memory data models.
- `src/static/`: Frontend assets (HTML, JS, CSS) for a simple web interface.
- `src/README.md`: API usage, endpoints, and data model documentation.

## Developer Workflows
- **Install dependencies:**
  ```bash
  pip install fastapi uvicorn
  ```
- **Run the server:**
  ```bash
  python src/app.py
  ```
- **API docs:**
  - Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
  - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Patterns & Conventions
- **Endpoints:**
  - `GET /activities`: List all activities with details and participant count.
  - `POST /activities/{activity_name}/signup?email=student@mergington.edu`: Sign up a student for an activity.
- **Identifiers:**
  - Activities: Identified by name (string).
  - Students: Identified by email (string).
- **Data Model:**
  - Activities have description, schedule, max participants, and a list of signed-up student emails.
  - Students have name and grade level.
- **No persistent storage:** All data is lost on server restart.

## Frontend Integration
- Static files in `src/static/` provide a basic web interface.
- No build step required for frontend; edit files directly.

## Patterns & Practices
- Keep all business logic and data in `app.py`.
- Use clear, descriptive variable names matching the domain (e.g., `activity_name`, `student_email`).
- Return informative error messages for invalid requests (e.g., duplicate signup, activity full).
- Follow FastAPI conventions for endpoint definitions and response models.

## Example Usage
- To sign up a student:
  ```bash
  curl -X POST "http://localhost:8000/activities/Basketball/signup?email=student@mergington.edu"
  ```

## Additional Notes
- No authentication or authorization is implemented.
- For new features, update both API and static frontend as needed.
- See `src/README.md` for more details and endpoint documentation.
