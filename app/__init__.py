"""app package

This module re-exports the FastAPI application instance so callers can
import the app with `from app import app`. That pattern is useful for
test clients (`TestClient(app)`) and some deployment tools that expect
the package to expose the ASGI app at package-level.
"""

# Re-export the application instance created in `main.py`
from .main import app

__all__ = ["app"]
