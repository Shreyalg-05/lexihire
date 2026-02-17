from db.database import Database
import json

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

        # 🔹 Experience filter
        # 🔹 Experience filter (interval-based)
        # 🔹 Experience filter (interval-based)
        if experience:
            if "-" in experience:
                min_exp, max_exp = experience.split("-")
                min_exp = float(min_exp)
                max_exp = float(max_exp)

                base_sql += " AND u.experience >= %s AND u.experience < %s"
                base_params.extend([min_exp, max_exp])
        results = []

        # ==========================
        # 1️⃣ SEARCH IN SKILLS
        # ==========================
        if skills:
            skill_list = [s.strip().lower() for s in skills.split(",")]
            skill_conditions = []
            params = base_params.copy()

            for skill in skill_list:
                skill_conditions.append("u.skills LIKE %s")
                params.append(f"%{skill}%")

            skills_sql = (
                base_sql
                + " AND (" + " OR ".join(skill_conditions) + ")"
            )

            cursor.execute(skills_sql, params)
            results = cursor.fetchall()

        # ==========================
        # 2️⃣ FALLBACK → METADATA
        # ==========================
        if skills and not results:
            metadata_conditions = []
            params = base_params.copy()

            for skill in skills.split(","):
                metadata_conditions.append(
                    "JSON_SEARCH(u.metadata, 'all', %s) IS NOT NULL"
                )
                params.append(skill.strip().lower())

            metadata_sql = (
                base_sql
                + " AND (" + " OR ".join(metadata_conditions) + ")"
            )

            cursor.execute(metadata_sql, params)
            results = cursor.fetchall()

        cursor.close()
        conn.close()

        return SearchEngine._rank(results, skills)

    # ==========================
    # 🔥 TF-IDF RANKING
    # ==========================
    @staticmethod
    def _rank(candidates, query):
        if not candidates:
            return []

        # If no skill query → return basic results
        if not query:
            for c in candidates:
                c["match_score"] = 0

                # remove internal columns
                c.pop("skills", None)
                c.pop("metadata", None)
                c.pop("experience", None)

            return candidates

        query_skills = {s.strip().lower() for s in query.split(",")}
        total_query = len(query_skills)

        for c in candidates:
            metadata_raw = c.get("metadata", "{}")

            if isinstance(metadata_raw, str):
                metadata = json.loads(metadata_raw)
            else:
                metadata = metadata_raw or {}

            skill_block = metadata.get("skills", {})

            candidate_skills = set(
                skill_block.get("canonical", []) +
                skill_block.get("languages", []) +
                skill_block.get("tools", [])
            )

            candidate_skills = {s.lower() for s in candidate_skills}

            matched = len(query_skills & candidate_skills)

            skill_score = (matched / total_query) * 100 if total_query > 0 else 0

            experience = c.get("experience", 0)
            experience_boost = min(experience * 2, 20)

            final_score = min(skill_score + experience_boost, 100)

            c["match_score"] = round(final_score, 2)

            # 🔥 Remove internal fields before sending to frontend
            c.pop("skills", None)
            c.pop("metadata", None)
            c.pop("experience", None)

        return sorted(candidates, key=lambda x: x["match_score"], reverse=True)



