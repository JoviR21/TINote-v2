from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class MataKuliah(models.Model):
    HARI_CHOICES = [
        ("Senin", "Senin"),
        ("Selasa", "Selasa"),
        ("Rabu", "Rabu"),
        ("Kamis", "Kamis"),
        ("Jumat", "Jumat"),
        ("Sabtu", "Sabtu"),
    ]
    kode = models.CharField(max_length=20, unique=True, help_text="Contoh: TI101")
    nama = models.CharField(max_length=120)
    dosen = models.CharField(max_length=120, help_text="Nama dosen pengampu")
    no_wa_dosen = models.CharField(max_length=20, blank=True, default="", help_text="Contoh: 081234567890 (opsional, jadi tombol WA)")
    sks = models.PositiveSmallIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(6)], help_text="1-6")
    hari = models.CharField(max_length=10, choices=HARI_CHOICES)
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    ruang = models.CharField(max_length=50, blank=True, default="")
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["hari", "jam_mulai", "kode"]

    def __str__(self):
        return f"{self.kode} - {self.nama}"

    @property
    def jadwal_singkat(self):
        ruang = f" • {self.ruang}" if self.ruang else ""
        mulai = self.jam_mulai.strftime("%H:%M") if self.jam_mulai else ""
        selesai = self.jam_selesai.strftime("%H:%M") if self.jam_selesai else ""
        return f"{self.hari}, {mulai}-{selesai}{ruang} • {self.dosen} • {self.sks} SKS"

    @property
    def wa_link(self):
        import re
        digits = re.sub(r"\D", "", self.no_wa_dosen or "")
        if not digits:
            return ""
        if digits.startswith("0"):
            digits = "62" + digits[1:]
        return f"https://wa.me/{digits}"
