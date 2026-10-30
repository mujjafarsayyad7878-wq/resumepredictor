"""
FastAPI REST API Routes
Provides endpoints for parsing uploads, running analysis,
serving role guides, and generating PDF reports.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

from app.nlp.skill_taxonomy import JOB_ROLES
from app.services.pdf_parser import parse_uploaded_file
from app.services.analyzer_service import analyzer_service
from app.services.pdf_report_generator import generate_pdf_report
from app.services.db_service import db_service

router = APIRouter(prefix="/api", tags=["Resume Predictor"])

# Pydantic Schemas
class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., description="Raw text of candidate resume")
    target_role: Optional[str] = Field("Senior Full Stack Developer", description="Standard industry role title")
    custom_jd: Optional[str] = Field(None, description="Optional custom job description text")
    language: Optional[str] = Field("auto", description="Preferred language ('auto', 'en', 'hi')")

class TextExtractResponse(BaseModel):
    filename: str
    extracted_text: str
    character_count: int
    word_count: int
    detected_language: str = "en"

@router.get("/health")
def health_check():
    """
    Health check endpoint verifying backend and ML modules.
    """
    return {
        "status": "healthy",
        "service": "Smart Resume Skill-Gap & Career Predictor",
        "version": "1.0.0"
    }

@router.get("/roles")
def get_benchmark_roles():
    """
    Returns list and details of standard pre-configured industry benchmark roles.
    Includes both English and Hindi descriptions.
    """
    return {
        "status": "success",
        "roles": [
            {
                "id": key,
                "title": val["title"],
                "title_hi": val.get("title_hi", val["title"]),
                "category": val["category"],
                "category_hi": val.get("category_hi", val["category"]),
                "min_experience_years": val["min_experience_years"],
                "primary_skills": val["primary_skills"],
                "secondary_skills": val["secondary_skills"],
                "salary_range": val["salary_range"],
                "summary": val["summary"],
                "summary_hi": val.get("summary_hi", val["summary"])
            }
            for key, val in JOB_ROLES.items()
        ]
    }

@router.post("/extract-text", response_model=TextExtractResponse)
async def extract_text_from_file(file: UploadFile = File(...)):
    """
    Extracts raw text from an uploaded file (PDF, TXT, MD, etc.).
    """
    try:
        content = await file.read()
        extracted = parse_uploaded_file(content, file.filename or "upload.txt")
        if not extracted or len(extracted.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Could not extract readable text from the uploaded file. Please ensure the file contains searchable text or paste directly."
            )
        
        words = extracted.split()
        from app.nlp.preprocessor import detect_language
        lang = detect_language(extracted)

        return TextExtractResponse(
            filename=file.filename or "uploaded_file",
            extracted_text=extracted,
            character_count=len(extracted),
            word_count=len(words),
            detected_language=lang
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@router.post("/analyze")
async def analyze_resume_endpoint(request: AnalyzeRequest):
    """
    Analyzes resume text using NLP pipelines against target role or custom JD.
    """
    try:
        result = analyzer_service.analyze_resume(
            resume_text=request.resume_text,
            target_role=request.target_role,
            custom_jd=request.custom_jd,
            language_preference=request.language
        )
        assessment_id = db_service.save_assessment(result)
        result["assessment_id"] = assessment_id
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis pipeline error: {str(e)}")

@router.post("/analyze-upload")
async def analyze_uploaded_file(
    file: UploadFile = File(...),
    target_role: Optional[str] = Form("Senior Full Stack Developer"),
    custom_jd: Optional[str] = Form(None),
    language: Optional[str] = Form("auto")
):
    """
    Direct multi-part upload endpoint: parses uploaded file and immediately returns analysis.
    """
    try:
        content = await file.read()
        extracted = parse_uploaded_file(content, file.filename or "resume.pdf")
        if not extracted or len(extracted.strip()) < 10:
            raise HTTPException(
                status_code=400, 
                detail="Unable to extract text from file. Please ensure it is not an image-only scan."
            )

        result = analyzer_service.analyze_resume(
            resume_text=extracted,
            target_role=target_role,
            custom_jd=custom_jd,
            language_preference=language
        )
        result["extracted_raw_text"] = extracted
        assessment_id = db_service.save_assessment(result)
        result["assessment_id"] = assessment_id
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload & analyze failed: {str(e)}")

@router.get("/assessment/{assessment_id}")
def get_saved_assessment(assessment_id: str):
    """
    Retrieves previously stored assessment result from database.
    """
    data = db_service.get_assessment(assessment_id)
    if not data:
        raise HTTPException(status_code=404, detail="Assessment not found or expired")
    return {"status": "success", "assessment": data}

@router.post("/export-pdf")
def export_pdf_report_endpoint(analysis_data: Dict[str, Any]):
    """
    Generates downloadable PDF assessment report based on analysis payload.
    """
    try:
        pdf_bytes = generate_pdf_report(analysis_data)
        cand_name = analysis_data.get("profile", {}).get("candidate_name", "Candidate")
        safe_filename = f"Career_Assessment_{cand_name.replace(' ', '_')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={safe_filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation error: {str(e)}")
