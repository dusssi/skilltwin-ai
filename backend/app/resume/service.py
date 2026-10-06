"""Resume → Twin pipeline.

Every analysis is persisted (resume + analysis rows), merged into the
user's Skill Twin as evidence, and recorded as progress events. Nothing
is discarded.
"""

from app.db import content as content_repo
from app.db import memory as memory_repo
from app.db import twin as twin_repo
from app.resume.analyzer import ResumeAnalyzer
from app.resume.parser import ResumeParser
from app.twin import service as twin_service


class ResumeService:
    def __init__(self):
        self.parser = ResumeParser()
        self.analyzer = ResumeAnalyzer()

    def analyze_text(
        self,
        user_id: str,
        resume_text: str,
        filename_original: str = "pasted-resume.txt",
        filename_stored: str = "",
    ) -> dict:
        profile = twin_repo.get_profile(user_id) or {}
        analysis = self.analyzer.analyze(resume_text or "", profile.get("target_role", ""))

        resume = content_repo.create_resume(
            user_id=user_id,
            filename_stored=filename_stored or "text-input",
            filename_original=filename_original,
            content_text=(resume_text or "")[:60000],
        )
        record = content_repo.save_resume_analysis(
            resume_id=resume["id"],
            user_id=user_id,
            extracted_skills=analysis.extracted_skills,
            missing_skills=analysis.missing_skills,
            experience=analysis.experience.model_dump(),
            projects=[project.model_dump() for project in analysis.projects],
            education=analysis.education,
            career_signals=analysis.career_signals,
            readiness_score=analysis.readiness_score,
        )

        twin_diff = self._merge_into_twin(user_id, analysis, resume["id"])
        memory_repo.record_event(
            user_id,
            "resume_uploaded",
            ref_type="resume",
            ref_id=str(resume["id"]),
            data={
                "filename": filename_original,
                "skills_found": len(analysis.extracted_skills),
                "readiness": analysis.readiness_score,
            },
        )
        return {"resume": resume, "analysis": record, "twin_diff": twin_diff}

    def analyze_pdf(self, user_id: str, file_path: str, filename_original: str,
                    filename_stored: str) -> dict:
        text = self.parser.parse_pdf(file_path)
        return self.analyze_text(
            user_id=user_id,
            resume_text=text,
            filename_original=filename_original,
            filename_stored=filename_stored,
        )

    def _merge_into_twin(self, user_id: str, analysis, resume_id: int) -> dict:
        added: list = []
        leveled: list = []
        for skill_name in analysis.extracted_skills:
            change = twin_service.add_skill_evidence(
                user_id=user_id,
                skill_name=skill_name,
                source="resume",
                note=f"Detected in resume #{resume_id}",
            )
            if change["old_level"] == 0:
                added.append({"skill": skill_name, "level": change["new_level"]})
            elif change["leveled_up"]:
                leveled.append(change)
        for project in analysis.projects[:10]:
            twin_repo.create_project(
                user_id=user_id,
                title=project.title,
                description=project.detail,
                skills=project.skills,
                status="completed",
            )
        if analysis.experience.years:
            profile = twin_repo.get_profile(user_id) or {}
            if float(profile.get("experience_years", 0) or 0) == 0:
                twin_repo.update_profile(user_id, {"experience_years": analysis.experience.years})
        if analysis.education:
            profile = twin_repo.get_profile(user_id) or {}
            if not profile.get("education"):
                twin_repo.update_profile(user_id, {"education": "; ".join(analysis.education[:3])})
        gaps, _ = twin_service.get_gaps(user_id, persist=True)
        return {
            "skills_added": added,
            "skills_leveled": leveled,
            "projects_imported": min(len(analysis.projects), 10),
            "open_gaps": len(gaps),
        }
