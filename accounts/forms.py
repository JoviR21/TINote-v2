import re
from django import forms
from .models import User


class LoginForm(forms.Form):
    nim = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "placeholder": "Contoh: TI001", "class": "input input-bordered w-full brutal-input", "autocomplete": "username",
    }))
    pin = forms.CharField(max_length=6, widget=forms.PasswordInput(attrs={
        "placeholder": "6 digit angka", "class": "input input-bordered w-full brutal-input", "autocomplete": "current-password",
    }))
    remember_me = forms.BooleanField(required=False, initial=False, label="Ingat saya (3 hari)")

    def clean_pin(self):
        pin = self.cleaned_data.get("pin", "")
        if not re.fullmatch(r"\d{6}", pin):
            raise forms.ValidationError("PIN harus tepat 6 digit angka.")
        return pin


class GantiPinForm(forms.Form):
    pin_lama = forms.CharField(max_length=6, widget=forms.PasswordInput(attrs={"class": "input input-bordered w-full"}))
    pin_baru = forms.CharField(max_length=6, widget=forms.PasswordInput(attrs={"class": "input input-bordered w-full"}))
    konfirmasi = forms.CharField(max_length=6, widget=forms.PasswordInput(attrs={"class": "input input-bordered w-full"}))

    def clean(self):
        cleaned = super().clean()
        for f in ("pin_baru", "konfirmasi", "pin_lama"):
            v = cleaned.get(f, "")
            if v and not re.fullmatch(r"\d{6}", v):
                self.add_error(f, "Harus tepat 6 digit angka.")
        if cleaned.get("pin_baru") and cleaned.get("konfirmasi") and cleaned["pin_baru"] != cleaned["konfirmasi"]:
            self.add_error("konfirmasi", "Konfirmasi beda sama PIN baru.")
        return cleaned


class UserForm(forms.ModelForm):
    pin = forms.CharField(max_length=6, required=False, help_text="Isi kalau mau set/ganti PIN. Kosongkan biar gak berubah.",
                           widget=forms.PasswordInput(attrs={"class": "input input-bordered w-full", "placeholder": "6 digit"}))

    class Meta:
        model = User
        fields = ["nim", "nama", "role"]
        widgets = {
            "nim": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "nama": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "role": forms.Select(attrs={"class": "select select-bordered w-full"}),
        }

    def clean_pin(self):
        pin = self.cleaned_data.get("pin", "")
        if pin and not re.fullmatch(r"\d{6}", pin):
            raise forms.ValidationError("PIN harus tepat 6 digit angka.")
        return pin


class ImportCSVForm(forms.Form):
    file = forms.FileField(help_text="Format CSV: NIM,Nama,Role,PIN — contoh: TI001,Budi Santai,mahasiswa,123456")
