from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import MataKuliahForm
from .models import MataKuliah


@login_required
def matkul_list_view(request):
    items = MataKuliah.objects.all()
    return render(request, "matkul/matkul_list.html", {"items": items, "is_staff": request.user.role == "staff"})


def _staff_only(request):
    return request.user.is_authenticated and request.user.role == "staff"


@login_required
def matkul_create_view(request):
    if not _staff_only(request):
        messages.error(request, "Khusus staff ya.")
        return redirect("matkul:list")
    form = MataKuliahForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Matkul baru udah ditambah.")
        return redirect("matkul:list")
    return render(request, "matkul/matkul_form.html", {"form": form, "judul": "Tambah Matkul"})


@login_required
def matkul_edit_view(request, pk):
    if not _staff_only(request):
        messages.error(request, "Khusus staff ya.")
        return redirect("matkul:list")
    obj = get_object_or_404(MataKuliah, pk=pk)
    form = MataKuliahForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Matkul udah diupdate.")
        return redirect("matkul:list")
    return render(request, "matkul/matkul_form.html", {"form": form, "judul": f"Edit {obj.kode}"})


@login_required
def matkul_delete_view(request, pk):
    if not _staff_only(request):
        messages.error(request, "Khusus staff ya.")
        return redirect("matkul:list")
    obj = get_object_or_404(MataKuliah, pk=pk)
    if request.method == "POST":
        messages.success(request, f"Matkul {obj.kode} dihapus.")
        obj.delete()
        return redirect("matkul:list")
    return render(request, "matkul/matkul_confirm_delete.html", {"obj": obj})
