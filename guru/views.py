from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout,authenticate, login as login_guru, get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from user.models import User, Guru, Murid
from django.conf import settings
from guru.models import Berita, Kegiatan, Video, Modul,Pengetesan, Pengajuan


def is_user(user):
    return user.role == User.GURU_ROLE

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def upload_berita(request):
    berita = Berita.objects.all()
    return render(request, 'uploadberita.html', {'berita':berita})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tambah_berita(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        foto_berita = request.FILES.get('berita')

        berita = Berita(judul=judul, deskripsi=deskripsi,foto_berita=foto_berita)
        if foto_berita:
            berita.foto_berita.save(foto_berita.name, foto_berita, save=True)
        berita.save()
        return redirect('upload_berita')
    return render(request, 'berita/tambahberita.html')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def edit_berita(request, id):
    berita = Berita.objects.get(id=id)
    return render(request, 'berita/editberita.html', {'berita':berita})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def update_berita(request, id):
    berita = get_object_or_404(Berita, id=id)
    if request.method == 'POST':
        berita.judul = request.POST['judul']
        berita.deskripsi = request.POST['deskripsi']
        if 'berita' in request.FILES:
            berita.foto_berita = request.FILES['berita']
        berita.save()
        messages.success(request,"Data Berhasil Diubah")
        return redirect('upload_berita')
    return render(request, 'berita/editberita.html', {'berita': berita})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def hapus_berita(request,id):
    if request.method=='POST':  
        berita = Berita.objects.get(id=id) 
        berita.delete()
    return redirect ('upload_berita')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def upload_kegiatan(request):
    kegiatan = Kegiatan.objects.all()
    return render(request, 'uploadkegiatan.html', {'kegiatan':kegiatan})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tambah_kegiatan(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        foto_kegiatan = request.FILES.get('kegiatan')

        kegiatan = Kegiatan(judul=judul, deskripsi=deskripsi,foto_kegiatan=foto_kegiatan)
        if foto_kegiatan:
            kegiatan.foto_kegiatan.save(foto_kegiatan.name, foto_kegiatan, save=True)
        kegiatan.save()
        return redirect('upload_kegiatan')
    return render(request, 'kegiatan/tambahkegiatan.html')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def edit_kegiatan(request, id):
    kegiatan = Kegiatan.objects.get(id=id)
    return render(request, 'kegiatan/editkegiatan.html', {'kegiatan':kegiatan})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def update_kegiatan(request, id):
    kegiatan = get_object_or_404(Kegiatan, id=id)
    if request.method == 'POST':
        kegiatan.judul = request.POST['judul']
        kegiatan.deskripsi = request.POST['deskripsi']
        if 'kegiatan' in request.FILES:
            kegiatan.foto_kegiatan = request.FILES['kegiatan']
        kegiatan.save()
        messages.success(request,"Data Berhasil Diubah")
        return redirect('upload_kegiatan')
    return render(request, 'kegiatan/editkegiatan.html', {'kegiatan': kegiatan})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def hapus_kegiatan(request,id):
    if request.method=='POST':  
        kegiatan = Kegiatan.objects.get(id=id) 
        kegiatan.delete()
    return redirect ('upload_kegiatan')




@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def guru_dashboard(request):
    video = Video.objects.all()
    return render(request, 'materi/video.html', {'video':video})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tambahvideomateri(request):
    if request.method == 'POST':
        materi = request.POST['materi']
        judul = request.POST['judul']
        deskripsi = request.POST['deskripsi']
        file_video = request.FILES['video']
        video = Video(judul=judul, materi=materi, deskripsi=deskripsi, file_video=file_video)
        video.save()
        return redirect('guruku')
    return render(request, 'materi/tambahvideo.html')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def editvideo(request, id):
    video = Video.objects.get(id=id)
    return render(request, 'materi/editvideo.html', {'video':video})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def updatevideo(request, id):
    video = get_object_or_404(Video, id=id)
    if request.method == 'POST':
        video.materi = request.POST['materi']
        video.judul = request.POST['judul']
        video.deskripsi = request.POST['deskripsi']
        if 'video' in request.FILES:
            video.file_video = request.FILES['video']
        video.save()
        messages.success(request, 'Data Berhasil Diubah')
        return redirect('guruku')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def delete_video(request, id):
    if request.method=='POST':  
        video = Video.objects.get(id=id) 
        video.delete()
    return redirect("guruku")


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def modulmateri(request):
    modul = Modul.objects.all()
    return render(request, 'materi/modul.html', {'modul':modul})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tambahmodulmateri(request):
    if request.method == 'POST':
        materi = request.POST['materi']
        judul = request.POST['judul']
        deskripsi = request.POST['deskripsi']
        file_modul = request.FILES['modul']
        modul = Modul(judul=judul, materi=materi, deskripsi=deskripsi, file_modul=file_modul)
        modul.save()
        return redirect('materi_modul')
    return render(request, 'materi/tambahmodul.html')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def editmodul(request, id):
    modul = Modul.objects.get(id=id)
    return render(request, 'materi/editmodul.html', {'modul':modul})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def updatemodul(request, id):
    modul = get_object_or_404(Modul, id=id)
    if request.method == 'POST':
        modul.materi = request.POST['materi']
        modul.judul = request.POST['judul']
        modul.deskripsi = request.POST['deskripsi']
        if 'modul' in request.FILES:
            modul.file_modul = request.FILES['modul']
        modul.save()
        messages.success(request, 'Data Berhasil Diubah')
        return redirect('materi_modul')
    
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def deletemodul(request, id):
    if request.method=='POST':  
        modul = Modul.objects.get(id=id) 
        modul.delete()
    return redirect("materi_modul")

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def pengetesan(request):
    pengetesan = Pengetesan.objects.all()
    return render(request, 'pengetesan.html', {'pengetesan':pengetesan})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tambah_pengetesan(request):
    if request.method == 'POST':
        judul = request.POST['judul']
        tingkat = request.POST['tingkat']
        materi = request.POST['materi']
        url = request.POST['url']
        test = Pengetesan(judul=judul, url=url, tingkat=tingkat, materi=materi)
        test.save()
        return redirect('pengetesan')
    return render(request, 'test/tambahpengetesan.html')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def editpengetesan(request, id):
    pengetesan = Pengetesan.objects.get(id=id)
    return render(request, 'test/editpengetesan.html', {'pengetesan':pengetesan})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def updatepengetesan(request, id):
    pengetesan = get_object_or_404(Pengetesan, id=id)
    if request.method == 'POST':
        pengetesan.judul = request.POST['judul']
        pengetesan.tingkat = request.POST['tingkat']
        pengetesan.materi = request.POST['materi']
        pengetesan.url = request.POST['url']
        pengetesan.save()
        messages.success(request, 'Data Berhasil Diubah')
        return redirect('pengetesan')
    
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def deletepengetesan(request, id):
    if request.method=='POST':  
        pengetesan = Pengetesan.objects.get(id=id) 
        pengetesan.delete()
    return redirect("pengetesan")

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def pengajuan_menghitung(request):
    pengajuan = Pengajuan.objects.all()
    return render(request, 'pengajuan_menghitung.html', {'pengajuan':pengajuan})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def setuju_pengajuan_menghitung(request, id):
    pengajuan = get_object_or_404(Pengajuan, id=id)

    if pengajuan.status == 'Menunggu Penilaian':
        pengajuan.status = 'Disetujui'
        pengajuan.save()

        if pengajuan.murid.menghitung == 'Menghitung Tingkat 1':
            pengajuan.murid.menghitung = 'Menghitung Tingkat 2'
            pengajuan.murid.save()

        elif pengajuan.murid.menghitung == 'Menghitung Tingkat 2':
            pengajuan.murid.menghitung = 'Menghitung Tingkat 3'
            pengajuan.murid.save()

    elif pengajuan.status == 'Ditolak':
        pengajuan.status = 'Disetujui'
        pengajuan.save()
        if pengajuan.murid.menghitung == 'Menghitung Tingkat 1':
            pengajuan.murid.menghitung = 'Menghitung Tingkat 2'
            pengajuan.murid.save()

        elif pengajuan.murid.menghitung == 'Menghitung Tingkat 2':
            pengajuan.murid.menghitung = 'Menghitung Tingkat 3'
            pengajuan.murid.save()

    return redirect('pengajuan_menghitung')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tolak_pengajuan_menghitung(request, id):
    pengajuan = get_object_or_404(Pengajuan, id=id)

    if pengajuan.status == 'Menunggu Penilaian':
        pengajuan.status = 'Ditolak'
        pengajuan.save()

    elif pengajuan.status == 'Disetujui':
        pengajuan.status = 'Ditolak'
        pengajuan.save()
    return redirect('pengajuan_menghitung')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def pengajuan_membaca(request):
    pengajuan = Pengajuan.objects.all()
    return render(request, 'pengajuan_membaca.html', {'pengajuan':pengajuan})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def setuju_pengajuan_membaca(request, id):
    pengajuan = get_object_or_404(Pengajuan, id=id)

    if pengajuan.status == 'Menunggu Penilaian':
        pengajuan.status = 'Disetujui'
        pengajuan.save()

        if pengajuan.murid.membaca == 'Membaca Tingkat 1':
            pengajuan.murid.membaca = 'Membaca Tingkat 2'
            pengajuan.murid.save()

        elif pengajuan.murid.membaca == 'Membaca Tingkat 2':
            pengajuan.murid.membaca = 'Membaca Tingkat 3'
            pengajuan.murid.save()

    elif pengajuan.status == 'Ditolak':
        pengajuan.status = 'Disetujui'
        pengajuan.save()
        if pengajuan.murid.membaca == 'Membaca Tingkat 1':
            pengajuan.murid.membaca = 'Membaca Tingkat 2'
            pengajuan.murid.save()

        elif pengajuan.murid.membaca == 'Membaca Tingkat 2':
            pengajuan.murid.membaca = 'Membaca Tingkat 3'
            pengajuan.murid.save()

    return redirect('pengajuan_membaca')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tolak_pengajuan_membaca(request, id):
    pengajuan = get_object_or_404(Pengajuan, id=id)

    if pengajuan.status == 'Menunggu Penilaian':
        pengajuan.status = 'Ditolak'
        pengajuan.save()

    elif pengajuan.status == 'Disetujui':
        pengajuan.status = 'Ditolak'
        pengajuan.save()
    return redirect('pengajuan_membaca')


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def pengajuan_menulis(request):
    pengajuan = Pengajuan.objects.all()
    return render(request, 'pengajuan_menulis.html', {'pengajuan':pengajuan})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def setuju_pengajuan_menulis(request, id):
    pengajuan = get_object_or_404(Pengajuan, id=id)

    if pengajuan.status == 'Menunggu Penilaian':
        pengajuan.status = 'Disetujui'
        pengajuan.save()

        if pengajuan.murid.menulis == 'Menulis Tingkat 1':
            pengajuan.murid.menulis = 'Menulis Tingkat 2'
            pengajuan.murid.save()

        elif pengajuan.murid.menulis == 'Menulis Tingkat 2':
            pengajuan.murid.menulis = 'Menulis Tingkat 3'
            pengajuan.murid.save()

    elif pengajuan.status == 'Ditolak':
        pengajuan.status = 'Disetujui'
        pengajuan.save()
        if pengajuan.murid.menulis == 'Menulis Tingkat 1':
            pengajuan.murid.menulis = 'Menulis Tingkat 2'
            pengajuan.murid.save()

        elif pengajuan.murid.menulis == 'Menulis Tingkat 2':
            pengajuan.murid.menulis = 'Menulis Tingkat 3'
            pengajuan.murid.save()

    return redirect('pengajuan_menulis')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tolak_pengajuan_menulis(request, id):
    pengajuan = get_object_or_404(Pengajuan, id=id)

    if pengajuan.status == 'Menunggu Penilaian':
        pengajuan.status = 'Ditolak'
        pengajuan.save()

    elif pengajuan.status == 'Disetujui':
        pengajuan.status = 'Ditolak'
        pengajuan.save()
    return redirect('pengajuan_menulis')