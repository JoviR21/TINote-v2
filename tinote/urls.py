from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda r: redirect("announcements:dashboard" if r.user.is_authenticated else "accounts:login")),
    path("", include("accounts.urls")),
    path("", include("matkul.urls")),
    path("", include("announcements.urls")),
]
