# System Architecture & Diagrams Documentation
> **LPU HRDC Nexus — Enterprise Platform Blueprint & Diagrams**

LPU HRDC Nexus is an enterprise-grade Progressive Web App (PWA) designed to manage the end-to-end lifecycle of training programmes. It integrates Next.js 15, FastAPI, Supabase, Groq APIs, and a LangGraph AI reasoning workflow backed by pgvector RAG.

---

## 1. System Architecture Diagram
The high-level architecture decouples presentation, application logic, database storage, and AI reasoning.

```mermaid
graph TB
    subgraph Presentation Layer (PWA Client)
        FE[Next.js 15 Frontend / React 19] -->|Install stand-alone app| PWA[Installable Mobile/Desktop Client]
        FE -->|JWT Bearer Token| API_Gateway[FastAPI Endpoints]
    end

    subgraph Application Layer (FastAPI Backend)
        API_Gateway --> Auth_Dep[Auth Dependency / JWT Validation]
        API_Gateway --> CRUD_Svc[CRUD Service Core]
        API_Gateway --> Agent_Svc[LangGraph AI Orchestrator]
    end

    subgraph Storage & External Services
        Auth_Dep -->|Validate token| Supa_Auth[Supabase Auth]
        CRUD_Svc -->|SQLAlchemy Core / SQLite Fallback| Postgres[(Supabase PostgreSQL)]
        CRUD_Svc -->|Binary file upload| Storage[(Supabase Storage)]
        Agent_Svc -->|Embeddings RAG queries| pgvector[(pgvector Index)]
        Agent_Svc -->|LLM Completion| Groq[Groq Cloud LLM API]
    end
```

---

## 2. Component Diagram
Shows how different structural modules in the system interact.

```mermaid
graph LR
    subgraph UI Components
        Dashboard[Overview Dashboard]
        ProgPortal[Programmes Portal]
        AttHub[Attendance Hub]
        AssessClient[Assessments Client]
        FeedbackROI[Feedback & ROI surveys]
        AIChat[AI Knowledge Chat]
    end

    subgraph Backend Routers
        AuthRouter[Auth Router]
        ProgRouter[Programmes Router]
        AttRouter[Attendance Router]
        AssessRouter[Assessments Router]
        CertRouter[Certificates Router]
        AIRouter[AI Assistant Router]
    end

    Dashboard --> ProgRouter
    ProgPortal --> ProgRouter
    AttHub --> AttRouter
    AssessClient --> AssessRouter
    FeedbackROI --> ProgRouter
    AIChat --> AIRouter
```

---

## 3. Database Entity-Relationship (ER) Diagram
Shows the complete PostgreSQL database structure for LPU HRDC Nexus.

```mermaid
erDiagram
    users ||--o| profiles : "has one profile"
    users ||--o| application_settings : "has application setting"
    users ||--o| materials : "uploads many materials"
    users ||--o| attendance : "marks many attendances"
    users ||--o| assessment_submissions : "submits assessments"
    users ||--o| project_submissions : "submits projects"
    users ||--o| feedbacks : "writes feedbacks"
    users ||--o| certificates : "earns certificates"

    programmes ||--o{ sessions : "contains many sessions"
    programmes ||--o{ programme_trainers : "has many trainers"
    programmes ||--o{ programme_participants : "has many participants"
    programmes ||--o{ materials : "houses materials"
    programmes ||--o{ assessments : "houses assessments"
    programmes ||--o{ project_submissions : "houses projects"
    programmes ||--o{ feedbacks : "receives feedbacks"
    programmes ||--o{ certificates : "issues certificates"

    sessions ||--o{ attendance : "logs attendance"
    sessions ||--o{ materials : "references files"
    sessions ||--o{ assessments : "references quizzes"

    materials ||--o{ document_embeddings : "yields vector chunks"

    corporate_clients ||--o{ corporate_contracts : "signs contracts"
    programmes ||--o{ corporate_contracts : "satisfies contract"

    users {
        string id PK
        string email
        timestamp created_at
    }
    profiles {
        int id PK
        string user_id FK
        string name
        string role
        string department
        string phone
        string designation
    }
    programmes {
        int id PK
        string title
        text description
        string category
        string mode
        string venue
        string coordinator_id FK
        timestamp start_date
        timestamp end_date
        int max_capacity
        string status
    }
    sessions {
        int id PK
        int programme_id FK
        int session_number
        string title
        date date
        string start_time
        string end_time
        string venue
        string trainer_id FK
        string attendance_qr_code
        timestamp attendance_window_start
        timestamp attendance_window_end
        boolean gps_verification
        float gps_lat
        float gps_lng
        float gps_radius_meters
    }
    attendance {
        int id PK
        int session_id FK
        string participant_id FK
        string status
        timestamp timestamp
        float gps_lat
        float gps_lng
        boolean verified_by_gps
        boolean verified_by_qr
        boolean manual_override
        string overridden_by FK
        text notes
    }
    materials {
        int id PK
        string title
        string file_path
        string file_url
        string file_type
        int programme_id FK
        int session_id FK
        string uploaded_by FK
        boolean is_indexed
    }
    document_embeddings {
        int id PK
        int material_id FK
        string filename
        text text_chunk
        vector embedding
    }
    corporate_contracts {
        int id PK
        int client_id FK
        int programme_id FK
        string invoice_number
        float invoice_amount
        string invoice_status
    }
```

---

## 4. Deployment Diagram
LPU HRDC Nexus is a cloud-native platform utilizing Render, Vercel, and Supabase.

```mermaid
graph TD
    Client([Browser / Mobile PWA]) -->|HTTPS| Vercel[Vercel Serverless Hosting]
    Vercel -->|Serves Static Files| HTML[HTML/JS/PWA assets]
    
    Client -->|REST Requests| Render[Render Web Service]
    Render -->|Runs Docker Container| FastAPI[FastAPI Backend / Python 3.12]
    
    FastAPI -->|JWT verification| Supa_Auth[Supabase Auth]
    FastAPI -->|pgvector Query| Supa_DB[Supabase Postgres Instance]
    FastAPI -->|File Storage| Supa_S3[Supabase Object Buckets]
    FastAPI -->|Token requests| Groq_Cloud[Groq LLM Engine API]
```

---

## 5. Sequence Diagram
Shows the sequence of logging geofenced and QR-validated classroom attendance.

```mermaid
sequenceDiagram
    autonumber
    actor Participant as User Participant
    participant App as Next.js Client
    participant API as FastAPI Backend
    participant DB as Postgres Database

    Participant->>App: Scan classroom QR & request check-in
    App->>App: Acquire Geolocation coordinates (navigator.geolocation)
    App->>API: POST /api/sessions/{id}/attendance (QR code, lat, lng)
    API->>DB: Fetch session attendance parameters (lat, lng, radius, QR hash, window)
    DB-->>API: Session configuration details
    API->>API: Verify scan time is within window
    API->>API: Verify QR code matches hash
    API->>API: Calculate distance between user coordinates & classroom center
    alt Validation Passed
        API->>DB: Save Attendance log (Present/Late)
        DB-->>API: Success
        API-->>App: Return 200 (Attendance marked)
        App-->>Participant: Present indicator marked successfully!
    else Validation Failed
        API-->>App: Return 400 (Verification Error)
        App-->>Participant: Display Out-Of-Boundary/Expired Error
    end
```

---

## 6. Class Diagram
Represents the key object schemas inside the FastAPI app.

```mermaid
classDiagram
    class User {
        +id: String
        +email: String
        +created_at: DateTime
        +get_profile() Profile
    }
    class Profile {
        +id: Integer
        +user_id: String
        +name: String
        +role: String
        +department: String
        +phone: String
    }
    class Programme {
        +id: Integer
        +title: String
        +category: String
        +mode: String
        +start_date: DateTime
        +status: String
        +sessions: List[Session]
    }
    class Session {
        +id: Integer
        +programme_id: Integer
        +session_number: Integer
        +title: String
        +attendance_qr_code: String
        +gps_verification: Boolean
        +gps_lat: Float
        +gps_lng: Float
        +gps_radius_meters: Float
        +verify_geofence(lat, lng): Boolean
    }
    class Attendance {
        +id: Integer
        +session_id: Integer
        +participant_id: String
        +status: String
        +verified_by_gps: Boolean
        +verified_by_qr: Boolean
    }

    User "1" *-- "1" Profile
    Programme "1" *-- "many" Session
    Session "1" *-- "many" Attendance
```

---

## 7. LangGraph Workflow Diagram
Defines the multi-agent reasoning flow executed during AI Knowledge Assistant queries.

```mermaid
graph TD
    Query([User Query]) --> Classify[Intent Classification Agent]
    Classify --> Router[Router Agent]
    
    Router -->|ATTENDANCE| AttAgent[Attendance Agent]
    Router -->|PROGRAMME| ProgAgent[Programme Retrieval Agent]
    Router -->|DOCUMENT| DocAgent[Document Retrieval Agent / RAG]
    Router -->|ANALYTICS| AnalAgent[Analytics Agent]
    Router -->|REPORT| RepAgent[Report Generation Agent]
    
    AttAgent --> Validate[Response Validation Agent]
    ProgAgent --> Validate
    DocAgent --> Validate
    AnalAgent --> Validate
    RepAgent --> Validate
    
    Validate --> LLM[Groq LLM Engine / llama3-8b]
    LLM --> FinalResponse([Final Cited Response])
```

---

## 8. RAG Architecture Diagram
Defines how documents (PDFs, PPTs, DOCXs) are chunked, embedded, stored, and queried.

```mermaid
graph TD
    subgraph Ingestion Pipeline (Background Task)
        Doc[Uploaded PDF/PPT/Word File] --> Parser[PDFParser / Text Extractor]
        Parser --> Chunker[Chunker: 600 words + 150 overlap]
        Chunker --> Embedder[Offline ADA-002 Embedder Simulator]
        Embedder --> DB_Insert[Save Chunk & Embedding into public.document_embeddings]
    end

    subgraph Retrieval Pipeline (LangGraph Workflow)
        Query[User Chat Query] --> QueryEmbed[Embed Query Text]
        QueryEmbed --> VectorSearch[Cosine Similarity Search using pgvector hnsw]
        DB_Insert -->|Seed embeddings| pgvector[(Supabase pgvector Index)]
        pgvector -->|Return top 4 matched chunks| VectorSearch
        VectorSearch --> LLMContext[Compile into LLM system context]
    end
```
