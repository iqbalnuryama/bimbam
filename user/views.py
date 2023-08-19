from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,authenticate, login as auth_login, get_user_model
from django.contrib import messages
from .models import Pembayaran
from murid.models import Murid
from guru.models import Berita, Kegiatan
import traceback
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings 
from django.urls import reverse
from django.db import IntegrityError
User = get_user_model()


def is_user(user):
    return user.role == User.USER_ROLE

def index(request):
    berita = Berita.objects.all()
    kegiatan = Kegiatan.objects.all()
    return render(request, 'index.html', {'berita':berita, 'kegiatan':kegiatan})
def buatpass(request):
    return render(request, 'buatpass.html')

def tentang(request):
    return render(request, 'tentang.html')
def pembelajaran(request):
    return render(request, 'daftarsekarang.html')
# berita
def berita(request):
    berita_list = Berita.objects.all()
    paginator = Paginator(berita_list, 5)
    page_number = request.GET.get('page')
    berita = paginator.get_page(page_number)
    return render(request, 'berita.html', {'berita':berita})
def detailberita(request, id):
    berita = Berita.objects.get(id=id)
    context = {
        'berita': berita
    }
    return render(request, 'detailberita.html', context)
# end
def kegiatan(request):
    kegiatan_list = Kegiatan.objects.all()
    paginator = Paginator(kegiatan_list, 5)
    page_number = request.GET.get('page')
    kegiatan = paginator.get_page(page_number)
    return render(request, 'kegiatan.html', {'kegiatan':kegiatan})
def detailkegiatan(request, id):
    kegiatan = Kegiatan.objects.get(id=id)
    context = {
        'kegiatan': kegiatan
    }
    return render(request, 'detailkegiatan.html', context)
def kontak(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        email = request.POST['email']
        subjek = request.POST['subjek']
        komentar = request.POST['komentar']

        # Mengirim email
        send_mail(
            subjek,
            f'Nama: {nama}\nEmail: {email}\nKomentar: {komentar}',
            email,  # Menggunakan alamat email yang diinputkan oleh pengguna sebagai pengirim
            ['iqbalbeutik19@gmail.com'],  # Ganti dengan alamat email penerima
            fail_silently=False,
        )

        # Redirect atau tampilkan pesan sukses setelah pengiriman email
        messages.success(request,'Pesan Terkirim')
    return render(request, 'kontak.html')


# pendfatran
def caradaftar(request):
    return render(request, 'pendaftaran/caradaftar.html')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def biodata(request):
    try:
        # Cek apakah pengguna saat ini sudah memiliki data mahasiswa
        murid = Murid.objects.get(user=request.user)
        button_text = "Edit"
        nama = murid.nama
        jenis_kelamin = murid.jenis_kelamin
        tempat_lahir = murid.tempat_lahir
        tanggal_lahir = murid.tanggal_lahir
        anak_ke = murid.anak_ke
        agama = murid.agama
        alamat = murid.alamat
        nama_ayah = murid.nama_ayah
        nama_ibu = murid.nama_ibu
        no_handphone = murid.no_handphone
    except Murid.DoesNotExist:
        murid = None
        button_text = "Submit"
        nama = ''
        jenis_kelamin = ''
        tempat_lahir = ''
        tanggal_lahir = ''
        anak_ke = ''
        agama = ''
        alamat = ''
        nama_ayah = ''
        nama_ibu = ''
        no_handphone = ''


    if request.method == 'POST':
        nama = request.POST.get('nama')
        jenis_kelamin =request.POST.get('jk')
        tempat_lahir = request.POST.get('teml')
        tanggal_lahir = request.POST.get('tl')
        anak_ke = request.POST.get('ak')
        agama =request.POST.get('agama')
        alamat = request.POST.get('alamat')
        nama_ayah = request.POST.get('na')
        nama_ibu = request.POST.get('ni')
        no_handphone = request.POST.get('no')

        if murid:
            # Update data mahasiswa yang sudah ada
            murid.nama = nama
            murid.jenis_kelamin = jenis_kelamin
            murid.tempat_lahir = tempat_lahir
            murid.tanggal_lahir = tanggal_lahir
            murid.anak_ke = anak_ke
            murid.agama = agama
            murid.alamat = alamat
            murid.nama_ayah = nama_ayah
            murid.nama_ibu = nama_ibu
            murid.no_handphone = no_handphone
            murid.save()
            success_message = "Data mahasiswa berhasil diperbarui."
        else:
            # Buat data mahasiswa baru
            murid = Murid.objects.create(user=request.user, nama=nama, jenis_kelamin=jenis_kelamin, tempat_lahir=tempat_lahir, tanggal_lahir=tanggal_lahir, anak_ke=anak_ke,agama=agama,alamat=alamat,nama_ayah=nama_ayah,nama_ibu=nama_ibu,no_handphone=no_handphone)
            success_message = "Data mahasiswa berhasil disimpan."
            button_text = "Edit"

    else:
        success_message = None

    # Refresh objek mahasiswa dari database jika ada
    if murid:
        murid.refresh_from_db()

    return render(request, 'pendaftaran/biodata.html', {
        'success_message': success_message,
        'murid': murid,
        'button_text': button_text,
        'nama': nama,
        'jenis_kelamin': jenis_kelamin,
        'tempat_lahir': tempat_lahir,
        'tanggal_lahir': tanggal_lahir,
        'anak_ke': anak_ke,
        'agama': agama,
        'alamat': alamat,
        'nama_ayah': nama_ayah,
        'nama_ibu': nama_ibu,
        'no_handphone': no_handphone 
    })

def daftar(request):
    User.objects.filter(email='').delete()
    if request.method == 'POST':
        username = request.POST.get('nisn')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password1')

        # Memeriksa apakah email kosong
        if not email:
            messages.error(request, 'Email harus diisi.')
            return redirect('/daftar/')

        # Memeriksa apakah email sudah digunakan
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah digunakan.')
            return redirect('/daftar/')

        # Memeriksa apakah username sudah digunakan
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan.')
            return redirect('/daftar/')

        if password != confirm_password:
            messages.error(request, "Password tidak sesuai.")
            return redirect('/daftar/')

        hashed_password = make_password(password, confirm_password)

        user = User(username=username, email=email, password=hashed_password)
        try:
            user.save()
        except IntegrityError as e:
            messages.error(request, "Terjadi kesalahan saat menyimpan data pengguna.")
            traceback.print_exc()  # Cetak traceback kesalahan di konsol
            return redirect('/daftar/')

        # Authenticate user
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            # User authentication successful
            messages.success(request, "Akun Kamu Berhasil Dibuat, Silahkan Lakukan Login")
            return redirect('/daftar/')
        else:
            # User authentication failed
            messages.error(request, "Terjadi kesalahan saat membuat akun.")
            return redirect('/daftar/')
        

    else:
        return render(request, "pendaftaran/daftar.html")

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('nisn')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.role == User.ADMIN_ROLE:
                return redirect('admin')
            elif user.role == User.GURU_ROLE:
                return redirect('guruku')
            elif user.role == User.USER_ROLE:
                pembayaran = Pembayaran.objects.filter(user=user).first()
                if pembayaran is not None:
                    if pembayaran.status_pembayaran == 'Disetujui':
                        return redirect('beranda')
                    elif pembayaran.status_pembayaran == 'Menunggu':
                        messages.success(request, 'Pembayaran sedang menunggu konfirmasi')
                        return redirect('pembayaran/status/')
                    elif pembayaran.status_pembayaran == 'Ditolak':
                        pembayaran.delete()
                        return redirect('/pembayaran/')
                else:
                    messages.success(request, 'Silahkan untuk melanjutkan pembayaran')
                    return redirect('/pembayaran/')

        messages.error(request, 'Username/Password salah atau Anda tidak memiliki izin untuk mengakses halaman ini.')
        return redirect('login')  # Mengarahkan pengguna kembali ke halaman login

    return render(request, 'login.html')




@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def pembayaran(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        jenis_bank = request.POST.get('jenis_bank')
        bukti_transfer = request.FILES.get('bt')
        pembayaran = Pembayaran(user=request.user, nama=nama, jenis_bank=jenis_bank, bukti_transfer=bukti_transfer)
        if bukti_transfer:
            pembayaran.bukti_transfer.save(bukti_transfer.name, bukti_transfer, save=True)
        pembayaran.save()
        messages.success(request, 'Pembayaran berhasil diajukan silahkan tunggu konfirmasi.')
        return redirect('status')
    return render(request, 'pendaftaran/pembayaran.html')

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def status(request):
    pembayaran = Pembayaran.objects.filter(user=request.user).first()
    return render(request, 'pendaftaran/status.html', {'pembayaran': pembayaran})


def logoutuser(request):
    # Logout pengguna
    logout(request)
    request.session.clear()
    messages.success(request, 'Anda telah berhasil logout.')
    # Redirect ke halaman login
    return redirect('login')


