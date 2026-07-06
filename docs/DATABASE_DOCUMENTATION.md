# Database & Supabase Documentation
> **LPU Academic Copilot — PostgreSQL Relational Schema, Tables, and Supabase Configurations**

The database is built on **Supabase PostgreSQL**, managed locally via SQLAlchemy models and migrated using Alembic. 

---

## 1. Relational Schema ER Diagram

The relational layout links users to their settings, history, and generated academic packs:

```mermaid
erDiagram
    users {
        string id PK "auth.uid()"
        string email
        timestamp created_at
    }
    faculty_profiles {
        int id PK
        string user_id FK "users.id"
        string name
        string department
    }
    application_settings {
        int id PK
        string user_id FK "users.id"
        string llm_provider
        string model_name
        float temperature
    }
    syllabi {
        int id PK
        string user_id FK "users.id"
        string filename
        string file_path
        string raw_text
        string course_name
        string course_code
    }
    generation_histories {
        int id PK
        string user_id FK "users.id"
        int syllabus_id FK "syllabi.id"
        string status
        timestamp created_at
    }
    agent_execution_logs {
        int id PK
        int syllabus_id FK "syllabi.id"
        string agent_name
        string status
        string log_message
        timestamp created_at
    }

    users ||--o| faculty_profiles : owns
    users ||--o| application_settings : configures
    users ||--o| syllabi : uploads
    users ||--o| generation_histories : tracks
    syllabi ||--o| generation_histories : links
    syllabi ||--o| agent_execution_logs : prints
```

---

## 2. Table Specifications

### A. `users`
* Contains basic profile sync info from Supabase Auth.
* Column `id` is a `TEXT` matching the Supabase UID.

### B. `syllabi`
* Stores the parsed text and PDF storage location.
* Columns: `id` (serial), `user_id` (foreign key), `filename`, `file_path`, `raw_text`, `course_name`, `course_code`.

### C. `agent_execution_logs`
* Tracks the logs displayed in the frontend timeline.
* Columns: `id`, `syllabus_id` (foreign key), `agent_name`, `status` (`STARTED`, `COMPLETED`, `FAILED`), `log_message`, `created_at`.

---

## 3. Supabase Storage Integration
The application uses two buckets in Supabase Object Storage:
1. **`syllabi`**: Stores the uploaded syllabus PDFs.
2. **`reports`**: Stores the generated Course Pack report PDFs.

The backend uses the `SUPABASE_SERVICE_ROLE_KEY` to authenticate storage requests, bypassing client RLS policies during PDF write operations.
