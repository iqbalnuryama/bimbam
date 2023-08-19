from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout,authenticate, login as login_auth, get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from murid.models import Murid
from django.db.models import Sum
from user.models import User, Pembayaran, Guru
from django.urls import reverse
from django.template.loader import get_template
from django.conf import settings
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tables import CellStyle

def is_user(user):
    return user.role == User.ADMIN_ROLE

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def admin(request):
    murid = Murid.objects.all()
    guru = Guru.objects.all()
    users = User.objects.all()
    transaksi = Pembayaran.objects.all()
    return render(request, 'admin.html', {
        'murid':murid,
        'guru':guru,
        'users':users,
        'transaksi': transaksi,
        })


# Murid Open
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def murid(request):
    murid = Murid.objects.all()
    return render(request, 'kelolamurid.html', {'murid':murid})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tambahmurid(request):
    if request.method=='POST':
        nama=request.POST['name']
        jenis_kelamin=request.POST['jk']
        tempat_lahir=request.POST['teml']
        tanggal_lahir=request.POST['tl']
        anak_ke=request.POST['anak']
        agama=request.POST['agama']
        alamat=request.POST['alamat']
        nama_ayah=request.POST['na']
        nama_ibu=request.POST['ni']
        no_handphone=request.POST['nohp']
        murid = Murid(nama=nama,jenis_kelamin=jenis_kelamin,tempat_lahir=tempat_lahir,tanggal_lahir=tanggal_lahir,anak_ke=anak_ke,agama=agama,alamat=alamat,nama_ayah=nama_ayah,nama_ibu=nama_ibu,no_handphone=no_handphone)
        murid.save()
        return redirect('murid')
    else:    
        return render(request,'murid/tambahmurid.html')
    
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def edit(request, id):  
    murid_edit = Murid.objects.get(id=id) 
    return render(request,'murid/editmurid.html', {'murid':murid_edit})  

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def update_murid(request, id):
    murid = get_object_or_404(Murid, id=id)
    if request.method == 'POST':
        murid.nama = request.POST['name']
        murid.jenis_kelamin = request.POST['jk']
        murid.tempat_lahir = request.POST['teml']
        murid.anak_ke = request.POST['anak']
        murid.tanggal_lahir = request.POST['tl']
        murid.agama = request.POST['agama']
        murid.alamat = request.POST['alamat']
        murid.nama_ayah = request.POST['na']
        murid.nama_ibu = request.POST['ni']
        murid.no_handphone = request.POST['nohp']
        murid.save()
        messages.success(request,"Data Berhasil Diubah")
        return redirect('/murid')
    
    return render(request, 'murid/editmurid.html', {'murid': murid})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def destroymurid(request, id):
    if request.method=='POST':  
        murid = Murid.objects.get(id=id) 
        murid.delete()
    return redirect("/murid")
# Murid Close

# Guru Open
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def guruku(request):
    guru = Guru.objects.all()
    return render(request, 'kelolaguru.html',{'guru':guru})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tambahguru(request):
    if request.method=='POST':
        nip=request.POST['nip']
        nama=request.POST['nama']
        alamat=request.POST['alamat_guru']
        no_handphone=request.POST['nohp_guru']
        guru = Guru(nip=nip, nama=nama, alamat=alamat, no_handphone=no_handphone)
        guru.save()
        messages.success(request,"Data Ditambahkan")
        return redirect('guru')
    else:    
        return render(request,'guru/tambahguru.html')
    
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def editguru(request, id):
    guruku = Guru.objects.get(id=id)
    return render (request, 'guru/editguru.html', {'guru':guruku})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def updateguru(request, id):
    guru = get_object_or_404(Guru, id=id)
    if request.method=='POST':
        guru.nip=request.POST['nip']
        guru.alamat=request.POST['alamat_guru']
        guru.no_handphone=request.POST['nohp_guru']
        guru.nama=request.POST['nama']
        guru.save()
        messages.success(request,"Data Berhasil Diubah")
        return redirect('/guru') 
    
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def hapusguru(request,id):
    if request.method=='POST':  
        guru = Guru.objects.get(id=id) 
        guru.delete()
    return redirect ('/guru')
# Guru Close

# User Open
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def user(request):
    user = User.objects.all()
    return render(request, 'kelolauser.html', {'user':user})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def tambahuser(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['pass']
        role =request.POST['role']
        hashed_password = make_password(password)
        guru = User(username=username, email=email, password=hashed_password, role=role)
        guru.save()
        messages.success(request,"Data Ditambahkan")
        return redirect('/user')
    else:    
        return render(request,'user/tambahuser.html')
    

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def edituser(request, id):
    user = User.objects.get(id=id)
    return render (request, 'user/edituser.html', {'user':user})

@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def updateuser(request, id):
    user = get_object_or_404(User, id=id)
    if request.method=='POST':
        user.nisn=request.POST['nisn']
        user.email=request.POST['email']
        password=request.POST['password']
        hashed_password = make_password(password)
        user.password = hashed_password
        user.save()
        return redirect('/user')
    
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def hapususer(request,id):
    if request.method=='POST':  
        user = User.objects.get(id=id) 
        user.delete()
    return redirect ('/user')
    
# User Close

# Pembayaran Open
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def transaksi(request):
    transaksi = Pembayaran.objects.all()[::-1]
    user = User.objects.all()
    return render(request, 'kelolatransaksi.html', {'transaksi': transaksi, 'user':user})


def setuju(request, id_pembayaran):
    pembayaran = get_object_or_404(Pembayaran, id_pembayaran=id_pembayaran)

    if pembayaran.status_pembayaran == 'Menunggu':
        # Setujui pembayaran
        pembayaran.status_pembayaran = 'Disetujui'
        pembayaran.save()

    elif pembayaran.status_pembayaran == 'Ditolak':
        # Tolak pembayaran
        pembayaran.status_pembayaran = 'Disetujui'
        pembayaran.save()

    return redirect('transaksi')

def tolak(request, id_pembayaran):
    pembayaran = get_object_or_404(Pembayaran, id_pembayaran=id_pembayaran)

    if pembayaran.status_pembayaran == 'Menunggu':
        # Tolak pembayaran
        pembayaran.status_pembayaran = 'Ditolak'
        pembayaran.save()
        
    elif pembayaran.status_pembayaran == 'Disetujui':
        # Tolak pembayaran
        pembayaran.status_pembayaran = 'Ditolak'
        pembayaran.save()
        messages.error(request, 'Pembayaran Anda ditolak. Silahkan ulang pembayaran.')
    return redirect('transaksi')

def hapuspembayaran(request,id):
    if request.method=='POST':  
        user = User.objects.get(id=id) 
        user.delete()
    return redirect ('/user')
# Pembayaran Close


# Laporan
@login_required(login_url=settings.LOGIN_URL)
@user_passes_test(is_user)
def laporan(request):
    transaksi = Pembayaran.objects.all()
    return render(request, 'laporan.html', {'transaksi': transaksi})

def generate_laporan(request):
    # Retrieve data transaksi dari database
    transaksi = Pembayaran.objects.all()  # Ubah dengan query sesuai dengan model dan data transaksi Anda

    # Buat objek buffer untuk menyimpan PDF
    buffer = BytesIO()

    # Buat objek dokumen PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # Buat konten laporan
    report_title = 'Laporan Transaksi'
    table_header = ['ID Pembayaran', 'Nama Pengirim', 'Email', 'Jenis Bank', 'Status Pembayaran']

    # Buat data transaksi sebagai list 2D
    data = []
    data.append(table_header)
    for pembayaran in transaksi:
        row = [str(pembayaran.id_pembayaran), pembayaran.nama, pembayaran.user.email, pembayaran.jenis_bank, pembayaran.status_pembayaran]
        data.append(row)

    # Buat objek tabel dengan data transaksi
    table = Table(data)

    # Atur gaya tabel
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Tambahkan objek tabel ke elemen dokumen
    elements.append(table)

    # Membuat laporan dengan elemen yang ditambahkan
    doc.build(elements)

    # Mengambil nilai buffer PDF dan merespon dengan file PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="laporan_transaksi.pdf"'
    return response
# Laporan Close