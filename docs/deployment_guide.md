# LPU Academic Copilot — Deployment Guide

This guide describes how to deploy the decoupled Next.js 15 frontend on Vercel and the FastAPI backend on Render.

---

## 1. Prerequisites
Ensure you have the following credentials:
1. **GitHub account** containing the pushed project code.
2. **Render account** (for FastAPI backend).
3. **Vercel account** (for Next.js frontend).
4. **Supabase project** (for PostgreSQL database, Auth, and Storage).

---

## 2. Supabase Configuration (Cloud Database)

### 2.1. SQL Database Setup
1. Log in to the [Supabase Console](https://supabase.com).
2. Create a new project.
3. Open the **SQL Editor** in the left menu.
4. Copy the complete SQL commands from [`schema.sql`](file:///C:/Users/AKASH%20PC/lpu-academic-copilot/schema.sql) in the project root.
5. Click **Run** to create the tables and set up Row Level Security (RLS) policies.

### 2.2. Supabase Storage Setup
1. Navigate to **Storage** in the left menu.
2. Create two new buckets:
   - Name: `syllabi` (Set access to Public/Private based on your security preferences).
   - Name: `reports` (Set access to Public/Private based on preferences).

---

## 3. Backend Deployment on Render

### 3.1. Render Setup
1. Log in to [Render Dashboard](https://render.com).
2. Click **New +** and select **Web Service**.
3. Link your GitHub repository.
4. Set the following properties:
   - **Name**: `lpu-academic-copilot-backend`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Region**: Select a region close to your target audience.

### 3.2. Render Environment Variables
Add the following key-value pairs in the **Environment** tab:
```env
PORT=8000
DATABASE_URL=your-supabase-connection-string (Transaction Pooler or Session Pooler URI)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-public-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
GEMINI_API_KEY=your-google-gemini-api-key
GROQ_API_KEY=your-groq-api-key (Optional)
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

---

## 4. Frontend Deployment on Vercel

### 4.1. Vercel Setup
1. Log in to the [Vercel Dashboard](https://vercel.com).
2. Click **Add New** and select **Project**.
3. Import your GitHub repository.
4. Set the following properties:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend`

### 4.2. Vercel Environment Variables
Add the following variables before clicking **Deploy**:
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-public-key
NEXT_PUBLIC_BACKEND_URL=https://lpu-academic-copilot-backend.onrender.com
```

---

## 5. Troubleshooting Guidelines

### 5.1. CORS Issues
If you encounter `CORS preflight request blocked` errors in your browser console:
- Ensure the `FRONTEND_URL` on Render matches your Vercel deployment URL exactly (with no trailing slash).
- If you're testing locally, ensure the `FRONTEND_URL` is set to `http://localhost:3000`.

### 5.2. Database Connection Timeouts
If the backend fails to start or times out:
- Double check that your `DATABASE_URL` is correct.
- If using Supabase, prefer the **Session Pooler** port (typically `5432` or transaction pooler `6543`) over direct connection, as cloud services can run out of connections.
