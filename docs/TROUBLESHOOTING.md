# Troubleshooting & Debugging Guide
> **LPU Academic Copilot — Common Issues, Error Solutions, and Maintenance Rules**

This guide compiles common configuration errors, network anomalies, and environment issues with their respective solutions.

---

## 1. "Agent Orchestration Failed" (Immediate Crash)

### **A. Supabase Authentication JWT Mismatch**
* **Symptoms**: The browser displays a failure immediately upon clicking upload. The backend `/api/debug-logs` endpoint returns `{"logs":[],"histories":[]}`.
* **Reason**: The frontend and backend are using mismatched Supabase projects, or Vercel lacks the Supabase variables.
* **Fix**: Ensure that the `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` variables on Vercel match the backend's `SUPABASE_URL` and `SUPABASE_ANON_KEY` environment variables.

### **B. Supabase Email Rate Limits**
* **Symptoms**: Sign-up fails with `"email rate limit exceeded"` or login fails with `"Email not confirmed"`.
* **Fix**: Disable email verification in the Supabase console under **Authentication** -> **Providers** -> **Email** -> toggle off **"Confirm email"**.

---

## 2. Render Build or Connection Failures

### **A. OperationalError: Network is unreachable (Supabase IPv6)**
* **Symptoms**: Render log prints psycopg2 connection failures to `db.xxxx.supabase.co:5432`.
* **Reason**: Supabase direct database connection hosts resolve to IPv6 addresses, which Render's free tier networks cannot route.
* **Fix**: Replace your `DATABASE_URL` with your Supabase **Connection Pooler URI** (uses port **`6543`** instead of `5432` and connects to `*.pooler.supabase.com`).

### **B. ProgrammingError: invalid connection option "pgbouncer"**
* **Symptoms**: The server crashes with this error during startup.
* **Reason**: `psycopg2` fails to parse the `pgbouncer` URL query option.
* **Fix**: Strip `?pgbouncer=true` from your `DATABASE_URL` variable. The backend's `config.py` and `database.py` files contain automatic sanitizers to strip this parameter at boot.

---

## 3. PDF Downloads Fail with "Not Authenticated"

* **Symptoms**: Clicking the download button returns `{"detail":"Not authenticated"}`.
* **Reason**: Browser links (`<a>` elements) make standard GET requests that cannot append bearer authentication headers.
* **Fix**: The `/api/download/{syllabus_id}` endpoint has been made public in `main.py`. The lookup has been refactored to fetch the uploading user's profile (`syllabus.user_id`) to generate footer headers.

---

## 4. NameError: name 'datetime' or 'io' is not defined

* **Symptoms**: Backend logs throw `NameError` when compiling PDFs or uploading files.
* **Reason**: Python's standard `datetime` and `io` packages were not imported at the top of `main.py`.
* **Fix**: Add `import datetime` and `import io` to the imports section of [`main.py`](file:///C:/Users/AKASH%20PC/lpu-academic-copilot/backend/app/main.py).
