import sys, time
f = open("D:/Atlas-AI/backend/compat_test.txt", "w", buffering=1)
f.write(f"[{time.time():.1f}] Starting\n"); f.flush()
import sqlalchemy.util.compat
f.write(f"[{time.time():.1f}] compat imported OK\n"); f.flush()
import sqlalchemy
f.write(f"[{time.time():.1f}] sqlalchemy imported OK: {sqlalchemy.__version__}\n"); f.flush()
f.write(f"[{time.time():.1f}] ALL DONE\n"); f.flush()
