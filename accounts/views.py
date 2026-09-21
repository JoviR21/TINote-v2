import csv
import io
import random
import re
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from .forms import GantiPinForm, ImportCSVForm, LoginForm, UserForm
from .models import User


def staff_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != "staff":
            messages.error(request, "Eits, halaman ini khusus staff ya.")
            return redirect("announcements:dashboard")
        return view_func(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.user.is_authenticated:
        return redirect("announcements:dashboard")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        nim = form.cleaned_data["nim"].strip()
        pin = form.cleaned_data["pin"]
        user = authenticate(request, username=nim, password=pin)
        if user is not None:
            login(request, user)
            # Remember me: 3 hari, kalau enggak centang hangus pas browser tutup
            if form.cleaned_data.get("remember_me"):
                request.session.set_expiry(259200)
            else:
                request.session.set_expiry(0)
            messages.success(request, f"Halo {user.nama}, selamat datang lagi!")
            nxt = request.GET.get("next") or reverse("announcements:dashboard")
            return redirect(nxt)
        messages.error(request, "NIM atau PIN-nya keliru, coba lagi ya.")
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Udah logout, sampai jumpa lagi!")
    return redirect("accounts:login")


@login_required
def ganti_pin_view(request):
    form = GantiPinForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if not request.user.check_password(form.cleaned_data["pin_lama"]):
            messages.error(request, "PIN lama-nya salah.")
        else:
            request.user.set_password(form.cleaned_data["pin_baru"])
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "PIN berhasil diganti, jangan lupa ya!")
            return redirect("announcements:dashboard")
    return render(request, "accounts/ganti_pin.html", {"form": form})


@staff_required
def user_list_view(request):
    q = request.GET.get("q", "").strip()
    users = User.objects.all()
    if q:
        users = users.filter(nim__icontains=q) | users.filter(nama__icontains=q)
    return render(request, "accounts/user_list.html", {"users": users, "q": q})


@staff_required
def user_create_view(request):
    form = UserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        pin = form.cleaned_data.get("pin") or f"{random.randint(0, 999999):06d}"
        user = User(nim=form.cleaned_data["nim"].strip(), nama=form.cleaned_data["nama"].strip(), role=form.cleaned_data["role"])
        user.set_password(pin)
        user.save()
        messages.success(request, f"User {user.nim} kepake, PIN awal: {pin} — catat ya, cuma muncul sekali.")
        return redirect("accounts:user_list")
    return render(request, "accounts/user_form.html", {"form": form, "judul": "Tambah User"})


@staff_required
def user_edit_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        pin = form.cleaned_data.get("pin")
        if pin:
            user.set_password(pin)
        user.save()
        msg = f"User {user.nim} udah diupdate."
        if pin:
            msg += f" PIN baru: {pin} — catat ya."
        messages.success(request, msg)
        return redirect("accounts:user_list")
    return render(request, "accounts/user_form.html", {"form": form, "judul": f"Edit {user.nim}"})


@staff_required
def user_delete_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "Gak bisa hapus akun sendiri lah.")
        return redirect("accounts:user_list")
    if request.method == "POST":
        messages.success(request, f"User {user.nim} udah dihapus.")
        user.delete()
        return redirect("accounts:user_list")
    return render(request, "accounts/user_confirm_delete.html", {"user_obj": user})


@staff_required
def user_reset_pin_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        pin_baru = f"{random.randint(0, 999999):06d}"
        user.set_password(pin_baru)
        user.save()
        messages.success(request, f"PIN {user.nim} di-reset jadi: {pin_baru} — kasih ke orangnya, suruh ganti sendiri.")
    return redirect("accounts:user_list")


@staff_required
def user_import_view(request):
    form = ImportCSVForm(request.POST or None, request.FILES or None)
    hasil = None
    if request.method == "POST" and form.is_valid():
        try:
            data = request.FILES["file"].read().decode("utf-8-sig")
        except Exception:
            messages.error(request, "File-nya gak kebaca, pastikan CSV UTF-8 ya.")
            return render(request, "accounts/user_import.html", {"form": form, "hasil": None})
        reader = csv.reader(io.StringIO(data))
        ok, gagal, errors = 0, 0, []
        for i, row in enumerate(reader, start=1):
            if not row or all(not c.strip() for c in row):
                continue
            if len(row) < 4:
                gagal += 1
                errors.append(f"Baris {i}: kolom kurang, butuh NIM,Nama,Role,PIN")
                continue
            nim, nama, role, pin = [c.strip() for c in row[:4]]
            role = role.lower() if role.lower() in ("mahasiswa", "staff") else "mahasiswa"
            if not nim or not nama:
                gagal += 1
                errors.append(f"Baris {i}: NIM/nama kosong")
                continue
            if not re.fullmatch(r"\d{6}", pin or ""):
                gagal += 1
                errors.append(f"Baris {i} ({nim}): PIN harus 6 digit angka")
                continue
            if User.objects.filter(nim=nim).exists():
                gagal += 1
                errors.append(f"Baris {i} ({nim}): NIM udah ada, skip")
                continue
            u = User(nim=nim, nama=nama, role=role)
            u.set_password(pin)
            u.save()
            ok += 1
        hasil = {"ok": ok, "gagal": gagal, "errors": errors}
        messages.success(request, f"Import kelar: {ok} masuk, {gagal} gagal.")
    return render(request, "accounts/user_import.html", {"form": form, "hasil": hasil})
