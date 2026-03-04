from db.database import Database
import json
import os
import re

class SearchEngine:

    @staticmethod
    def search(skills=None, experience=None, name=None):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        base_sql = """
            SELECT  
                u.id AS user_id,
                u.name,
                u.email,
                u.skills,
                u.experience,
                u.metadata,
                r.resume_url
            FROM user_details u
            JOIN resume_details r ON u.id = r.user_id
            WHERE 1=1
        """

        base_params = []

        # 🔹 Name filter
        if name:
            base_sql += " AND u.name LIKE %s"
            base_params.append(f"%{name}%")

        # 🔹 Experience filter (interval-based: 3-5 → >=3 AND <5)
        if experience:
            if "-" in experience:
                min_exp, max_exp = experience.split("-")
                base_sql += " AND u.experience >= %s AND u.experience <= %s"
                base_params.extend([float(min_exp), float(max_exp)])
            else:
                base_sql += " AND u.experience >= %s"
                base_params.append(float(experience))

        results = []
        # ==========================
        # 1️⃣ PRIMARY SEARCH → METADATA
        # ==========================
        if skills:
            metadata_conditions = []
            params = base_params.copy()

            for skill in skills.split(","):
                metadata_conditions.append(
                    "JSON_SEARCH(u.metadata, 'all', %s) IS NOT NULL"
                )
                params.append(skill.strip().lower())

            metadata_sql = base_sql + " AND (" + " OR ".join(metadata_conditions) + ")"

            cursor.execute(metadata_sql, params)
            results = cursor.fetchall()

        # ==========================
        # 2️⃣ FALLBACK → SKILLS COLUMN
        # ==========================
        if skills and not results:
            skill_list = [s.strip().lower() for s in skills.split(",")]
            skill_conditions = []
            params = base_params.copy()

            for skill in skill_list:
                skill_conditions.append("LOWER(u.skills) LIKE %s")
                params.append(f"%{skill}%")

            skills_sql = base_sql + " AND (" + " OR ".join(skill_conditions) + ")"

            cursor.execute(skills_sql, params)
            results = cursor.fetchall()
        cursor.close()
        conn.close()

        return SearchEngine._rank(results, skills)
    # ==========================
    # 🔥 RANKING FUNCTION
    # ==========================
    @staticmethod
    def _rank(candidates, query):

        if not candidates:
            return []

        # 🔹 If no skill query → return basic results
        if not query:
            for c in candidates:
                c["match_score"] = 0

                # Extract only filename for frontend
                if c.get("resume_url"):
                    c["resume_url"] = os.path.basename(c["resume_url"])

                # Remove internal fields
                c.pop("skills", None)
                c.pop("metadata", None)
                c.pop("experience", None)

            return candidates

        query_skills = {s.strip().lower() for s in query.split(",")}
        total_query = len(query_skills)

        for c in candidates:

            # Parse metadata safely
            metadata_raw = c.get("metadata", "{}")

            try:
                if isinstance(metadata_raw, str):
                    metadata = json.loads(metadata_raw)
                else:
                    metadata = metadata_raw or {}
            except Exception:
                metadata = {}

            sections = metadata.get("sections", {})
            skill_lines = sections.get("skills", [])

            candidate_skills = set()

            for line in skill_lines:
                parts = re.split(r"[,:]", line)
                for p in parts:
                    skill = p.strip().lower()
                    if skill:
                        candidate_skills.add(skill)

            # 🔥 Skill match score
            matched = len(query_skills & candidate_skills)
            skill_score = (matched / total_query) * 100 if total_query > 0 else 0

            # 🔥 Experience boost (max 20%)
            experience = float(c.get("experience") or 0)
            experience_boost = min(experience * 2, 20)

            final_score = min(skill_score + experience_boost, 100)

            c["match_score"] = round(final_score, 2)

            # 🔥 IMPORTANT → Fix resume filename
            resume_path = c.get("resume_url")
            if resume_path:
                c["resume_url"] = os.path.basename(str(resume_path))

            # Remove internal fields before sending to frontend
            c.pop("skills", None)
            c.pop("metadata", None)
            c.pop("experience", None)

        return sorted(candidates, key=lambda x: x["match_score"], reverse=True)
