from matkul.models import MataKuliah
from .models import Announcement, Komentar


def unread_inbox(request):
    """Badge inbox di navbar: hitung pengumuman/matkul/komentar baru sejak terakhir dibuka."""
    if not request.user.is_authenticated:
        return {}
    seen = request.user.inbox_seen_at
    if seen:
        ann = Announcement.objects.filter(dibuat_pada__gt=seen).exclude(dibuat_oleh=request.user).count()
        mk = MataKuliah.objects.filter(dibuat_pada__gt=seen).count()
        kom = Komentar.objects.filter(dibuat_pada__gt=seen).exclude(penulis=request.user).count()
    else:
        ann = Announcement.objects.exclude(dibuat_oleh=request.user).count()
        mk = MataKuliah.objects.count()
        kom = Komentar.objects.exclude(penulis=request.user).count()
    return {"unread_inbox": ann + mk + kom}
