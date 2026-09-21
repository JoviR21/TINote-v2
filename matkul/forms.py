from django import forms
from .models import MataKuliah


class MataKuliahForm(forms.ModelForm):
    class Meta:
        model = MataKuliah
        fields = ["kode", "nama", "dosen", "no_wa_dosen", "sks", "hari", "jam_mulai", "jam_selesai", "ruang"]
        widgets = {
            "kode": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "TI101"}),
            "nama": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Pemrograman Web"}),
            "dosen": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Nama dosen"}),
            "no_wa_dosen": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "0812xxxx (opsional)"}),
            "sks": forms.NumberInput(attrs={"class": "input input-bordered w-full", "min": 1, "max": 6}),
            "hari": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "jam_mulai": forms.TimeInput(attrs={"class": "input input-bordered w-full", "type": "time"}),
            "jam_selesai": forms.TimeInput(attrs={"class": "input input-bordered w-full", "type": "time"}),
            "ruang": forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Ruang / Lab"}),
        }

    def clean_no_wa_dosen(self):
        import re
        wa = (self.cleaned_data.get("no_wa_dosen") or "").strip()
        if not wa:
            return ""
        digits = re.sub(r"\D", "", wa)
        if len(digits) < 9 or len(digits) > 15:
            raise forms.ValidationError("Nomor WA gak valid, cek lagi ya (9-15 digit).")
        return wa

    def clean(self):
        cleaned = super().clean()
        m, s = cleaned.get("jam_mulai"), cleaned.get("jam_selesai")
        if m and s and s <= m:
            self.add_error("jam_selesai", "Jam selesai harus lebih telat dari jam mulai.")
        return cleaned
