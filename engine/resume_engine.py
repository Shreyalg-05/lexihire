import os
import json
import re
from werkzeug.utils import secure_filename

from db.database import Database
from utils.pdf_utils import extract_full_text
from engine.skill_engine import SkillEngine
from engine.experience_engine import ExperienceEngine

UPLOAD_FOLDER = "uploads/resumes"


class ResumeEngine:

    @staticmethod
    def upload_resume(file):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        filename = secure_filename(file.filename)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)

        # ==============================
        # TEXT EXTRACTION
        # ==============================
        raw_text = extract_full_text(temp_path)
        raw_text = (
            raw_text.replace("\u2010", "-")
            .replace("\u2011", "-")
            .replace("\u2013", "-")
        )

        raw_text = re.sub(r"_+", "\n", raw_text)
        raw_text = re.sub(r"([a-z])([A-Z])", r"\1 \2", raw_text)
        raw_text = re.sub(r"\n{2,}", "\n\n", raw_text)

        full_text = SkillEngine.normalize_text(
            SkillEngine.normalize_broken_text(raw_text)
        )

        # ==============================
        # HEADER EXTRACTION
        # ==============================
        header = SkillEngine._extract_header(full_text)
        email = header.get("email")

        phone_match = header.get("phone")
        phone = None
        if phone_match:
            phone = "".join(phone_match)  # flatten tuple

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
        name = SkillEngine._extract_name_from_text(full_text)

        exp_block = SkillEngine._extract_section(full_text, "experience") or ""
        experience = ExperienceEngine.extract_experience_years(exp_block)

        if experience == 0:
            experience = ExperienceEngine._experience_from_explicit(full_text)

        skills = SkillEngine.extract_skills_for_column(full_text)
        skills_list = skills.split(", ") if skills else []

        metadata_dict = SkillEngine.build_metadata(
            full_text,
            skills_list,
            header_override={"name": name}
        )
        metadata_json = json.dumps(metadata_dict)

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




