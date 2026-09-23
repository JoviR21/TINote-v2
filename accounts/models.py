import re
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models


def validate_pin_format(pin: str):
    if not re.fullmatch(r"\d{6}", str(pin or "")):
        raise ValidationError("PIN harus tepat 6 digit angka, misal 123456.")


class UserManager(BaseUserManager):
    def create_user(self, nim, nama, pin, role="mahasiswa", **extra):
        if not nim:
            raise ValueError("NIM wajib diisi.")
        validate_pin_format(pin)
        user = self.model(nim=str(nim).strip(), nama=nama.strip(), role=role, **extra)
        user.set_password(str(pin))
        user.save(using=self._db)
        return user

    def create_superuser(self, nim, nama="Staff", pin="123456", **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        extra.setdefault("is_active", True)
        return self.create_user(nim=nim, nama=nama, pin=str(pin), role="staff", **extra)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("mahasiswa", "Mahasiswa"),
        ("staff", "Staff"),
    ]
    nim = models.CharField(max_length=30, unique=True, help_text="NIM dipakai buat login.")
    nama = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="mahasiswa")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    inbox_seen_at = models.DateTimeField(null=True, blank=True, help_text="Terakhir kali buka inbox.")

    objects = UserManager()

    USERNAME_FIELD = "nim"
    REQUIRED_FIELDS = ["nama"]

    class Meta:
        ordering = ["nim"]

    def __str__(self):
        return f"{self.nim} - {self.nama} ({self.role})"

    def save(self, *args, **kwargs):
        # Sinkronkan is_staff dengan role biar bisa masuk /admin/
        if self.role == "staff":
            self.is_staff = True
        super().save(*args, **kwargs)

    @property
    def is_staff_role(self):
        return self.role == "staff"
