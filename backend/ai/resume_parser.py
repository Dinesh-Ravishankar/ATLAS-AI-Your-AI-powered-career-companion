"""
Resume Parser
Extracts structured data from uploaded PDF/DOCX resumes using NLP + GPT
"""

import io
from typing import Dict, Optional
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from openai import OpenAI
from config import get_settings
import json
import re

settings = get_settings()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text content from a PDF file"""
    reader = PdfReader(io.BytesIO(file_bytes))
    text_parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_parts.append(text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text content from a DOCX file"""
    doc = DocxDocument(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extract text from either PDF or DOCX"""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif lower.endswith(".docx") or lower.endswith(".doc"):
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {filename}. Please upload PDF or DOCX.")


def parse_resume_with_ai(text: str) -> Dict:
    """Use GPT to extract structured data from resume text"""
    if not settings.openai_api_key:
        return _fallback_parse(text)

    client = OpenAI(api_key=settings.openai_api_key)

    prompt = f"""Extract structured information from this resume text. Return ONLY valid JSON with these fields:

{{
  "full_name": "string or null",
  "email": "string or null",
  "phone": "string or null",
  "location": "string or null",
  "linkedin_url": "string or null",
  "github_url": "string or null",
  "bio": "1-2 sentence professional summary or null",
  "skills": ["list of skills mentioned"],
  "education": [
    {{"institution": "string", "degree": "string", "field": "string", "year": "number or null"}}
  ],
  "experience": [
    {{"company": "string", "role": "string", "description": "string", "duration": "string"}}
  ],
  "projects": [
    {{"title": "string", "description": "string", "technologies": ["list"]}}
  ]
}}

Resume text:
{text[:4000]}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a resume parser. Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        content = response.choices[0].message.content
        # Extract JSON from possible markdown code blocks
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(content)
    except Exception as e:
        print(f"AI resume parsing failed: {e}")
        return _fallback_parse(text)


def _fallback_parse(text: str) -> Dict:
    """Basic regex-based fallback parsing when AI is unavailable"""
    email_match = re.search(r'[\w.-]+@[\w.-]+\.\w+', text)
    phone_match = re.search(r'[\+]?[\d\s\-\(\)]{10,15}', text)
    linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text)
    github_match = re.search(r'github\.com/[\w-]+', text)

    # Simple skill extraction by keyword matching
    common_skills = [
        "Python", "JavaScript", "TypeScript", "React", "Node.js", "SQL", "Java",
        "C++", "Docker", "Kubernetes", "AWS", "Git", "HTML", "CSS", "Machine Learning",
        "Data Analysis", "TensorFlow", "PyTorch", "MongoDB", "PostgreSQL", "REST API",
        "Agile", "Scrum", "Figma", "Adobe", "Communication", "Leadership", "Teamwork"
    ]
    found_skills = [s for s in common_skills if s.lower() in text.lower()]

    return {
        "full_name": None,
        "email": email_match.group() if email_match else None,
        "phone": phone_match.group().strip() if phone_match else None,
        "location": None,
        "linkedin_url": f"https://{linkedin_match.group()}" if linkedin_match else None,
        "github_url": f"https://{github_match.group()}" if github_match else None,
        "bio": None,
        "skills": found_skills,
        "education": [],
        "experience": [],
        "projects": [],
    }
