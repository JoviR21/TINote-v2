from django.contrib import admin
from .models import Announcement, Komentar, TandaiSelesai


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("judul", "kategori", "matkul", "deadline", "dibuat_oleh")
    list_filter = ("kategori", "matkul")
    search_fields = ("judul", "deskripsi")


@admin.register(Komentar)
class KomentarAdmin(admin.ModelAdmin):
    list_display = ("announcement", "penulis", "dibuat_pada")
    search_fields = ("isi",)


@admin.register(TandaiSelesai)
class SelesaiAdmin(admin.ModelAdmin):
    list_display = ("user", "announcement", "selesai_pada")
