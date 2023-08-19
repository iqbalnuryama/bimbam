from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.conf import settings
from guru.models import Berita, Kegiatan,Video, Modul, Pengajuan, Pengetesan
from user.models import Pembayaran, User
from murid.models import Murid
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
import mimetypes
import os
from django.http import HttpResponse


def is_user(user):
    return user.role == User.USER_ROLE

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def beranda(request):
    berita = Berita.objects.all()
    kegiatan = Kegiatan.objects.all()
    user = request.user
    pembayaran = Pembayaran.objects.get(user=user)
    
    if  pembayaran.status_pembayaran == 'Ditolak':
        pembayaran.delete()
        return redirect('/pembayaran/')
    return render (request, 'beranda.html', {'berita':berita, 'kegiatan':kegiatan})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def beritamurid(request):
    berita_list = Berita.objects.all()
    paginator = Paginator(berita_list, 5)
    page_number = request.GET.get('page')
    berita = paginator.get_page(page_number)
    return render(request, 'beritamurid.html', {'berita':berita})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def detailberitamurid(request, id):
    berita = Berita.objects.get(id=id)
    context = {
        'berita': berita
    }
    return render(request, 'detailberitamurid.html', context)

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def kegiatanmurid(request):
    kegiatan_list = Kegiatan.objects.all()
    paginator = Paginator(kegiatan_list, 5)
    page_number = request.GET.get('page')
    kegiatan = paginator.get_page(page_number)
    return render(request, 'kegiatanmurid.html', {'kegiatan':kegiatan})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def detailkegiatanmurid(request, id):
    kegiatan = Kegiatan.objects.get(id=id)
    context = {
        'kegiatan': kegiatan
    }
    return render(request, 'detailkegiatanmurid.html', context)

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tentangmurid(request):
    return render (request, 'tentangmurid.html')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def kontakmurid(request):
    return render (request, 'kontakmurid.html')


@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def materi(request):
    return render(request, 'pembelajaran/materi.html')



@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def pengetesan_murid(request):
    murid = Murid.objects.filter(user=request.user).first()
    if not murid:
        messages.error(request, 'Anda harus mengisi biodata terlebih dahulu.')
        return redirect('biodata')
    if murid.menghitung == 'Menghitung Tingkat 2':
        disable_tingkat2_menghitung = True 
    elif murid.menghitung == 'Menghitung Tingkat 3':
        disable_tingkat3_menghitung = True
        disable_tingkat2_menghitung = True  # Menonaktifkan tombol Tingkat 2
        return render(request, 'pembelajaran/pengetesan.html', {'disable_tingkat2_menghitung': disable_tingkat2_menghitung, 'disable_tingkat3_menghitung': disable_tingkat3_menghitung})
    
    if murid.membaca == 'Membaca Tingkat 2':
        disable_tingkat2_membaca = True 
    elif murid.membaca == 'Membaca Tingkat 3':
        disable_tingkat3_membaca = True
        disable_tingkat2_membaca = True  # Menonaktifkan tombol Tingkat 2
        return render(request, 'pembelajaran/pengetesan.html', {'disable_tingkat2_membaca': disable_tingkat2_membaca, 'disable_tingkat3_membaca': disable_tingkat3_membaca})
    
    if murid.menulis == 'Menulis Tingkat 2':
        disable_tingkat2_menulis = True 
    elif murid.menulis == 'Menulis Tingkat 3':
        disable_tingkat3_menulis = True
        disable_tingkat2_menulis = True  # Menonaktifkan tombol Tingkat 2
        return render(request, 'pembelajaran/pengetesan.html', {'disable_tingkat2_menulis': disable_tingkat2_menulis, 'disable_tingkat3_menulis': disable_tingkat3_menulis})
    return render (request, 'pembelajaran/pengetesan.html')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def level(request):
    user = request.user
    murid = Murid.objects.get(user=user)

    if not murid.is_biodata_completed:  # Ganti 'is_biodata_completed' dengan atribut yang menandakan apakah biodata telah diisi atau tidak
        return redirect('biodata')  # Ganti 'biodata' dengan URL halaman biodata yang sesuai

    return render(request, 'pembelajaran/level.html', {'murid': murid})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def status_tingkat_menghitung(request):
    murid = Murid.objects.filter(user=request.user).first()
    if not murid:
        return redirect('materimurid')  
    menghitung = ['Menghitung Tingkat 1', 'Menghitung Tingkat 2', 'Menghitung Tingkat 3']
    pengajuan = Pengajuan.objects.filter(murid=murid, murid__menghitung__in=menghitung).last()
    
    context = {
        'pengajuan': pengajuan,
    }
    
    return render(request, 'statustingkat_menghitung.html', context)

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def status_tingkat_membaca(request):
    murid = Murid.objects.filter(user=request.user).first()
    if not murid:
        return redirect('materimurid')  
    membaca = ['Membaca Tingkat 1', 'Membaca Tingkat 2', 'Membaca Tingkat 3']
    pengajuan = Pengajuan.objects.filter(murid=murid, murid__membaca__in=membaca).last()
    
    context = {
        'pengajuan': pengajuan,
    }
    
    return render(request, 'statustingkat_membaca.html', context)

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def status_tingkat_menulis(request):
    murid = Murid.objects.filter(user=request.user).first()
    if not murid:
        return redirect('materimurid')  
    menulis = ['Menulis Tingkat 1', 'Menulis Tingkat 2', 'Menulis Tingkat 3']
    pengajuan = Pengajuan.objects.filter(murid=murid, murid__menulis__in=menulis).last()
    
    context = {
        'pengajuan': pengajuan,
    }
    
    return render(request, 'statustingkat_menulis.html', context)



# menghitung test
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def pengetesan_murid_menghitung(request, tingkat):
    choices = ['Tingkat 1', 'Tingkat 2', 'Tingkat 3']
    materi = 'Menghitung'
    
    if tingkat in choices:
        murid = Murid.objects.filter(user=request.user).first()
        
        if not murid:
            return redirect('materimurid')  # Redirect jika murid tidak ditemukan

        if materi == 'Menghitung' and tingkat == 'Tingkat 2':
            if murid.menghitung == 'Menghitung Tingkat 2':
                return redirect('status_tingkat_menghitung')
            
            if request.method == 'POST':
                file_bukti = request.FILES.get('bukti')
                pengajuan = Pengajuan.objects.create(file_bukti=file_bukti, murid=murid, user=request.user)
                pengajuan.save()

                return redirect('status_tingkat_menghitung')
            
            pengetesan = Pengetesan.objects.filter(tingkat='Tingkat 2', materi=materi)
            pengetesan_id = pengetesan.first().id if pengetesan else None
        
        elif materi == 'Menghitung' and tingkat == 'Tingkat 3':
            if murid.menghitung == 'Menghitung Tingkat 3':
                return redirect('status_tingkat_menghitung')
            
            if murid.menghitung != 'Menghitung Tingkat 2':
                messages.error(request, 'Anda harus menjadi Tingkat 2 terlebih dahulu sebelum mengajukan Tingkat 3.')
                return redirect('materimurid')
            
            if request.method == 'POST':
                file_bukti = request.FILES.get('bukti')
                pengajuan = Pengajuan.objects.create(file_bukti=file_bukti, murid=murid, user=request.user)
                pengajuan.save()
                
                return redirect('status_tingkat_menghitung')
            
            pengetesan = Pengetesan.objects.filter(tingkat='Tingkat 3', materi=materi)
            pengetesan_id = pengetesan.first().id if pengetesan else None
        
        else:
            pass
        
        return render(request, 'pembelajaran/pengetesan/menghitung/{}.html'.format(tingkat), {'pengetesan': pengetesan, 'tingkat': tingkat, 'pengetesan_id': pengetesan_id})
    
    else:
        messages.error(request, 'Tingkat tidak tersedia.')
        return redirect('materimurid')

# end test

# membaca test
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def pengetesan_murid_membaca(request, tingkat):
    choices = ['Tingkat 1', 'Tingkat 2', 'Tingkat 3']
    materi = 'Membaca'
    
    if tingkat in choices:
        murid = Murid.objects.filter(user=request.user).first()
        
        if not murid:
            return redirect('materimurid')  # Redirect jika murid tidak ditemukan

        if materi == 'Membaca' and tingkat == 'Tingkat 2':
            if murid.membaca == 'Membaca Tingkat 2':
                return redirect('status_tingkat_membaca')
            
            if request.method == 'POST':
                file_bukti = request.FILES.get('bukti')
                pengajuan = Pengajuan.objects.create(file_bukti=file_bukti, murid=murid, user=request.user)
                pengajuan.save()

                return redirect('status_tingkat_membaca')
            
            pengetesan = Pengetesan.objects.filter(tingkat='Tingkat 2', materi=materi)
            pengetesan_id = pengetesan.first().id if pengetesan else None
        
        elif materi == 'Membaca' and tingkat == 'Tingkat 3':
            if murid.membaca == 'Membaca Tingkat 3':
                return redirect('status_tingkat_membaca')
            
            if murid.membaca != 'Membaca Tingkat 2':
                messages.error(request, 'Anda harus menjadi Tingkat 2 terlebih dahulu sebelum mengajukan Tingkat 3.')
                return redirect('materimurid')
            
            if request.method == 'POST':
                file_bukti = request.FILES.get('bukti')
                pengajuan = Pengajuan.objects.create(file_bukti=file_bukti, murid=murid, user=request.user)
                pengajuan.save()
                
                return redirect('status_tingkat_membaca')
            
            pengetesan = Pengetesan.objects.filter(tingkat='Tingkat 3', materi=materi)
            pengetesan_id = pengetesan.first().id if pengetesan else None
        
        else:
            pass
        
        return render(request, 'pembelajaran/pengetesan/membaca/{}.html'.format(tingkat), {'pengetesan': pengetesan, 'tingkat': tingkat, 'pengetesan_id': pengetesan_id})
    
    else:
        messages.error(request, 'Tingkat tidak tersedia.')
        return redirect('materimurid')

# end test

# menulis test
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def pengetesan_murid_menulis(request, tingkat):
    choices = ['Tingkat 1', 'Tingkat 2', 'Tingkat 3']
    materi = 'Menulis'
    
    if tingkat in choices:
        murid = Murid.objects.filter(user=request.user).first()
        
        if not murid:
            return redirect('materimurid')  # Redirect jika murid tidak ditemukan

        if materi == 'Menulis' and tingkat == 'Tingkat 2':
            if murid.menulis == 'Menulis Tingkat 2':
                return redirect('status_tingkat_menulis')
            
            if request.method == 'POST':
                file_bukti = request.FILES.get('bukti')
                pengajuan = Pengajuan.objects.create(file_bukti=file_bukti, murid=murid, user=request.user)
                pengajuan.save()

                return redirect('status_tingkat_menulis')
            
            pengetesan = Pengetesan.objects.filter(tingkat='Tingkat 2', materi=materi)
            pengetesan_id = pengetesan.first().id if pengetesan else None
        
        elif materi == 'Menulis' and tingkat == 'Tingkat 3':
            if murid.menulis == 'Menulis Tingkat 3':
                return redirect('status_tingkat_menulis')
            
            if murid.menulis != 'Menulis Tingkat 2':
                messages.error(request, 'Anda harus menjadi Tingkat 2 terlebih dahulu sebelum mengajukan Tingkat 3.')
                return redirect('materimurid')
            
            if request.method == 'POST':
                file_bukti = request.FILES.get('bukti')
                pengajuan = Pengajuan.objects.create(file_bukti=file_bukti, murid=murid, user=request.user)
                pengajuan.save()
                
                return redirect('status_tingkat_menulis')
            
            pengetesan = Pengetesan.objects.filter(tingkat='Tingkat 3', materi=materi)
            pengetesan_id = pengetesan.first().id if pengetesan else None
        
        else:
            pass
        
        return render(request, 'pembelajaran/pengetesan/menulis/{}.html'.format(tingkat), {'pengetesan': pengetesan, 'tingkat': tingkat, 'pengetesan_id': pengetesan_id})
    
    else:
        messages.error(request, 'Tingkat tidak tersedia.')
        return redirect('materimurid')

# end test

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def menghitung(request, tingkat):
    choices = ['Tingkat 1', 'Tingkat 2', 'Tingkat 3']
    if tingkat in choices:
        if tingkat == 'Tingkat 2':
            pengajuan_tingkat2 = Pengajuan.objects.filter(user=request.user, murid__menghitung='Menghitung Tingkat 2').first()
            if not pengajuan_tingkat2 or pengajuan_tingkat2.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 2.')
                return redirect('materimurid')
            video = Video.objects.filter(materi='Menghitung Tingkat 2')
        elif tingkat == 'Tingkat 3':
            pengajuan_tingkat3 = Pengajuan.objects.filter(user=request.user, murid__menghitung='Menghitung Tingkat 3').first()
            if not pengajuan_tingkat3 or pengajuan_tingkat3.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 3.')
                return redirect('materimurid')
            video = Video.objects.filter(materi=['Menghitung Tingkat 2', 'Menghitung Tingkat 3'])
        else:
            video = Video.objects.filter(materi='Menghitung Tingkat 1')
        if video.exists():
            return render(request, 'pembelajaran/menghitung/{}.html'.format(tingkat), {'video': video, 'tingkat': tingkat})
        else:
            messages.error(request, 'Materi menghitung {} belum tersedia.'.format(tingkat))
            return redirect('materimurid')
    else:
        messages.error(request, 'Tingkat tidak tersedia.')
        return redirect('materimurid')
    
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def membaca(request, tingkat):
    choices = ['Tingkat 1', 'Tingkat 2', 'Tingkat 3']
    if tingkat in choices:
        if tingkat == 'Tingkat 2':
            pengajuan_tingkat2 = Pengajuan.objects.filter(user=request.user, murid__membaca='Membaca Tingkat 2').first()
            if not pengajuan_tingkat2 or pengajuan_tingkat2.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 2.')
                return redirect('materimurid')
            video = Video.objects.filter(materi='Membaca Tingkat 2')
        elif tingkat == 'Tingkat 3':
            pengajuan_tingkat3 = Pengajuan.objects.filter(user=request.user, murid__membaca='Membaca Tingkat 3').first()
            if not pengajuan_tingkat3 or pengajuan_tingkat3.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 3.')
                return redirect('materimurid')
            video = Video.objects.filter(materi=['Membaca Tingkat 2', 'Membaca Tingkat 3'])
        else:
            video = Video.objects.filter(materi='Membaca Tingkat 1')
        if video.exists():
            return render(request, 'pembelajaran/membaca/{}.html'.format(tingkat), {'video': video, 'tingkat': tingkat})
        else:
            messages.error(request, 'Materi membaca {} belum tersedia.'.format(tingkat))
            return redirect('materimurid')
    else:
        messages.error(request, 'Tingkat tidak tersedia.')
        return redirect('materimurid')
    
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def menulis(request, tingkat):
    choices = ['Tingkat 1', 'Tingkat 2', 'Tingkat 3']
    if tingkat in choices:
        if tingkat == 'Tingkat 2':
            pengajuan_tingkat2 = Pengajuan.objects.filter(user=request.user, murid__menulis='Menulis Tingkat 2').first()
            if not pengajuan_tingkat2 or pengajuan_tingkat2.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 2.')
                return redirect('materimurid')
            video = Video.objects.filter(materi='Menulis Tingkat 2')
        elif tingkat == 'Tingkat 3':
            pengajuan_tingkat3 = Pengajuan.objects.filter(user=request.user, murid__menulis='Menulis Tingkat 3').first()
            if not pengajuan_tingkat3 or pengajuan_tingkat3.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 3.')
                return redirect('materimurid')
            video = Video.objects.filter(materi=['Menulis Tingkat 2', 'Menulis Tingkat 3'])
        else:
            video = Video.objects.filter(materi='Menulis Tingkat 1')
        if video.exists():
            return render(request, 'pembelajaran/menulis/{}.html'.format(tingkat), {'video': video, 'tingkat': tingkat})
        else:
            messages.error(request, 'Materi menulis {} belum tersedia.'.format(tingkat))
            return redirect('materimurid')
    else:
        messages.error(request, 'Tingkat tidak tersedia.')
        return redirect('materimurid')
    
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def menghitung_modul(request, tingkat):
    choices = ['Tingkat 1', 'Tingkat 2', 'Tingkat 3']
    if tingkat in choices:
        if tingkat == 'Tingkat 2':
            pengajuan_tingkat2 = Pengajuan.objects.filter(user=request.user, murid__menghitung='Menghitung Tingkat 2').first()
            if not pengajuan_tingkat2 or pengajuan_tingkat2.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 2.')
                return redirect('materimurid')
            modul = Modul.objects.filter(materi='Menghitung Tingkat 2')
        elif tingkat == 'Tingkat 3':
            pengajuan_tingkat3 = Pengajuan.objects.filter(user=request.user, murid__menghitung='Menghitung Tingkat 3').first()
            if not pengajuan_tingkat3 or pengajuan_tingkat3.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 3.')
                return redirect('materimurid')
            modul = Modul.objects.filter(materi=['Menghitung Tingkat 2', 'Menghitung Tingkat 3'])
        else:
            modul = Modul.objects.filter(materi='Menghitung Tingkat 1')
        if modul.exists():
            return render(request, 'modul/menghitung/{}.html'.format(tingkat), {'modul': modul, 'tingkat': tingkat})
        else:
            messages.error(request, 'Materi menghitung {} belum tersedia.'.format(tingkat))
            return redirect('materimurid')
    else:
        messages.error(request, 'Tingkat tidak tersedia.')
        return redirect('materimurid')
    
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def membaca_modul(request, tingkat):
    choices = ['Tingkat 1', 'Tingkat 2', 'Tingkat 3']
    if tingkat in choices:
        if tingkat == 'Tingkat 2':
            pengajuan_tingkat3 = Pengajuan.objects.filter(user=request.user, murid__membaca='Membaca Tingkat 2').first()
            if not pengajuan_tingkat3 or pengajuan_tingkat3.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 2.')
                return redirect('materimurid')
            modul = Modul.objects.filter(materi='Membaca Tingkat 2')
        elif tingkat == 'Tingkat 3':
            pengajuan_tingkat3 = Pengajuan.objects.filter(user=request.user, murid__membaca='Membaca Tingkat 3').first()
            if not pengajuan_tingkat3 or pengajuan_tingkat3.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 3.')
                return redirect('materimurid')
            modul = Modul.objects.filter(materi=['Membaca Tingkat 2', 'Membaca Tingkat 3'])
        else:
            modul = Modul.objects.filter(materi='Membaca Tingkat 1')
        if modul.exists():
            return render(request, 'modul/membaca/{}.html'.format(tingkat), {'modul': modul, 'tingkat': tingkat})
        else:
            messages.error(request, 'Materi membaca {} belum tersedia.'.format(tingkat))
            return redirect('materimurid')
    else:
        messages.error(request, 'Tingkat tidak tersedia.')
        return redirect('materimurid')
    
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def menulis_modul(request, tingkat):
    choices = ['Tingkat 1', 'Tingkat 2', 'Tingkat 3']
    if tingkat in choices:
        if tingkat == 'Tingkat 2':
            pengajuan_tingkat2 = Pengajuan.objects.filter(user=request.user, murid__menulis='Menulis Tingkat 2').first()
            if not pengajuan_tingkat2 or pengajuan_tingkat2.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 2.')
                return redirect('materimurid')
            modul = Modul.objects.filter(materi='Menulis Tingkat 2')
        elif tingkat == 'Tingkat 3':
            pengajuan_tingkat3 = Pengajuan.objects.filter(user=request.user, murid__menulis='Menulis Tingkat 3').first()
            if not pengajuan_tingkat3 or pengajuan_tingkat3.status != 'Disetujui':
                messages.error(request, 'Anda belum diizinkan untuk mengakses tingkat 3.')
                return redirect('materimurid')
            modul = Modul.objects.filter(materi=['Menulis Tingkat 2', 'Menulis Tingkat 3'])
        else:
            modul = Modul.objects.filter(materi='Menulis Tingkat 1')
        if modul.exists():
            return render(request, 'modul/menulis/{}.html'.format(tingkat), {'modul': modul, 'tingkat': tingkat})
        else:
            messages.error(request, 'Materi menulis {} belum tersedia.'.format(tingkat))
            return redirect('materimurid')
    else:
        messages.error(request, 'Tingkat tidak tersedia.')
        return redirect('materimurid')
        



