from django.conf import settings
from django.db import models
from django.utils import timezone


class Announcement(models.Model):
    KATEGORI_CHOICES = [
        ("jadwal", "Jadwal Kuliah"),
        ("tugas", "Tugas Kuliah"),
        ("event", "Event"),
    ]
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default="tugas")
    matkul = models.ForeignKey(
        "matkul.MataKuliah",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="announcements",
        help_text="Kosongkan kalau event umum, bukan matkul tertentu.",
    )
    deadline = models.DateTimeField(help_text="Tanggal + jam deadline / pelaksanaan.")
    lokasi = models.CharField(max_length=200, blank=True, default="", help_text="Ruang / lokasi event.")
    link = models.URLField(blank=True, default="", help_text="Link webinar / bootcamp / pengumpulan.")
    dibuat_oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="announcements"
    )
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diubah_pada = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return self.judul

    @property
    def sudah_lewat(self):
        return self.deadline < timezone.now()

    def badge_deadline(self):
        """Balikin (label, warna) santai: H-2, Hari ini, Terlewat."""
        now = timezone.now()
        selisih = self.deadline - now
        if selisih.total_seconds() < 0:
            return ("Terlewat", "badge-error")
        hari = selisih.days
        if self.deadline.date() == now.date():
            return ("Hari ini", "badge-warning")
        if hari == 0:
            return ("Besok", "badge-warning")
        if hari <= 3:
            return (f"H-{hari}", "badge-warning")
        return (f"H-{hari}", "badge-info")


class Komentar(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="komentars")
    penulis = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="komentars")
    isi = models.TextField(max_length=1000)
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["dibuat_pada"]

    def __str__(self):
        return f"{self.penulis.nim}: {self.isi[:30]}"


class TandaiSelesai(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tugas_selesai")
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="yang_selesai")
    selesai_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "announcement")
        ordering = ["-selesai_pada"]

    def __str__(self):
        return f"{self.user.nim} selesai {self.announcement_id}"
