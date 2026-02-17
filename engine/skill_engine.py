import re
import spacy
from engine.experience_engine import ExperienceEngine
from utils.nlp_utils import extract_sentences
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")
class SkillEngine:
    COMMON_SKILL_KEYWORDS = [
        "python", "java", "c++", "c",
        "spring", "hibernate",
        "django", "flask",
        "machine learning", "deep learning",
        "sql", "mysql", "postgresql", "mongodb",
        "react", "angular", "node", "express",
        "docker", "kubernetes", "jenkins",
        "git", "linux", "windows",
        "tensorflow", "pytorch", "scikit-learn",
        "power bi", "tableau",
        "html", "css", "jquery",
        "react native", "maven", "tomcat", "heroku", "circleci",
        "javascript","jira","visual studio"
    ]

    SKILL_ALIASES = {
        "react js": "react",
        "angular js": "angular",
        "node js": "node",
        "express js": "express",
        "mongo db": "mongodb",
        "circle ci": "circleci",
        "jquery": "jquery",
        "exponent js": "exponent",
        "grunt": "grunt"
    }
    STOPWORDS = {
        "and", "the", "with", "using", "used", "for", "to", "of",
        "in", "on", "by", "from", "that", "this", "it",
        "experience", "education", "projects", "summary",
        "software", "engineer", "engineering"
    }

    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    _nlp = None
    patterns = [nlp.make_doc(skill) for skill in COMMON_SKILL_KEYWORDS]
    matcher.add("SKILLS", patterns)

    # ===============================
    # FOR user_details.skills COLUMN
    # ===============================
    @staticmethod
    def discover_skill_candidates(text: str):
        text = text.lower()

        # only look inside skill-like sections
        match = re.search(
            r"(technical skills|skills|core competencies|tech stack|tools|technologies)(.*?)(experience|education|projects|\Z)",
            text,
            re.DOTALL
        )

        if not match:
            return []

        block = match.group(2)

        candidates = set()
        for token in re.findall(r"[a-zA-Z][a-zA-Z\+\#\.]{2,}", block):
            token = SkillEngine._normalize_skill(token)
            if 3 <= len(token) <= 25:
                candidates.add(token)

        return list(candidates)

    @staticmethod
    def extract_skills_for_column(text: str) -> str:
        text = text.lower()

        for k, v in SkillEngine.SKILL_ALIASES.items():
            text = text.replace(k, v)

        found = set()

        for skill in SkillEngine.COMMON_SKILL_KEYWORDS:
            if re.search(rf"\b{re.escape(skill)}\b", text):
                found.add(skill)

        return ", ".join(sorted(found))

    # ===============================
    # FOR metadata.skills (JSON)
    # ===============================
    @staticmethod
    def extract_skills_for_metadata(text: str):
        text = text.lower()
        tokens = set()

        for word in re.findall(r"[a-zA-Z][a-zA-Z\+\#\.]{2,}", text):
            w = SkillEngine._normalize_skill(word)

            # Remove noise
            if w in SkillEngine.STOPWORDS:
                continue
            if len(w) < 3 or len(w) > 20:
                continue
            if w.isdigit():
                continue

            tokens.add(w)

        return {"all": sorted(tokens)}

    @staticmethod
    def _normalize_skill(skill: str):
        skill = skill.lower().strip()

        replacements = {
            "reactjs": "react",
            "nodejs": "node",
            "angularjs": "angular",
            "expressjs": "express",
            "circleci": "circle ci",
            "html/css": "html css"
        }

        for k, v in replacements.items():
            skill = skill.replace(k, v)

        skill = skill.replace("/", " ")
        skill = skill.replace("&", " ")
        skill = re.sub(r"[^a-z0-9\s]", "", skill)

        return skill.strip()

    @staticmethod
    def normalize_text(text: str) -> str:
        text = text.replace("\r", "\n")
        text = re.sub(r"\n{2,}", "\n", text)  # collapse multiple newlines
        text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)# fix glued words
        return text.strip()

    @staticmethod
    def normalize_broken_text(text: str) -> str:
        # 1️⃣ Fix spaced ALL-CAPS headings: E X P E R I E N C E → EXPERIENCE
        text = re.sub(
            r"\b(?:[A-Z]\s){2,}[A-Z]\b",
            lambda m: m.group(0).replace(" ", ""),
            text
        )

        # 2️⃣ Fix broken ALL-CAPS words split once: EDUCA TI O N → EDUCATION

        return text

    # ===============================
    # METADATA BUILDER
    # ===============================
    @staticmethod

    def build_metadata(full_text: str,canonical_skills: list,header_override=None):
        exp_block = SkillEngine._extract_section(full_text, "experience")
        if not exp_block:
            exp_block = ""
        summary_block = SkillEngine._extract_section(full_text, "summary")
        summary_sentences = extract_sentences(summary_block.replace("\n", " ")) if summary_block else []
        projects_block = SkillEngine._extract_section(full_text, "projects")
        if projects_block:
            projects_block = projects_block.replace("•", ".").replace("●", ".")
            project_sentences = extract_sentences(projects_block)
        else:
            project_sentences = []
        header = {
            "name": SkillEngine._extract_name_from_text(full_text),
            **SkillEngine._extract_header(full_text)
        }
        if header_override:
            header.update({k: v for k, v in header_override.items() if v})

        return {
            "header": header,
            "summary": " ".join(summary_sentences) if summary_sentences else None,
            "skills": {
                "canonical": canonical_skills,
                "soft": [],
                "tools": [],
                "languages": canonical_skills,
                "raw": list(set(SkillEngine.extract_skills_for_metadata(full_text)["all"]))
            },
            "experience": ExperienceEngine.extract_experience_structured(exp_block) if exp_block else [],
            "education": SkillEngine._extract_section(full_text, "education"),
            "projects": project_sentences if project_sentences else [],
            "certifications": SkillEngine._extract_section(full_text, "certifications")
        }

    # ===============================
    # HELPERS
    # ===============================
    @staticmethod
    def _extract_header(text: str):

        # Extract email
        email_match = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

        # Robust phone pattern (handles international + Indian + US)
        phone_match = re.findall(
            r"""
            (?:
                \+?\d{1,3}[\s\-]?        # Country code
            )?
            (?:\(?\d{3,5}\)?[\s\-]?)?    # Area code
            \d{5}[\s\-]?\d{4}            # Main number (Indian style)
            """,
            text,
            re.VERBOSE
        )

        # Clean phone numbers
        phone = None
        if phone_match:
            # Remove spaces/dashes for storage
            phone = re.sub(r"[^\d+]", "", phone_match[0])

        return {
            "email": email_match[0] if email_match else None,
            "phone": phone
        }

    @staticmethod
    def _extract_section(text: str, section_name: str):

        section_aliases = {
            "summary": ["summary", "professional summary", "profile", "about"],
            "experience": ["work experience", "experience", "employment", "career history"],
            "education": ["education", "academic background"],
            "projects": ["projects", "personal projects"],
            "certifications": ["certifications", "licenses"]
        }

        all_sections = [
            "summary", "work experience", "experience", "education",
            "projects", "certifications", "skills",
            "contact", "other", "volunteering"
        ]

        aliases = section_aliases.get(section_name, [section_name])
        text_lower = text.lower()

        # find all section headers
        header_pattern = r"\b(" + "|".join(all_sections) + r")\b"
        headers = list(re.finditer(header_pattern, text_lower))

        if not headers:
            return None

        for i, header in enumerate(headers):
            if header.group(1) in aliases:
                start = header.start()
                end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
                return text[start:end].strip()

        return None

    @staticmethod
    def _extract_name_from_text(text: str):
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        for line in lines[:5]:
            # Skip emails, separators, or lines containing numbers
            if "@" in line or "|" in line or any(c.isdigit() for c in line):
                continue

            clean = line.replace(" ", "")

            # Likely name: 2–4 words, only alphabets
            if (
                    2 <= len(line.split()) <= 4
                    and re.match(r"^[A-Za-z.\-']+$", line.replace(" ", ""))
            ):
                return line.title()

        return None






