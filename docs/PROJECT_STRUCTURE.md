# Project Directory Layout
> **LPU Academic Copilot — Codebase Navigation Map**

This document details the folder hierarchy, workspace structures, and module layouts of the LPU Academic Copilot project.

---

## 1. Project Directory Tree

```text
LPU_FDP_Final_Project/
│
├── backend/                       # Python FastAPI Backend
│   ├── app/
│   │   ├── agents/                # 10 Specialized Orchestration Nodes
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py      # Abstract agent interface & LLM router
│   │   │   ├── planning_agent.py
│   │   │   ├── lesson_plan_agent.py
│   │   │   ├── assignment_agent.py
│   │   │   ├── quiz_agent.py
│   │   │   ├── question_paper_agent.py
│   │   │   ├── bloom_agent.py
│   │   │   ├── co_mapping_agent.py
│   │   │   ├── reviewer_agent.py
│   │   │   ├── academic_quality_agent.py
│   │   │   └── pdf_generator.py   # PDF rendering module
│   │   │
│   │   ├── prompts/               # System & inference text instructions
│   │   │   ├── planning_prompt.txt
│   │   │   ├── lesson_plan_prompt.txt
│   │   │   └── ...
│   │   │
│   │   ├── auth.py                # Supabase session JWT decoders
│   │   ├── config.py              # Environment configuration & URL sanitizers
│   │   ├── database.py            # SQLite/PostgreSQL connection engine
│   │   ├── crud.py                # Database read/write helpers
│   │   ├── models.py              # SQLAlchemy database tables mapping
│   │   ├── schemas.py             # Pydantic schemas for request validation
│   │   └── main.py                # FastAPI routes & background task orchestrator
│   │
│   ├── migrations/                # Alembic database migration scripts
│   ├── render.yaml                # Render Infrastructure blueprint configuration
│   └── requirements.txt           # Python backend dependencies list
│
├── frontend/                      # Next.js 15 Client App
│   ├── public/                    # Static images, assets, and icons
│   ├── src/
│   │   ├── app/                   # App Router Page tree
│   │   │   ├── dashboard/         # Faculty protected portal
│   │   │   │   ├── upload/        # Syllabus uploader and live timeline
│   │   │   │   ├── history/       # Past generations list
│   │   │   │   └── settings/      # Faculty profiles settings
│   │   │   ├── login/             # Login screen (Supabase widget)
│   │   │   ├── layout.tsx         # Root HTML wrappers
│   │   │   └── page.tsx           # Product Landing Page
│   │   │
│   │   ├── components/            # Shared UI components
│   │   │   ├── agent-timeline.tsx # Live pipeline timeline log streams
│   │   │   ├── navbar.tsx
│   │   │   └── sidebar.tsx
│   │   │
│   │   └── lib/                   # Client state libraries
│   │       ├── api.ts             # API wrapper request client
│   │       └── supabase.ts        # Supabase browser client setup
│   │
│   ├── vercel.json                # Vercel routing configurations
│   └── package.json               # Frontend dependencies manifest
│
└── scripts/                       # Local execution testing scripts
    ├── sample_syllabus.pdf        # Test document
    ├── test_pipeline.py           # Sync local workflow validation check
    └── test_live_api.py           # End-to-end integration test runner
```
