# Supabase Setup Guide for Atlas AI

## Step 1: Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com) and sign in
2. Click "New Project"
3. Fill in:
   - **Project Name:** atlas-ai (or your preferred name)
   - **Database Password:** Create a strong password (SAVE THIS!)
   - **Region:** Choose closest to your users (e.g., `us-east-1`, `eu-west-1`)
4. Click "Create new project" and wait for provisioning (~2 minutes)

## Step 2: Get Your Connection String

1. In your Supabase project dashboard, click **"Connect"** button (top right)
2. Select **"ORMs"** tab
3. Choose **"Transaction"** mode (Port 6543) - **IMPORTANT for FastAPI**
4. Copy the connection string that looks like:
   ```
   postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```
5. Replace `[YOUR-PASSWORD]` with your actual database password

## Step 3: Get Your API Keys

1. Go to **Project Settings** (gear icon in sidebar)
2. Click **"API"** in the left menu
3. Copy these values:
   - **Project URL:** `https://[PROJECT-REF].supabase.co`
   - **anon public key:** Long string starting with `eyJ...`
   - **service_role key:** Long string starting with `eyJ...` (keep this SECRET!)

## Step 4: Update Your .env File

Open `d:\Atlas-AI\backend\.env` and replace the placeholders:

```bash
# Database - Supabase PostgreSQL
DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres

# Supabase Configuration
SUPABASE_URL=https://[PROJECT-REF].supabase.co
SUPABASE_ANON_KEY=eyJ... (your anon key)
SUPABASE_SERVICE_KEY=eyJ... (your service role key)
```

**Example (with fake values):**
```bash
DATABASE_URL=postgresql://postgres.xyzabc123:[MyP@ssw0rd!]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
SUPABASE_URL=https://xyzabc123.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Step 5: Install Required Dependencies

Make sure you have the PostgreSQL adapter installed:

```bash
pip install psycopg2-binary
```

Or if you prefer the compiled version:
```bash
pip install psycopg2
```

## Step 6: Create Database Tables

The tables will be created automatically when you start the server. The `main.py` file has:
```python
Base.metadata.create_all(bind=engine)
```

This will create all tables defined in `models/database.py`.

## Step 7: Verify Connection

1. Stop the current server (Ctrl+C in the terminal)
2. Restart the server:
   ```bash
   python main.py
   ```
3. Check for successful startup messages
4. Visit `http://localhost:8000/health` to verify

## Step 8: View Your Data in Supabase

1. Go to your Supabase dashboard
2. Click **"Table Editor"** in the sidebar
3. You should see your tables: `users`, `profiles`, `skills`, `projects`, etc.

## Troubleshooting

### Error: "password authentication failed"
- Double-check your password in the DATABASE_URL
- Make sure there are no special characters that need URL encoding
- Try resetting your database password in Supabase settings

### Error: "could not connect to server"
- Verify your PROJECT-REF and REGION are correct
- Check if you're using port 6543 (Transaction mode)
- Ensure your internet connection is stable

### Error: "SSL connection required"
- Supabase requires SSL by default (this is already handled)
- If issues persist, add `?sslmode=require` to your connection string

### Connection Pooling Issues
- We're using `NullPool` for Supabase Transaction Pooler
- This is automatically configured in `config.py`
- No additional setup needed

## Security Best Practices

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Use service_role key only in backend** - Never expose in frontend
3. **Use anon key for frontend** - It's safe to expose
4. **Enable Row Level Security (RLS)** in Supabase for production
5. **Rotate keys regularly** in production environments

## Next Steps

1. ✅ Configure your `.env` with real Supabase credentials
2. ✅ Restart the server
3. ✅ Test API endpoints at `http://localhost:8000/docs`
4. 🔄 Set up Row Level Security policies in Supabase
5. 🔄 Configure backup and monitoring in Supabase dashboard

## Additional Resources

- [Supabase Python Docs](https://supabase.com/docs/reference/python/introduction)
- [Supabase Database Docs](https://supabase.com/docs/guides/database)
- [SQLAlchemy with Supabase](https://supabase.com/docs/guides/database/connecting-to-postgres)
