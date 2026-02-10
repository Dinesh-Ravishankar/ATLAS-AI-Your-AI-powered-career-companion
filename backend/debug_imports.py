import time, sys
sys.stdout.reconfigure(line_buffering=True)

def timed_import(name, stmt):
    print(f"  Importing {name}...", flush=True)
    t = time.time()
    try:
        exec(stmt)
        print(f"  OK {name} in {time.time()-t:.1f}s", flush=True)
    except Exception as e:
        print(f"  FAIL {name}: {e}", flush=True)

print("=== IMPORT DIAGNOSTIC ===", flush=True)

timed_import("fastapi", "import fastapi")
timed_import("sqlalchemy", "import sqlalchemy")
timed_import("config", "from config import engine")
timed_import("models.database", "from models.database import Base")
timed_import("api.routes.auth", "from api.routes import auth")
timed_import("api.routes.profile", "from api.routes import profile")
timed_import("api.routes.career", "from api.routes import career")
timed_import("api.routes.onboarding", "from api.routes import onboarding")
timed_import("api.routes.skills", "from api.routes import skills")
timed_import("api.routes.coach", "from api.routes import coach")
timed_import("api.routes.origin_story", "from api.routes import origin_story")
timed_import("api.routes.guide", "from api.routes import guide")
timed_import("api.routes.roadmap", "from api.routes import roadmap")

print("=== ALL IMPORTS DONE ===", flush=True)
