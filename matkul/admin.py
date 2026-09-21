from django.contrib import admin
from .models import MataKuliah


@admin.register(MataKuliah)
class MataKuliahAdmin(admin.ModelAdmin):
    list_display = ("kode", "nama", "dosen", "no_wa_dosen", "sks", "hari", "jam_mulai", "jam_selesai", "ruang")
    list_filter = ("hari", "sks")
    search_fields = ("kode", "nama", "dosen")
