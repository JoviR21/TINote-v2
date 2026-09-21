from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("ganti-pin/", views.ganti_pin_view, name="ganti_pin"),
    path("manage/users/", views.user_list_view, name="user_list"),
    path("manage/users/tambah/", views.user_create_view, name="user_create"),
    path("manage/users/import/", views.user_import_view, name="user_import"),
    path("manage/users/<int:pk>/edit/", views.user_edit_view, name="user_edit"),
    path("manage/users/<int:pk>/hapus/", views.user_delete_view, name="user_delete"),
    path("manage/users/<int:pk>/reset-pin/", views.user_reset_pin_view, name="user_reset_pin"),
]
