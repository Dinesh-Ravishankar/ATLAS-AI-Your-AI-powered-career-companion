# Steps to Connect Database - Atlas AI

## ✅ Step 1: Verify Your Supabase Credentials

Your current configuration:
- **Project Ref**: `ahxbyyzcozfhzmwhjavg`
- **Region**: `aws-1-ap-southeast-1`
- **Password**: `AtlasAI302007`

## 📋 Step 2: Verify Connection String Format

Your `.env` file should have (line 5):
```bash
DATABASE_URL=postgresql://postgres.ahxbyyzcozfhzmwhjavg:AtlasAI302007@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres
```

✅ **FIXED**: Removed duplicate `DATABASE_URL=` prefix

## 🔍 Step 3: Test Connection (Simple Method)

Create a minimal test file:

```python
# test_simple.py
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    print("✅ Connected successfully!")
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    print(f"PostgreSQL version: {cursor.fetchone()[0]}")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run it:
```bash
python test_simple.py
```

## 🚀 Step 4: Restart Backend Server

Once connection works:

```bash
# Stop the current server (it's been running with old config)
taskkill /F /PID 4720

# Start fresh with new .env
python main.py
```

## 🌐 Step 5: Verify API is Running

Open browser: http://localhost:8000/docs

You should see FastAPI Swagger UI.

## 🔧 Troubleshooting

### If connection still fails:

1. **Check Supabase Dashboard**:
   - Go to: https://supabase.com/dashboard/project/ahxbyyzcozfhzmwhjavg
   - Settings → Database → Connection String
   - Verify the password is correct

2. **Try Direct Connection** (Port 5432):
   ```bash
   DATABASE_URL=postgresql://postgres.ahxbyyzcozfhzmwhjavg:AtlasAI302007@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres
   ```

3. **Check Firewall**:
   - Ensure your network allows outbound connections to Supabase
   - Try from a different network if needed

4. **Reset Password**:
   - Supabase Dashboard → Database → Reset Database Password
   - Use a simple password without special characters
   - Update `.env` with new password

## 📝 Quick Reference

**Supabase Dashboard**: https://supabase.com/dashboard/project/ahxbyyzcozfhzmwhjavg

**Connection Modes**:
- **Transaction Pooling** (Port 6543): For serverless/FastAPI ✅ (Current)
- **Session Pooling** (Port 6543): For long-running connections
- **Direct Connection** (Port 5432): For migrations/admin tasks
