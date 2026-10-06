# 🧠 SkillTwin AI

### An evolving AI career twin — not a chatbot with career tips

SkillTwin AI maintains a **persistent, evolving representation of your career
state** — skills with proficiency levels and evidence, career goals, target
role, skill gaps, roadmap progress, projects, memory — and reasons **from
that representation** when it chats, recommends, plans roadmaps, or runs its
autonomous maintenance agent.

> The system learns about the user over time, maintains a persistent
> representation of their career state, reasons from that representation, and
> updates it as the user progresses.

---

## ✨ Features (all implemented and tested)

- **Accounts & auth** — register/login, salted password hashing, expiring
  bearer tokens, strict per-user data isolation.
- **Skill Twin** — skills with 1–5 proficiency, confidence, timestamped
  evidence (resume/chat/roadmap/project/manual), full level history,
  career goals, projects, experience, education.
- **Resume → Twin pipeline** — PDF upload (validated, size-capped,
  traversal-safe) or pasted text → accurate skill extraction (word
  boundaries, longest-match-first, aliases) → experience/projects/education
  parsing → Twin merge + readiness score. Nothing is discarded.
- **Skill gaps** — computed from target-role rubrics (current vs target,
  priority, reason, recommended action), snapshotted per user.
- **Personalized roadmap** — generated from *your* gaps with difficulty,
  effort, priority, dependencies, resources; completion feeds evidence back
  into the Twin and updates proficiency.
- **Twin-aware chat** — every reply is grounded in your Twin + gaps +
  long-term memory + past context + threshold-gated knowledge; durable
  facts from conversation (goals, skills, achievements, preferences) are
  extracted and evolve the Twin. Two users get different answers.
- **Memory** — short-term (persistent sessions/messages with summaries) and
  long-term (facts, goals, preferences, achievements) plus a typed progress
  event log. Survives restarts and influences future responses.
- **Agent runtime** — one canonical orchestrator:
  `observe → plan → act → reflect → finish`, running gap analysis, roadmap
  maintenance, recommendations and research, with a transparent reflection
  score.
- **Recommendations** — projects, internships and next actions ranked by
  real Twin fit (accept/dismiss tracked).
- **RAG knowledge** — TF-IDF retrieval with a similarity threshold; returns
  "no relevant knowledge" instead of a random topic.
- **LLM layer** — Gemini via HTTPS with retries/timeouts; structured JSON
  outputs validated against Pydantic schemas; safe user-facing errors. With
  no API key, the app uses an explicitly labeled, Twin-derived local
  composer — never fake "AI" output.
- **Security** — UUID upload names, PDF magic-byte + extension + size
  validation, validated usernames/IDs (no path traversal), CORS, rate
  limiting, consistent error envelopes, no raw exceptions to users.
- **Streamlit frontend** — auth sidebar, live Twin dashboard, proficiency
  visualization, gaps, resume, roadmap with completion buttons, persistent
  chat, runtime monitor, memory/event views. Zero fake metrics; loading,
  error, empty and backend-down states throughout.

---

## 🏗️ Architecture

```text
Streamlit frontend (frontend/)
        │  Bearer-token REST
        ▼
FastAPI backend (backend/app/)
        │
        ├── api/            routes: auth, twin, resume, chat, roadmap,
        │                   runtime, memory, recommendations, knowledge, health
        ├── agents/         ONE orchestrator + typed specialists
        │                   (skill, roadmap, resume, recommendation,
        │                    research, reflection)
        ├── twin/           Skill Twin service: merge, gaps, role rubrics, catalog
        ├── resume/         parser → extractor → analyzer → Twin merge
        ├── chat/           Twin+memory+knowledge context → LLM → learn facts
        ├── roadmap/        gap-driven generation + completion → evidence
        ├── memory/         long-term memories + progress events
        ├── sessions/       persistent chat sessions + summaries
        ├── knowledge/      seed KB + threshold TF-IDF retrieval
        ├── llm/            Gemini REST provider, prompts, validated parsing
        ├── planner/        typed plans from live Twin state
        ├── recommendations catalog + gap-fit ranking
        ├── auth/           pbkdf2 hashing, opaque tokens, dependencies
        ├── db/             SQLite repositories (swappable persistence layer)
        └── config/         environment-driven settings
```

Data flow:

```text
User → Profile → Resume → Skills+Proficiency → Goal → Gaps → Memory
  → AI reasoning → Recommendations → Roadmap → Progress → Twin update → …
```

---

## 🛠️ Tech stack

- **Backend:** Python 3.11, FastAPI, Uvicorn, Pydantic, SQLite (stdlib),
  pypdf, httpx, python-dotenv, python-multipart — see
  `backend/requirements.txt` (direct deps only).
- **Frontend:** Streamlit + requests — see `frontend/requirements.txt`.
- **AI:** Google Gemini (`gemini-2.5-flash` default) over HTTPS; local
  TF-IDF retrieval; deterministic rule/merge engines for gaps, roadmap and
  Twin updates (testable without network).
- **Tests:** pytest (unit + integration + API + security + end-to-end).

---

## 📁 Project structure

```text
skilltwin-ai/
├── README.md  render.yaml  .env.example
├── backend/
│   ├── requirements.txt  Dockerfile
│   ├── app/  (api agents auth chat config context db knowledge llm
│   │          memory planner recommendations reflection research
│   │          resume roadmap sessions twin)
│   └── tests/  (pytest suite)
└── frontend/
    ├── requirements.txt  app.py
    ├── pages/  (Home Chat Profile Resume Roadmap Runtime)
    ├── services/api.py  components/header.py
```

---

## 🚀 Setup

### Prerequisites

- Python 3.11+
- (Optional) a Google Gemini API key for full LLM replies. Without it the
  app runs in honest local Twin mode.

### 1. Clone & configure

```bash
git clone https://github.com/dusssi/skilltwin-ai.git
cd skilltwin-ai
cp .env.example .env
# edit .env — at minimum set GEMINI_API_KEY (or leave empty)
```

### 2. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.api.main:app --reload
```

Backend: `http://127.0.0.1:8000` · Swagger: `http://127.0.0.1:8000/docs`

### 3. Frontend (new terminal)

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Frontend: `http://localhost:8501` (set `BACKEND_URL` if the API lives elsewhere)

### 4. Docker (backend)

```bash
cd backend
docker build -t skilltwin-backend .
docker run -p 8000:8000 --env-file ../.env skilltwin-backend
```

---

## ⚙️ Environment variables

See `.env.example` for the full list. Key ones:

| Variable | Default | Purpose |
|---|---|---|
| `GEMINI_API_KEY` | *(empty)* | Gemini key; empty ⇒ local Twin mode |
| `GEMINI_MODEL` | `gemini-2.5-flash` | LLM model name |
| `SKILLTWIN_DB_PATH` | `backend/data/skilltwin.db` | SQLite file |
| `SKILLTWIN_UPLOAD_DIR` | `backend/uploads` | Resume storage |
| `SKILLTWIN_MAX_UPLOAD_MB` | `5` | Upload cap |
| `SKILLTWIN_TOKEN_EXPIRE_HOURS` | `72` | Token lifetime |
| `SKILLTWIN_CORS_ORIGINS` | Streamlit localhost | Allowed origins |
| `SKILLTWIN_RATE_LIMIT_*` | on / 120 / 15 | Throttling |
| `SKILLTWIN_RAG_THRESHOLD` | `0.12` | Retrieval relevance floor |
| `BACKEND_URL` | `http://127.0.0.1:8000` | Frontend → API |

---

## 🗄️ Database

SQLite file auto-created on startup (`init_db()` in the app lifespan) with
19 tables: `users, auth_tokens, profiles, career_goals, skills,
user_skills, skill_history, projects, resumes, resume_analyses,
skill_gap_snapshots, roadmaps, roadmap_items, progress_events, memories,
sessions, messages, recommendations`. No manual migration step; the skill
catalog (50 skills + aliases) seeds automatically. All access goes through
`app/db/*` repositories so PostgreSQL can replace SQLite later.

---

## 📡 API documentation

Interactive docs at `/docs` (OpenAPI). Main endpoints (all user routes need
`Authorization: Bearer <token>`):

| Method & path | Purpose |
|---|---|
| `GET /health`, `GET /ready` | Liveness / readiness (public) |
| `POST /auth/register`, `POST /auth/login`, `GET /auth/me`, `POST /auth/logout` | Auth |
| `GET /twin`, `PATCH /twin`, `GET /twin/summary` | Twin view & update |
| `GET/POST /twin/skills`, `GET /twin/skills/history`, `GET /twin/gaps` | Skills & gaps |
| `GET/POST /twin/goals`, `PATCH /twin/goals/{id}` | Goals |
| `GET/POST /twin/projects` | Projects |
| `POST /resume/analyze`, `POST /resume/upload`, `GET /resume/history` | Resume pipeline |
| `POST /chat`, `GET /chat/sessions`, `GET /chat/sessions/{id}/messages` | Chat |
| `GET /roadmap`, `POST /roadmap/generate`, `PATCH /roadmap/items/{id}` | Roadmap |
| `POST /runtime` | Agent run |
| `GET/POST /memory`, `GET /memory/events` | Memory |
| `GET /recommendations`, `POST /recommendations/generate`, `PATCH /recommendations/{id}` | Recommendations |
| `GET /knowledge/search?q=` | Retrieval transparency |

Errors use `{"error": {"code", "message"}}` with proper HTTP statuses
(400/401/403/404/409/413/422/429/500).

---

## 🧪 Testing

```bash
cd backend
pytest            # full suite: unit + API + security + end-to-end
pytest tests/test_e2e.py -q   # the complete SkillTwin user journey
```

79 tests, all with real assertions. The suite uses isolated temp databases,
a stub LLM (no network), and covers previously fixed regressions
(extractor false positives, always-relevant retrieval, reflector arity,
uninitialized DB, path traversal, user isolation).

---

## 🚢 Deployment

- **Render:** root `render.yaml` provisions the API (with `/health` checks)
  and the Streamlit app. Set `GEMINI_API_KEY` in the dashboard. Note:
  Render's ephemeral disk resets SQLite/uploads on redeploy — for durable
  production data, attach a disk or point `SKILLTWIN_DB_PATH` at managed
  storage (the repository layer isolates this change).
- **Docker:** `backend/Dockerfile` builds a slim API image.

---

## 🧬 Skill Twin data model

```text
Twin(user)
├── profile: display_name, target_role, primary_goal, experience, education
├── skills[]: name, level 1-5, target_level, confidence,
│              evidence[{source, note, at}], history[level changes]
├── gaps[]: skill, current → target, gap, priority, reason, action
├── goals[], projects[], resumes[]+analyses[]
├── roadmap: items[{title, skill, difficulty, effort, priority,
│                   status, dependencies, resources}] + progress
├── memories[]: kind(fact/goal/preference/achievement/observation),
│               content, importance
└── events[]: resume_uploaded, skill_detected/improved, roadmap_*,
              career_goal_changed, project_completed, agent_run_completed…
```

Merge rules: evidence appends; levels only rise on credible evidence;
roadmap/project completions can push a level up; every change is
history-logged and evented.

---

## 🤖 Agent architecture (single orchestrator)

`app/agents/orchestrator.py` is the only execution architecture; specialists
(`skill`, `roadmap`, `resume`, `recommendation`, `research`, `reflection`)
communicate via typed `AgentRunState`. Runs persist artifacts (gap
snapshots, roadmaps, recommendations) and emit `agent_run_completed` events.

## 🧠 Memory architecture

- **Short-term:** per-user chat sessions + messages with deterministic
  summaries (`sessions/`).
- **Long-term:** importance-weighted memories with keyword recall
  (`memories` table).
- **Skill memory:** `skill_history` + per-skill evidence lists.
- **Event memory:** typed `progress_events` log.
- Chat assembles Twin + memory + relevant past context + threshold-gated
  knowledge into every prompt; replies and extracted facts flow back into
  sessions, memories and the Twin.

---

## ⚠️ Known limitations

- SQLite + local uploads suit single-instance deploys; use a disk volume or
  managed Postgres + object storage for scaled production.
- The knowledge base is a curated 11-topic seed (easily extended in
  `app/knowledge/seed.json`); no web search yet.
- Gap rubrics cover 5 roles + a general fallback; new roles need rubric
  entries in `app/twin/role_profiles.py`.
- Opaque bearer tokens are stateful (DB) — fine for MVP scale.
