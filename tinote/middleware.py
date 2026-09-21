from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class LoginRequiredMiddleware:
    """Semua orang wajib login. Selain login page + static/admin login, lempar ke /login/."""

    EXEMPT_PATHS = {"/login/", "/admin/login/"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if (
            not request.user.is_authenticated
            and not path.startswith("/static/")
            and not path.startswith("/admin/")
            and path not in self.EXEMPT_PATHS
        ):
            login_url = reverse("accounts:login")
            if path != login_url:
                return redirect(f"{login_url}?next={path}")
        return self.get_response(request)
