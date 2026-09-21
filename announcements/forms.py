from django import forms
from .models import Announcement, Komentar


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["judul", "deskripsi", "kategori", "matkul", "deadline", "lokasi", "link"]
        widgets = {
            "judul": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Judul pengumuman"}),
            "deskripsi": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 5}),
            "kategori": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "matkul": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "deadline": forms.DateTimeInput(attrs={"class": "input input-bordered w-full", "type": "datetime-local"}),
            "lokasi": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Ruang / lokasi (opsional)"}),
            "link": forms.URLInput(attrs={"class": "input input-bordered w-full", "placeholder": "https://... (opsional)"}),
        }


class KomentarForm(forms.ModelForm):
    class Meta:
        model = Komentar
        fields = ["isi"]
        widgets = {
            "isi": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 2, "placeholder": "Tulis komentar santai aja..."}),
        }
