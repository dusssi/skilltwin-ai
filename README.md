# 🚀 SkillTwin AI

### AI Career Growth Companion

SkillTwin AI is an AI-powered career development platform that helps students and aspiring professionals identify skill gaps, analyze resumes, generate career roadmaps, receive internship recommendations, and track career growth through an autonomous agent system.

---

## ✨ Features

### 📄 Resume Intelligence

* Upload PDF resumes
* Extract technical skills automatically
* Detect missing skills
* Calculate career readiness score
* Recommend projects
* Recommend internships

### 👤 Profile Intelligence

* Career profile dashboard
* Skills tracking
* Missing skills analysis
* Reflection score monitoring

### 🗺️ Career Roadmap Engine

* Personalized learning paths
* Goal-oriented roadmap generation
* Progress tracking
* Career milestone planning

### 💬 AI Career Coach

* Internship guidance
* Project recommendations
* Career advice
* Learning strategy suggestions

### ⚙️ Runtime Monitor

* Observe → Plan → Act → Reflect → Replan loop
* Autonomous career agent
* Reflection analysis
* Progress monitoring

---

## 🏗️ Architecture

```text
Frontend (Streamlit)
        │
        ▼
Backend (FastAPI)
        │
        ▼
Career Intelligence Layer
        │
 ┌──────┼──────┐
 ▼      ▼      ▼
Resume  Roadmap Chat
Engine  Engine  Coach
        │
        ▼
Runtime Agent
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* FastAPI
* Pydantic
* Uvicorn

### Resume Intelligence

* PyPDF
* Custom Skill Extraction Engine

### Programming Language

* Python

---

## 📸 Screenshots

### Home Dashboard

![Home](screenshots/01-home.png)

### User Profile

![Profile](screenshots/02-profile-loaded.png)

### Resume Intelligence

![Resume](screenshots/03-resume-analysis.png)

### Career Roadmap

![Roadmap](screenshots/04-roadmap-generated.png)

### AI Career Coach

![Chat](screenshots/05-chat-response.png)

### Runtime Monitor

![Runtime](screenshots/06-runtime-complete.png)

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/dusssi/skilltwin-ai.git

cd skilltwin-ai
```

### Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.api.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Frontend Setup

```bash
cd frontend

pip install -r requirements.txt

streamlit run app.py
```

Frontend:

```text
http://localhost:8501
```

---

## 🎯 Use Cases

* Students preparing for internships
* MCA/BCA/BTech students
* Career transition learners
* Entry-level software engineers
* AI/ML internship seekers

---

## 🔮 Future Scope

### Phase 2

* Authentication
* User database
* Persistent profiles

### Phase 3

* LLM-powered career coaching
* Job recommendation engine
* LinkedIn profile analysis

### Phase 4

* AI Agent ecosystem
* Tool calling
* Web search integration
* Autonomous career planning

---

## 👨‍💻 Author

**Dushyant Chauhan**

MCA (AI & ML) Student

Built as a portfolio project focused on AI-powered career development.

---

## ⭐ Project Status

SkillTwin AI v1.0 — Portfolio Ready
