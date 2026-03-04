import os
import json
import re
from werkzeug.utils import secure_filename
from db.database import Database
from engine.skill_engine import extract_skills
from engine.experience_structurer import extract_experience_json
from engine.debug_extraction import (
    extract_lines_pymupdf,
    split_lines_into_columns,
    order_lines_reading_order,
    build_sections_from_lines,
    clean_section_content,
    merge_section_dicts,
)
import fitz
SUMMARY_EXP_RE = re.compile(r"(\d+(\.\d+)?)\s+years?\s+of\s+experience", re.I)

def extract_summary_experience(sections):
    summary_lines = sections.get("summary", [])

    for line in summary_lines:
        m = SUMMARY_EXP_RE.search(line)
        if m:
            return float(m.group(1))

    return 0
def is_valid_pdf(path):
    try:
        doc = fitz.open(path)
        doc.close()
        return True
    except Exception:
        return False
UPLOAD_FOLDER = "uploads/resumes"

def extract_name_from_header(header_lines):

    if not header_lines:
        return None

    SECTION_WORDS = {
        "summary","experience","skills","education",
        "projects","expertise","profile"
    }

    for line in header_lines[:10]:

        candidate = line.strip()
        words = candidate.split()

        if len(words) < 2 or len(words) > 4:
            continue

        # reject section titles
        if any(w.lower() in SECTION_WORDS for w in words):
            continue

        # reject lines with numbers/emails
        if re.search(r"\d|@|\+", candidate):
            continue

        # must look like a proper name
        if all(w.isalpha() for w in words):
            return candidate

    return None
class ResumeEngine:

    @staticmethod
    def upload_resume(file):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        filename = secure_filename(file.filename)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)
        # ✅ validate pdf
        if not is_valid_pdf(temp_path):
            os.remove(temp_path)
            cursor.close()
            conn.close()
            return {
                "error": "Invalid or corrupted PDF",
                "filename": filename
            }

        # ==============================
        # TEXT EXTRACTION (ADVANCED PIPELINE)
        # ==============================

        lines = extract_lines_pymupdf(temp_path)

        left_lines, right_lines = split_lines_into_columns(lines)

        left_lines = order_lines_reading_order(left_lines)
        right_lines = order_lines_reading_order(right_lines)

        left_sections = build_sections_from_lines(left_lines)
        right_sections = build_sections_from_lines(right_lines)

        sections = merge_section_dicts(left_sections, right_sections)
        sections = clean_section_content(sections)
        full_text = "\n".join(
            line["text"] for line in lines
        )

        print("SECTION KEYS:", sections.keys())
        # ==============================
        # HEADER EXTRACTION
        # ==============================
        header_lines = sections.get("header", [])
        header_text = " ".join(header_lines)

        EMAIL_RE = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        PHONE_RE = r"(?:\+?\d{1,3}[\s-]?)?\d{10}"

        email_match = re.search(EMAIL_RE, header_text) or re.search(EMAIL_RE, full_text)
        phone_match = re.search(PHONE_RE, header_text) or re.search(PHONE_RE, full_text)

        email = email_match.group(0) if email_match else None
        phone = phone_match.group(0) if phone_match else None

        # 🔥 CRITICAL FALLBACK — scan full resume
        if not email:
            email_match = re.search(EMAIL_RE, full_text)
            if email_match:
                email = email_match.group(0)

        if not phone:
            phone_match = re.search(PHONE_RE, full_text)
            if phone_match:
                phone = phone_match.group(0)

        if not email:
            cursor.close()
            conn.close()
            return {"error": "Email not found in resume."}

        # ==============================
        # CHECK DUPLICATE BY EMAIL
        # ==============================
        cursor.execute(
            "SELECT id FROM user_details WHERE email = %s",
            (email,)
        )
        existing_user = cursor.fetchone()

        # ==============================
        # EXTRACT OTHER FIELDS
        # ==============================

        name = extract_name_from_header(header_lines)
        name = name.title()
        if not name and email:
            name = email.split("@")[0]

        experience_json = extract_experience_json(sections)

        total_months = sum(
            exp.get("duration_months", 0)
            for exp in experience_json
        )

        experience = round(total_months / 12, 2)

        # fallback to summary if no job dates found
        if experience == 0:
            experience = extract_summary_experience(sections)

        skills_list = extract_skills(sections)
        skills = ", ".join(skills_list)

        metadata_dict = {
            "sections": sections,
            "experience_json": experience_json
        }
        metadata_json = json.dumps(metadata_dict, ensure_ascii=False)

        # ==============================
        # INSERT OR UPDATE
        # ==============================
        if existing_user:
            user_id = existing_user["id"]

            user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
            os.makedirs(user_folder, exist_ok=True)

            final_path = os.path.join(user_folder, filename)

            if os.path.exists(final_path):
                os.remove(final_path)

            os.replace(temp_path, final_path)

            cursor.execute("""
                           UPDATE user_details
                           SET name=%s,
                               email=%s,
                               phone_number=%s,
                               skills=%s,
                               experience=%s,
                               metadata=%s
                           WHERE id = %s
                           """, (name, email, phone, skills, experience, metadata_json, user_id))

            cursor.execute("""
                           UPDATE resume_details
                           SET resume_url=%s
                           WHERE user_id = %s
                           """, (filename, user_id))

            message = "Resume updated successfully"

        else:
            cursor.execute("""
                           INSERT INTO user_details
                               (name, email, phone_number, skills, experience, metadata)
                           VALUES (%s, %s, %s, %s, %s, %s)
                           """, (name, email, phone, skills, experience, metadata_json))

            user_id = cursor.lastrowid

            user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
            os.makedirs(user_folder, exist_ok=True)

            final_path = os.path.join(user_folder, filename)
            os.replace(temp_path, final_path)

            cursor.execute("""
                           INSERT INTO resume_details (user_id, resume_url)
                           VALUES (%s, %s)
                           """, (user_id, filename))

            message = "Resume uploaded successfully"

        conn.commit()
        cursor.close()
        conn.close()

        return {
            "message": message,
            "user_id": user_id,
            "resume_filename": filename
        }




