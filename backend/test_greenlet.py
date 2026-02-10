import sys, time
LOG = open("D:/Atlas-AI/backend/greenlet_test.txt", "w", buffering=1)
sys.stdout = LOG
sys.stderr = LOG

def log(msg):
    LOG.write(f"[{time.time():.1f}] {msg}\n")
    LOG.flush()

log("Test 1: import greenlet")
t = time.time()
try:
    import greenlet
    log(f"greenlet OK: {greenlet.__version__} in {time.time()-t:.1f}s")
except Exception as e:
    log(f"greenlet FAIL: {e}")

log("Test 2: import typing_extensions")
t = time.time()
try:
    import typing_extensions
    log(f"typing_extensions OK in {time.time()-t:.1f}s")
except Exception as e:
    log(f"typing_extensions FAIL: {e}")

log("Test 3: import sqlalchemy.util")
t = time.time()
try:
    import sqlalchemy.util
    log(f"sqlalchemy.util OK in {time.time()-t:.1f}s")
except Exception as e:
    log(f"sqlalchemy.util FAIL: {e}")

log("Test 4: from sqlalchemy import create_engine")
t = time.time()
try:
    from sqlalchemy import create_engine
    log(f"create_engine OK in {time.time()-t:.1f}s")
except Exception as e:
    log(f"create_engine FAIL: {e}")

log("ALL DONE")
