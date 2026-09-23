from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from matkul.models import MataKuliah
from .forms import AnnouncementForm, KomentarForm
from .models import Announcement, Komentar, TandaiSelesai


@login_required
def inbox_view(request):
    if request.method == "POST":
        request.user.inbox_seen_at = timezone.now()
        request.user.save(update_fields=["inbox_seen_at"])
        messages.success(request, "Semua notif ditandai dibaca.")
        return redirect("announcements:inbox")
    ann = Announcement.objects.select_related("matkul").exclude(dibuat_oleh=request.user).order_by("-dibuat_pada")[:10]
    mk = MataKuliah.objects.order_by("-dibuat_pada")[:10]
    kom = Komentar.objects.select_related("penulis", "announcement").exclude(penulis=request.user).order_by("-dibuat_pada")[:10]
    seen = request.user.inbox_seen_at
    for a in ann:
        a.baru = seen is None or a.dibuat_pada > seen
    for m in mk:
        m.baru = seen is None or m.dibuat_pada > seen
    for k in kom:
        k.baru = seen is None or k.dibuat_pada > seen
    return render(request, "announcements/inbox.html", {
        "ann": ann, "mk": mk, "kom": kom, "seen": seen,
        "is_staff": request.user.role == "staff",
    })


@login_required
def dashboard_view(request):
    matkul_id = request.GET.get("matkul", "").strip()
    urut = request.GET.get("urut", "terdekat")

    items = Announcement.objects.select_related("matkul", "dibuat_oleh").annotate(
        jumlah_komentar=Count("komentars")
    )
    if matkul_id.isdigit():
        items = items.filter(matkul_id=int(matkul_id))
    items = items.order_by("deadline" if urut != "terjauh" else "-deadline")

    done_ids = set(TandaiSelesai.objects.filter(user=request.user).values_list("announcement_id", flat=True))
    now = timezone.now()
    total = items.count()
    hampir = sum(1 for a in items if timezone.timedelta(0) <= (a.deadline - now) <= timezone.timedelta(days=3))
    selesai = len([a for a in items if a.id in done_ids])
    lewat = sum(1 for a in items if a.deadline < now)

    for a in items:
        a.sudah_selesai = a.id in done_ids
        a.terlambat = (a.id not in done_ids) and a.sudah_lewat
        label, warna = a.badge_deadline()
        a.badge_label = label
        a.badge_warna = warna

    context = {
        "items": items,
        "matkuls": MataKuliah.objects.all(),
        "matkul_id": matkul_id,
        "urut": urut,
        "is_staff": request.user.role == "staff",
        "stat": {"total": total, "hampir": hampir, "selesai": selesai, "lewat": lewat},
    }
    return render(request, "announcements/dashboard.html", context)


@login_required
def detail_view(request, pk):
    obj = get_object_or_404(Announcement.objects.select_related("matkul", "dibuat_oleh"), pk=pk)
    komentars = obj.komentars.select_related("penulis").all()
    is_done = TandaiSelesai.objects.filter(user=request.user, announcement=obj).exists()
    form = KomentarForm(request.POST or None if "kirim_komentar" in request.POST else None)

    if request.method == "POST":
        if "kirim_komentar" in request.POST and form.is_valid():
            Komentar.objects.create(announcement=obj, penulis=request.user, isi=form.cleaned_data["isi"])
            messages.success(request, "Komentar kekirim.")
            return redirect("announcements:detail", pk=pk)
        if "toggle_selesai" in request.POST:
            ts, created = TandaiSelesai.objects.get_or_create(user=request.user, announcement=obj)
            if not created:
                ts.delete()
                messages.info(request, "Oke, ditandai belum selesai lagi.")
            else:
                messages.success(request, "Mantap, ditandai selesai!")
            return redirect("announcements:detail", pk=pk)

    label, warna = obj.badge_deadline()
    return render(request, "announcements/detail.html", {
        "obj": obj, "komentars": komentars, "form": form, "is_done": is_done,
        "badge_label": label, "badge_warna": warna,
        "is_staff": request.user.role == "staff",
    })


@login_required
def toggle_selesai_view(request, pk):
    obj = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        ts, created = TandaiSelesai.objects.get_or_create(user=request.user, announcement=obj)
        if not created:
            ts.delete()
    nxt = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/dashboard/"
    return redirect(nxt)


def _staff_only(request):
    return request.user.is_authenticated and request.user.role == "staff"


@login_required
def announcement_create_view(request):
    if not _staff_only(request):
        messages.error(request, "Khusus staff ya.")
        return redirect("announcements:dashboard")
    form = AnnouncementForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.dibuat_oleh = request.user
        obj.save()
        messages.success(request, "Pengumuman baru udah tayang.")
        return redirect("announcements:dashboard")
    return render(request, "announcements/announcement_form.html", {"form": form, "judul": "Tambah Pengumuman"})


@login_required
def announcement_edit_view(request, pk):
    if not _staff_only(request):
        messages.error(request, "Khusus staff ya.")
        return redirect("announcements:dashboard")
    obj = get_object_or_404(Announcement, pk=pk)
    form = AnnouncementForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengumuman udah diupdate.")
        return redirect("announcements:detail", pk=pk)
    return render(request, "announcements/announcement_form.html", {"form": form, "judul": f"Edit: {obj.judul}"})


@login_required
def announcement_delete_view(request, pk):
    if not _staff_only(request):
        messages.error(request, "Khusus staff ya.")
        return redirect("announcements:dashboard")
    obj = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Pengumuman dihapus.")
        return redirect("announcements:dashboard")
    return render(request, "announcements/announcement_confirm_delete.html", {"obj": obj})


@login_required
def komentar_delete_view(request, pk):
    komen = get_object_or_404(Komentar, pk=pk)
    boleh = request.user.role == "staff" or komen.penulis_id == request.user.id
    if not boleh:
        messages.error(request, "Gak bisa hapus komentar orang lain.")
        return redirect("announcements:detail", pk=komen.announcement_id)
    if request.method == "POST":
        aid = komen.announcement_id
        komen.delete()
        messages.success(request, "Komentar dihapus.")
        return redirect("announcements:detail", pk=aid)
    return render(request, "announcements/komentar_confirm_delete.html", {"obj": komen})
