# Production Deployment Guide
> **LPU Academic Copilot — Steps to Deploy Next.js on Vercel and FastAPI on Render**

This document provides instructions for setting up the production environment on **Vercel** and **Render** linked to your GitHub repository **LPU_FDP_Final_Project**.

---

## 1. Backend Deployment (Render)

We use Render's **Blueprints** feature to deploy the backend automatically using configuration files.

### **Step A: Setup using Blueprint Button**
Click this deployment link:
👉 **[Deploy Backend on Render](https://render.com/deploy?repo=https://github.com/bhattacharjee-akash/LPU_FDP_Final_Project)**

*Render will automatically read the `render.yaml` at the root of the project, configure Python environments, build scripts, start-up commands, and ports.*

### **Step B: Add Environment Variables in Render**
Ensure you fill in these keys under the environment variables prompt:
* `DATABASE_URL`: Your Supabase **Connection Pooler URI** (Port `6543`).
* `SUPABASE_URL`: Your Supabase Project URL.
* `SUPABASE_ANON_KEY`: Your Supabase public anonymous key.
* `SUPABASE_SERVICE_ROLE_KEY`: Your Supabase service role secret key.
* `GEMINI_API_KEY`: YOUR_GEMINI_API_KEY
* `FRONTEND_URL`: `https://frontend-five-gules-38.vercel.app`

---

## 2. Frontend Deployment (Vercel)

Vercel hosts the Next.js app.

### **Step A: Link Project in Vercel**
1. Log in to Vercel and connect your GitHub account.
2. Select **"Import Project"** and choose your repository: **`LPU_FDP_Final_Project`**.
3. Choose the **Root Directory** as **`frontend`** (Next.js is inside this subdirectory).
4. Set the Framework Preset as **Next.js**.

### **Step B: Add Environment Variables in Vercel**
Add these three environment variables:
1. **`NEXT_PUBLIC_BACKEND_URL`**: `https://lpu-academic-copilot-backend.onrender.com`
2. **`NEXT_PUBLIC_SUPABASE_URL`**: `https://iqytwvoyignnohsyhhdn.supabase.co`
3. **`NEXT_PUBLIC_SUPABASE_ANON_KEY`**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### **Step C: Deploy**
Click **"Deploy"**. Vercel will build and deploy the Next.js app to production, linking it automatically to the Render backend and Supabase Auth.

---

## 3. Post-Deployment Verification
- Open the backend liveness check in your browser:  
  `https://lpu-academic-copilot-backend.onrender.com/api/debug-logs`  
  It should return `{"logs":[],"histories":[]}` with a `200 OK` status, showing the database is connected.
- Open the Vercel site:  
  `https://frontend-five-gules-38.vercel.app`  
  Register a user, upload a syllabus, and ensure the multi-agent timeline successfully processes and lets you download the compiled Course Pack.
