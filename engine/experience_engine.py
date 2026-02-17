import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ExperienceEngine:

    @staticmethod
    def extract_experience_years(text: str) -> float:
        text = text.lower()
        # Normalize all dash variations to standard dash
        text = re.sub(r"[\u2010-\u2015\u2212]", "-", text)

        # Ensure dash always has spaces around it
        text = re.sub(r"\s*-\s*", " - ", text)

        # 1️⃣ Date ranges (most reliable)
        years = ExperienceEngine._experience_from_date_ranges(text)
        if years > 0:
            return round(years, 1)

        # 2️⃣ Explicit mentions (e.g. "5 years")
        years = ExperienceEngine._experience_from_explicit(text)
        if years > 0:
            return years

        return 0.0

    # ---------------- DATE RANGE BASED ---------------- #

    @staticmethod
    def _experience_from_date_ranges(text: str) -> float:
        ranges = ExperienceEngine._extract_date_ranges(text)

        if not ranges:
            return 0.0

        total_months = 0
        for start, end in ranges:
            delta = relativedelta(end, start)
            total_months += delta.years * 12 + delta.months

        return total_months / 12

    @staticmethod
    def _extract_date_ranges(text):
        today = datetime.today()
        ranges = []

        patterns = [
            # Jan 2020 - Present
            r"\b([A-Za-z]{3,9})\s+(\d{4})\s*-\s*(present|current|now)\b",

            # Jan 2020 - Dec 2022
            r"\b([A-Za-z]{3,9})\s+(\d{4})\s*-\s*([A-Za-z]{3,9})\s+(\d{4})\b",

            # 06/2015 - Present
            r"\b(\d{1,2})/(\d{4})\s*-\s*(present|current|now)\b",

            # 06/2015 - 12/2018
            r"\b(\d{1,2})/(\d{4})\s*-\s*(\d{1,2})/(\d{4})\b",

            # 2015 - 2018
            r"\b(\d{4})\s*-\s*(\d{4})\b",

            # 2019 to 2022
            r"\b(\d{4})\s*(?:to|–|-)\s*(\d{4})\b"
        ]

        for pattern in patterns:
            for match in re.findall(pattern, text, re.I):
                start, end = ExperienceEngine._parse_match(match, today)
                if start and end:
                    ranges.append((start, end))

        return ExperienceEngine._merge_ranges(ranges)

    @staticmethod
    def _parse_match(match, today):
        try:
            # Jan 2022 - Present
            if len(match) == 3 and match[0].isalpha():
                month, year, _ = match
                month_map = {
                    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
                    "may": 5, "jun": 6, "jul": 7, "aug": 8,
                    "sep": 9, "oct": 10, "nov": 11, "dec": 12
                }
                start = datetime(int(year), month_map[month[:3].lower()], 1)
                end = today

            # May 2020 - Dec 2021
            elif len(match) == 4 and match[0].isalpha():
                sm, sy, em, ey = match
                month_map = {
                    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
                    "may": 5, "jun": 6, "jul": 7, "aug": 8,
                    "sep": 9, "oct": 10, "nov": 11, "dec": 12
                }
                start = datetime(int(sy), month_map[sm[:3].lower()], 1)
                end = datetime(int(ey), month_map[em[:3].lower()], 1)

            # 01/2015 - Present
            elif len(match) == 3 and match[0].isdigit():
                sm, sy, _ = match
                start = datetime(int(sy), int(sm), 1)
                end = today

            # 06/2010 - 12/2014
            elif len(match) == 4 and match[0].isdigit():
                sm, sy, em, ey = match
                start = datetime(int(sy), int(sm), 1)
                end = datetime(int(ey), int(em), 1)

            # 2011 - 2016
            elif len(match) == 2:
                sy, ey = match
                start = datetime(int(sy), 1, 1)
                end = datetime(int(ey), 12, 31)

            else:
                return None, None

            return start, end

        except Exception:
            return None, None

    @staticmethod
    def _merge_ranges(ranges):
        if not ranges:
            return []

        ranges.sort(key=lambda x: x[0])
        merged = [ranges[0]]

        for current in ranges[1:]:
            last = merged[-1]
            if current[0] <= last[1]:
                merged[-1] = (last[0], max(last[1], current[1]))
            else:
                merged.append(current)

        return merged

    # ---------------- EXPLICIT YEARS BASED ---------------- #

    @staticmethod
    def _experience_from_explicit(text: str) -> float:
        matches = re.findall(
            r"(\d+(\.\d+)?)\s*\+?\s*years?",
            text
        )

        if not matches:
            return 0.0

        return max(float(m[0]) for m in matches)

    @staticmethod
    def extract_experience_structured(exp_block: str):
        if not exp_block:
            return []

        jobs = re.split(r"\n{2,}", exp_block)

        experiences = []

        for job in jobs:
            date_match = re.search(
                r"(?:[A-Za-z]{3,9}\s+\d{4}|\d{4})\s*-\s*(?:Present|Current|Now|[A-Za-z]{3,9}\s+\d{4}|\d{4})",
                job,
                re.I
            )

            if not date_match:
                continue

            lines = [l.strip() for l in job.split("\n") if l.strip()]

            company = lines[0] if len(lines) > 0 else None
            role = lines[1] if len(lines) > 1 else None

            experiences.append({
                "company": company,
                "role": role,
                "date_range": date_match.group(0),
                "bullets": []
            })

        return experiences




