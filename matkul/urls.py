from django.urls import path
from . import views

app_name = "matkul"

urlpatterns = [
    path("matkul/", views.matkul_list_view, name="list"),
    path("matkul/tambah/", views.matkul_create_view, name="create"),
    path("matkul/<int:pk>/edit/", views.matkul_edit_view, name="edit"),
    path("matkul/<int:pk>/hapus/", views.matkul_delete_view, name="delete"),
]
