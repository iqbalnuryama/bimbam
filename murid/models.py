from django.db import models


class Murid(models.Model):
  MEMBACA_CHOICES = (
    ('Membaca Tingkat 1', 'Membaca Tingkat 1'),
    ('Membaca Tingkat 2', 'Membaca Tingkat 2'),
    ('Membaca Tingkat 3', 'Membaca Tingkat 3'),
)
  MENULIS_CHOICES =(
    ('Menulis Tingkat 1', 'Menulis Tingkat 1'),
    ('Menulis Tingkat 2', 'Menulis Tingkat 2'),
    ('Menulis Tingkat 3', 'Menulis Tingkat 3'),
  )
  MENGHITUNG_CHOICES =(
    ('Menghitung Tingkat 1', 'Menghitung Tingkat 1'),
    ('Menghitung Tingkat 2', 'Menghitung Tingkat 2'),
    ('Menghitung Tingkat 3', 'Menghitung Tingkat 3'),
  )

  membaca = models.CharField(max_length=50, choices=MEMBACA_CHOICES, default='Membaca Tingkat 1')
  menghitung = models.CharField(max_length=50, choices=MENGHITUNG_CHOICES, default='Menghitung Tingkat 1')
  menulis = models.CharField(max_length=50, choices=MENULIS_CHOICES, default='Menulis Tingkat 1')
  user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='murid', null=True)
  nama=models.CharField(null=False, max_length=30)
  jenis_kelamin=models.CharField(null=False, max_length=10)
  tempat_lahir=models.CharField(null=False, max_length=20)
  tanggal_lahir=models.DateField(null=False)
  anak_ke=models.CharField(null=False, max_length=15)
  agama=models.CharField(null=False, max_length=15)
  alamat=models.CharField(null=False, max_length=40)
  nama_ayah=models.CharField(null=False, max_length=30)
  nama_ibu=models.CharField(null=False, max_length=30)
  no_handphone=models.CharField(null=False, max_length=15)

  class Meta:
    db_table = "murid"

