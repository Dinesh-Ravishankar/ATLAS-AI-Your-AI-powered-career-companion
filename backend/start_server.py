import sys, os, time
LOG = open("D:/Atlas-AI/backend/startup_log.txt", "w", buffering=1, encoding="utf-8")
sys.stdout = LOG
sys.stderr = LOG
os.chdir("D:/Atlas-AI/backend")

def log(msg):
    LOG.write(f"[{time.time():.1f}] {msg}\n")
    LOG.flush()

log("START - importing sqlalchemy")
t = time.time()
from sqlalchemy import create_engine
log(f"sqlalchemy imported in {time.time()-t:.1f}s")

log("importing pydantic_settings")
t = time.time()
from pydantic_settings import BaseSettings
log(f"pydantic_settings imported in {time.time()-t:.1f}s")

log("importing config")
t = time.time()
from config import engine, settings
log(f"config imported in {time.time()-t:.1f}s")

log("importing fastapi")
t = time.time()
from fastapi import FastAPI
log(f"fastapi imported in {time.time()-t:.1f}s")

log("importing models.database")
t = time.time()
from models.database import Base
log(f"models.database imported in {time.time()-t:.1f}s")

log("importing api.routes.auth")
t = time.time()
from api.routes import auth
log(f"auth imported in {time.time()-t:.1f}s")

log("importing api.routes.coach")
t = time.time()
from api.routes import coach
log(f"coach imported in {time.time()-t:.1f}s")

log("importing api.routes.guide")
t = time.time()
from api.routes import guide
log(f"guide imported in {time.time()-t:.1f}s")

log("importing api.routes.roadmap")
t = time.time()
from api.routes import roadmap
log(f"roadmap imported in {time.time()-t:.1f}s")

log("ALL IMPORTS DONE - starting uvicorn")
import uvicorn
uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
