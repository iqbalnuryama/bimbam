from django.db import models
from user.models import User, Murid
from django.utils import timezone



class Berita(models.Model):
  judul =models.CharField(null=True, max_length=100)
  deskripsi =models.TextField(null=True)
  foto_berita = models.FileField(upload_to='berita/', null=True)
  tanggal_upload = models.DateTimeField(null=True, default=timezone.now)

  class Meta:
    db_table = "berita"

class Kegiatan(models.Model):
  judul =models.CharField(null=True, max_length=100)
  deskripsi =models.TextField(null=True)
  foto_kegiatan = models.FileField(upload_to='kegiatan/', null=True)
  tanggal_upload = models.DateTimeField(null=True, default=timezone.now)

  class Meta:
    db_table = "kegiatan"

from django.db import models


class Pengetesan(models.Model):
    MATERI_CHOICES = [
        ('Membaca', 'Membaca'),
        ('Menulis', 'Menulis'),
        ('Menghitung', 'Menghitung'),
    ]
    TINGKAT_CHOICES = [
        ('Tingkat 1', 'Tingkat 1'),
        ('Tingkat 2', 'Tingkat 2'),
        ('Tingkat 3', 'Tingkat 3'),
    ]
    tingkat = models.CharField(max_length=255, choices=TINGKAT_CHOICES)
    materi = models.CharField(max_length=255, choices=MATERI_CHOICES)
    judul = models.CharField(max_length=100)
    url = models.URLField()
    
    class Meta:
        db_table = "pengetesan"


class Video(models.Model):
    MATERI_CHOICES = [
        ('Membaca Tingkat 1', 'Membaca Tingkat 1'),
        ('Membaca Tingkat 2', 'Membaca Tingkat 2'),
        ('Membaca Tingkat 3', 'Membaca Tingkat 3'),
        ('Menulis Tingkat 1', 'Menulis Tingkat 1'),
        ('Menulis Tingkat 2', 'Menulis Tingkat 2'),
        ('Menulis Tingkat 3', 'Menulis Tingkat 3'),
        ('Menghitung Tingkat 1', 'Menghitung Tingkat 1'),
        ('Menghitung Tingkat 2', 'Menghitung Tingkat 2'),
        ('Menghitung Tingkat 3', 'Menghitung Tingkat 3'),
    ]
    materi = models.CharField(max_length=255, choices=MATERI_CHOICES)
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    file_video = models.FileField(upload_to='videos/')

    class Meta:
        db_table = "materi_video"

    def __str__(self):
        return self.judul
    
class Modul(models.Model):
    MATERI_CHOICES = [
        ('Membaca Tingkat 1', 'Membaca Tingkat 1'),
        ('Membaca Tingkat 2', 'Membaca Tingkat 2'),
        ('Membaca Tingkat 3', 'Membaca Tingkat 3'),
        ('Menulis Tingkat 1', 'Menulis Tingkat 1'),
        ('Menulis Tingkat 2', 'Menulis Tingkat 2'),
        ('Menulis Tingkat 3', 'Menulis Tingkat 3'),
        ('Menghitung Tingkat 1', 'Menghitung Tingkat 1'),
        ('Menghitung Tingkat 2', 'Menghitung Tingkat 2'),
        ('Menghitung Tingkat 3', 'Menghitung Tingkat 3'),
    ]
    materi = models.CharField(max_length=255, choices=MATERI_CHOICES)
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    file_modul = models.FileField(upload_to='modul/')

    class Meta:
        db_table = "materi_modul"  

    def __str__(self):
        return self.judul
    
class Pengajuan(models.Model):
    STATUS_CHOICES = [
        ('Menunggu Penilaian', 'Menunggu Penilaian'),
        ('Disetujui', 'Disetujui'),
        ('Ditolak', 'Ditolak'),
    ]
    
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Menunggu Penilaian')
    murid = models.ForeignKey(Murid, on_delete=models.CASCADE)
    pengetesan = models.ForeignKey(Pengetesan, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_bukti = models.FileField(upload_to='pengajuan/')


    class Meta:
        db_table = "pengajuan"

