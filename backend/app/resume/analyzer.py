"""Resume analysis: skills, experience, projects, education, signals.

Deterministic and transparent: every output derives from regex/section
parsing of the actual resume text plus the target-role rubric for gaps.
"""

import re

from app.resume.extractor import SkillExtractor
from app.resume.models import ResumeAnalysis, ResumeExperience, ResumeProject
from app.twin.role_profiles import get_role_profile, match_role

_DEGREE_PATTERNS = [
    r"\b(ph\.?d|doctorate)\b",
    r"\b(m\.?tech|mtech|m\.?e|mca|m\.?sc|msc|mba|master'?s?)\b",
    r"\b(b\.?tech|btech|b\.?e|bca|b\.?sc|bsc|bachelor'?s?)\b",
    r"\b(diploma|12th|10th|higher secondary|senior secondary)\b",
]

_ROLE_KEYWORDS = [
    "intern", "developer", "engineer", "analyst", "scientist",
    "designer", "consultant", "associate", "trainee", "freelancer",
]

_SENIORITY = [
    ("senior", ["senior", "sr.", "lead", "principal", "manager"]),
    ("mid", ["software engineer", "developer", "analyst", "engineer"]),
    ("entry", ["intern", "trainee", "fresher", "junior", "associate"]),
]

_SECTION_HEADS = {
    "experience": ["experience", "work experience", "employment", "work history"],
    "projects": ["projects", "personal projects", "academic projects"],
    "education": ["education", "educational", "qualification", "academics"],
    "skills": ["skills", "technical skills", "tech stack"],
}


class ResumeAnalyzer:
    def __init__(self):
        self.extractor = SkillExtractor()

    def analyze(self, resume_text: str, target_role: str = "") -> ResumeAnalysis:
        text = resume_text or ""
        skills = self.extractor.extract(text)
        experience = self._extract_experience(text)
        projects = self._extract_projects(text)
        education = self._extract_education(text)

        role_key = match_role(target_role)
        rubric = get_role_profile(role_key)["skills"]
        missing = [name for name in rubric if name not in skills]

        signals = self._career_signals(text, skills, experience, projects, education)
        readiness = self._readiness(skills, rubric, experience, projects)
        return ResumeAnalysis(
            extracted_skills=skills,
            missing_skills=missing,
            experience=experience,
            projects=projects,
            education=education,
            career_signals=signals,
            readiness_score=readiness,
        )

    # ------------------------------------------------------------- parts
    def _extract_experience(self, text: str) -> ResumeExperience:
        lowered = text.lower()
        years = 0.0
        for match in re.finditer(r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*years?", lowered):
            try:
                years = max(years, float(match.group(1)))
            except ValueError:
                continue
        if years == 0 and re.search(r"\bfresher\b|\bentry[- ]level\b", lowered):
            years = 0.0
        roles = sorted({kw.title() for kw in _ROLE_KEYWORDS if re.search(rf"\b{kw}\b", lowered)})
        seniority = "unknown"
        for level, keywords in _SENIORITY:
            if any(kw in lowered for kw in keywords):
                seniority = level
                break
        if "intern" in lowered and seniority == "unknown":
            seniority = "entry"
        return ResumeExperience(years=round(min(years, 40.0), 1), roles=roles, seniority=seniority)

    def _split_sections(self, text: str) -> dict:
        lines = [line.strip() for line in text.splitlines()]
        heads: list = []  # (index, section)
        for index, line in enumerate(lines):
            normalized = re.sub(r"[^a-z ]", "", line.lower()).strip()
            for section, keywords in _SECTION_HEADS.items():
                if normalized in keywords or any(
                    normalized == kw or normalized.startswith(kw + " ") for kw in keywords
                ):
                    heads.append((index, section))
                    break
        heads.sort()
        sections: dict = {}
        for pos, (index, section) in enumerate(heads):
            end = heads[pos + 1][0] if pos + 1 < len(heads) else len(lines)
            sections[section] = "\n".join(lines[index + 1:end]).strip()
        return sections

    def _extract_projects(self, text: str) -> list[ResumeProject]:
        sections = self._split_sections(text)
        block = sections.get("projects", "")
        if not block:
            # Fallback: bullet lines mentioning build/developed/project.
            candidates = [
                line.strip("•-* \t")
                for line in text.splitlines()
                if re.search(r"\b(built|developed|designed|created|project)\b", line, re.I)
            ]
            block = "\n".join(candidates[:8])
        projects: list[ResumeProject] = []
        for raw in [line.strip("•-* \t") for line in block.splitlines() if line.strip()]:
            if len(raw) < 8:
                continue
            title = raw.split("|")[0].split("–")[0].split("-")[0].strip()[:120] or raw[:60]
            skills = self.extractor.extract(raw)
            projects.append(ResumeProject(title=title, detail=raw[:500], skills=skills))
            if len(projects) >= 10:
                break
        return projects

    def _extract_education(self, text: str) -> list[str]:
        sections = self._split_sections(text)
        block = sections.get("education", text)
        found: list[str] = []
        for line in [ln.strip() for ln in block.splitlines() if ln.strip()]:
            if any(re.search(pattern, line, re.I) for pattern in _DEGREE_PATTERNS):
                cleaned = re.sub(r"\s+", " ", line).strip()[:200]
                if cleaned not in found:
                    found.append(cleaned)
            if len(found) >= 6:
                break
        return found

    def _career_signals(
        self, text: str, skills: list, experience: ResumeExperience,
        projects: list, education: list,
    ) -> list[str]:
        lowered = text.lower()
        signals: list[str] = []
        if experience.years >= 2:
            signals.append(f"{experience.years} years of experience")
        elif "intern" in lowered:
            signals.append("Internship experience present")
        if len(projects) >= 3:
            signals.append(f"{len(projects)} projects listed")
        elif projects:
            signals.append(f"{len(projects)} project(s) listed")
        if "github.com" in lowered or "github" in lowered:
            signals.append("GitHub presence indicated")
        if "linkedin.com" in lowered:
            signals.append("LinkedIn presence indicated")
        if education:
            signals.append(f"Education: {education[0][:80]}")
        if len(skills) >= 8:
            signals.append(f"Broad skill coverage ({len(skills)} skills)")
        if not signals:
            signals.append("Limited career signals detected")
        return signals

    def _readiness(self, skills: list, rubric: dict, experience: ResumeExperience, projects: list) -> int:
        required = list(rubric.keys()) or ["Python"]
        coverage = sum(1 for name in required if name in skills) / max(1, len(required))
        depth = min(1.0, len(skills) / 12)
        project_share = min(1.0, len(projects) / 3)
        exp_share = min(1.0, experience.years / 2) if experience.years else 0.2
        score = 0.45 * coverage + 0.2 * depth + 0.2 * project_share + 0.15 * exp_share
        return int(round(score * 100))
