"""Unit tests for the fixed skill extractor (regression: substring bug)."""

from app.resume.extractor import SkillExtractor


def test_extracts_basic_skills():
    skills = SkillExtractor().extract("I know Python, SQL and Git.")
    assert skills == ["Python", "SQL", "Git"]


def test_no_false_positive_on_letter_c():
    # Legacy bug: "c" in text matched "Recreational ... ice cream".
    assert SkillExtractor().extract("Recreational activities and ice cream") == []


def test_cpp_does_not_become_c():
    skills = SkillExtractor().extract("5 years of C++ and templates")
    assert "C++" in skills
    assert "C" not in skills


def test_c_and_cpp_coexist():
    skills = SkillExtractor().extract("C programming and C++ templates")
    assert "C" in skills and "C++" in skills


def test_aliases_resolve_to_canonical():
    skills = SkillExtractor().extract("scikit-learn and sklearn pipelines with ML models")
    assert "Scikit-Learn" in skills
    assert "Machine Learning" in skills
    assert "sklearn" not in skills


def test_case_insensitive_and_punctuation():
    skills = SkillExtractor().extract("PYTHON, (docker); node.js!")
    assert "Python" in skills
    assert "Docker" in skills
    assert "Node.js" in skills


def test_word_boundaries_for_short_terms():
    assert SkillExtractor().extract("GitHub workflows") == ["GitHub"]
    assert "Git" not in SkillExtractor().extract("GitHub workflows")


def test_empty_and_none_safe():
    assert SkillExtractor().extract("") == []
    assert SkillExtractor().extract(None) == []


def test_order_of_first_mention():
    skills = SkillExtractor().extract("SQL first, then Python, then SQL again")
    assert skills == ["SQL", "Python"]
