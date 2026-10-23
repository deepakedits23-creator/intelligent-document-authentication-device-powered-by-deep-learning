import uvicorn
import logging
from app.config import PROJECT_NAME, TAGLINE, DEVELOPER_CREDIT, EVENT_NAME
from app.database import init_db
from app.demo_data import seed_reference_database, generate_synthetic_samples

if __name__ == "__main__":
    print("=" * 70)
    print(f"  {PROJECT_NAME} — {TAGLINE}")
    print(f"  {DEVELOPER_CREDIT} | {EVENT_NAME}")
    print("=" * 70)
    print("  Initializing SQLite database & synthetic demo data...")
    init_db()
    seed_reference_database()
    generate_synthetic_samples(force=False)
    print("  Startup complete! Launching local web server...")
    print("  URL: http://127.0.0.1:8000")
    print("=" * 70)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
