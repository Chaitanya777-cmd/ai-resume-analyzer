import json
import os
import shutil

from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from services.pdf_parser import extract_text_from_pdf
from services.resume_parser import parse_resume
from services.ai_analyzer import analyze_resume
from services.job_matcher import match_resume_with_job
from services.quality_analyzer import analyze_resume_quality
from services.skill_gap_analyzer import analyze_skill_gap
from services.improvement_analyzer import analyze_resume_improvements
from services.report_generator import generate_report
from database import initialize_database, get_connection
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_user_id_from_token
)

app = FastAPI()
initialize_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer Backend is Running 🚀"
    }


@app.post("/register")
async def register(request: RegisterRequest):
    connection = get_connection()
    cursor = connection.cursor()

    existing_user = cursor.execute(
        "SELECT id FROM users WHERE email = ?",
        (request.email,)
    ).fetchone()

    if existing_user:
        connection.close()
        return {
            "success": False,
            "message": "Email already registered."
        }

    hashed_password = hash_password(request.password)

    cursor.execute(
        """
        INSERT INTO users
        (name, email, password)
        VALUES (?, ?, ?)
        """,
        (
            request.name,
            request.email,
            hashed_password
        )
    )

    connection.commit()
    user_id = cursor.lastrowid
    connection.close()

    token = create_access_token(user_id)

    return {
        "success": True,
        "message": "Registration successful!",
        "token": token
    }


@app.post("/login")
async def login(request: LoginRequest):
    connection = get_connection()
    cursor = connection.cursor()

    user = cursor.execute(
        """
        SELECT id, name, email, password
        FROM users
        WHERE email = ?
        """,
        (request.email,)
    ).fetchone()

    connection.close()

    if not user:
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    if not verify_password(request.password, user["password"]):
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    token = create_access_token(user["id"])

    return {
        "success": True,
        "message": "Login successful!",
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    authorization: str = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )

    token = authorization.split(" ")[1]

    try:
        user_id = get_user_id_from_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    
    if not file.filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "message": "Only PDF files are allowed."
        }

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)
    parsed_resume = parse_resume(extracted_text)
    ai_analysis = analyze_resume(parsed_resume)
    improvement_analysis = analyze_resume_improvements(parsed_resume)
    quality_analysis = analyze_resume_quality(extracted_text, parsed_resume)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO analyses
            (
        user_id,
        filename,
        name,
        email,
        overall_score,
        ats_score,
        analysis_data
    )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (   user_id,
            file.filename,
            parsed_resume.get("name", ""),
            parsed_resume.get("email", ""),
            ai_analysis.get("overall_score", 0),
            ai_analysis.get("ats_score", 0),
            json.dumps({
                "resume": parsed_resume,
                "ai_analysis": ai_analysis,
                "quality_analysis": quality_analysis,
                "improvement_analysis": improvement_analysis
            })
        )
    )

    connection.commit()
    connection.close()

    return {
        "success": True,
        "message": "Resume uploaded and analyzed successfully! 🚀",
        "filename": file.filename,
        "text": extracted_text,
        "resume": parsed_resume,
        "ai_analysis": ai_analysis,
        "improvement_analysis": improvement_analysis,
        "quality_analysis": quality_analysis
    }


class JobMatchRequest(BaseModel):
    resume: dict
    job_description: str


@app.post("/match-job")
async def match_job(request: JobMatchRequest):
    match_result = match_resume_with_job(
        request.resume,
        request.job_description
    )

    return {
        "success": True,
        "message": "Resume matched with job successfully! 🚀",
        "match": match_result
    }


class SkillGapRequest(BaseModel):
    resume_text: str
    job_description: str


@app.post("/skill-gap")
async def skill_gap(request: SkillGapRequest):
    result = analyze_skill_gap(
        request.resume_text,
        request.job_description
    )

    return {
        "success": True,
        "message": "Skill gap analysis completed successfully! 🎯",
        "skill_gap": result
    }


@app.post("/generate-report")
async def generate_analysis_report(data: dict):
    resume = data.get("resume", {})
    ai_analysis = data.get("ai_analysis", {})
    skill_gap = data.get("skill_gap", {})
    improvement_analysis = data.get("improvement_analysis", {})

    file_path = generate_report(
        resume,
        ai_analysis,
        skill_gap,
        improvement_analysis
    )

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="AI_Resume_Analysis_Report.pdf"
    )



@app.get("/history")
async def get_history(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )

    token = authorization.split(" ", 1)[1]

    try:
        user_id = get_user_id_from_token(token)
    except Exception as e:
        print("TOKEN ERROR in /history:", repr(e))
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id, filename, name, email,
                   overall_score, ats_score, created_at
            FROM analyses
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        history = [
            {
                "id": row["id"],
                "filename": row["filename"],
                "name": row["name"],
                "email": row["email"],
                "overall_score": row["overall_score"],
                "ats_score": row["ats_score"],
                "created_at": row["created_at"]
            }
            for row in rows
        ]

        return {
            "success": True,
            "history": history
        }
    finally:
        connection.close()


@app.get("/history/{analysis_id}")
async def get_analysis(
    analysis_id: int,
    authorization: str = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )

    token = authorization.split(" ", 1)[1]

    try:
        user_id = get_user_id_from_token(token)
    except Exception as e:
        print("TOKEN ERROR in /history/{analysis_id}:", repr(e))
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT analysis_data
            FROM analyses
            WHERE id = ? AND user_id = ?
            """,
            (analysis_id, user_id)
        )

        row = cursor.fetchone()

        if not row:
            raise HTTPException(
                status_code=404,
                detail="Analysis not found for this user."
            )

        analysis_data = json.loads(row["analysis_data"])

        return {
            "success": True,
            "analysis": analysis_data
        }
    finally:
        connection.close()
