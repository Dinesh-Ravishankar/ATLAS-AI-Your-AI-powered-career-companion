import sys, time
LOG = open("D:/Atlas-AI/backend/util_test.txt", "w", buffering=1)
sys.stdout = LOG
sys.stderr = LOG

def log(msg):
    LOG.write(f"[{time.time():.1f}] {msg}\n")
    LOG.flush()

log("Test: sqlalchemy.util.compat")
t = time.time()
try:
    import sqlalchemy.util.compat
    log(f"compat OK in {time.time()-t:.1f}s")
except Exception as e:
    log(f"compat FAIL: {e}")

log("Test: sqlalchemy.util._collections")
t = time.time()
try:
    import sqlalchemy.util._collections
    log(f"_collections OK in {time.time()-t:.1f}s")
except Exception as e:
    log(f"_collections FAIL: {e}")

log("Test: sqlalchemy.util.langhelpers")
t = time.time()
try:
    import sqlalchemy.util.langhelpers
    log(f"langhelpers OK in {time.time()-t:.1f}s")
except Exception as e:
    log(f"langhelpers FAIL: {e}")

log("Test: sqlalchemy.util.concurrency")
t = time.time()
try:
    import sqlalchemy.util.concurrency
    log(f"concurrency OK in {time.time()-t:.1f}s")
except Exception as e:
    log(f"concurrency FAIL: {e}")

log("Test: sqlalchemy.util.deprecations")
t = time.time()
try:
    import sqlalchemy.util.deprecations
    log(f"deprecations OK in {time.time()-t:.1f}s")
except Exception as e:
    log(f"deprecations FAIL: {e}")

log("ALL DONE")
