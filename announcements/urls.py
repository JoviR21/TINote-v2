from django.urls import path
from . import views

app_name = "announcements"

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("announcement/tambah/", views.announcement_create_view, name="create"),
    path("announcement/<int:pk>/", views.detail_view, name="detail"),
    path("announcement/<int:pk>/edit/", views.announcement_edit_view, name="edit"),
    path("announcement/<int:pk>/hapus/", views.announcement_delete_view, name="delete"),
    path("announcement/<int:pk>/selesai/", views.toggle_selesai_view, name="toggle_selesai"),
    path("komentar/<int:pk>/hapus/", views.komentar_delete_view, name="komentar_delete"),
]
