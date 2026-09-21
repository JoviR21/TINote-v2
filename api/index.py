import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tinote.settings")

from django.core.wsgi import get_wsgi_application

_django_app = get_wsgi_application()

PREFIX = "/api/index"


def _restore_path(path: str) -> str:
    if path == PREFIX:
        return "/"
    if path.startswith(PREFIX + "/"):
        return path[len(PREFIX):]
    return path


class VercelPathMiddleware:
    """Jaga-jaga: kalau Vercel meneruskan path hasil rewrite (/api/index...),
    kembalikan ke path asli (/...) sebelum Django routing."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ["PATH_INFO"] = _restore_path(environ.get("PATH_INFO", "/"))
        return self.app(environ, start_response)


app = VercelPathMiddleware(_django_app)
