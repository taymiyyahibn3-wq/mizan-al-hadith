"""
Mīzān al-Ḥadīth - Web Application Entrypoint
Exposes the FastAPI application from backend/main.py at the mizan-web root
so that `python -m uvicorn main:app` can be executed directly from this directory.
"""
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR / "backend"

# Ensure both backend directory (for its internal modules) and root directory are in sys.path
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

# Import the FastAPI ASGI app from backend.main
from backend.main import app  # noqa: F401

__all__ = ["app"]
