from django.db import models
from murid.models import Murid
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if User.objects.filter(email=extra_fields.get('email')).exists():
        # Email sudah digunakan, tampilkan pesan error atau ambil tindakan yang sesuai
            print("Email sudah digunakan.")
            return None
        # Normalisasi username
        username = self.normalize_email(username)
        # Buat instance User baru
        user = self.model(username=username, **extra_fields)
        # Set password
        user.set_password(password)
        # Simpan user ke database
        user.save(using=self._db)
        return user
    
    def create_guru(self, username, password=None, **extra_fields):
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.role = 'Guru'
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        # Buat user biasa dengan metode create_user
        user = self.create_user(username, password, **extra_fields)
        # Set atribut is_staff dan is_superuser menjadi True
        user.is_staff = True
        user.is_superuser = True
        user.role = 'Admin' 
        # Simpan perubahan pada user
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GURU_ROLE = 'Guru'
    USER_ROLE = 'User'
    ADMIN_ROLE = 'Admin'
    ROLE_CHOICES = [
        (USER_ROLE, 'User'),
        (ADMIN_ROLE, 'Admin'),
        (GURU_ROLE, 'Guru'),
    ]
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    confirm_password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER_ROLE)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = "pengguna"

    def is_admin(self):
        return self.role == self.ADMIN_ROLE
    
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.role == self.ADMIN_ROLE

    def has_module_perms(self, app_label):
        return self.role == self.ADMIN_ROLE



# class User(models.Model):
#   nisn=models.CharField(max_length=15)
#   email=models.EmailField(null=False)
#   password=models.CharField(max_length=200)
#   confirm_password=models.CharField(null=False,max_length=200)

#   class Meta:
#     db_table = "pengguna"

class Pembayaran(models.Model):
    STATUS_CHOICES = (
        ('Menunggu', 'Menunggu'),
        ('Disetujui', 'Disetujui'),
        ('Ditolak', 'Ditolak'),
    )
    id_pembayaran = models.CharField(primary_key=True, max_length=10, editable=False)
    token_pembayaran= models.CharField(max_length=50, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    murid = models.ForeignKey(Murid, on_delete=models.CASCADE, null=True)
    nama = models.CharField(max_length=255)
    jenis_bank = models.CharField(max_length=255)
    bukti_transfer = models.FileField(upload_to='bukti_transfer/')
    status_pembayaran = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Menunggu')
    tanggal_pembayaran = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_pembayaran

    def generate_id_pembayaran(self, instance):
        last_id_pembayaran = Pembayaran.objects.order_by('-id_pembayaran').first()

        if last_id_pembayaran and last_id_pembayaran.id_pembayaran:
            last_id_number = int(last_id_pembayaran.id_pembayaran[1:])
        else:
            last_id_number = 0

        new_id_number = last_id_number + 1
        new_id_pembayaran = f"B{new_id_number:05}"

        return new_id_pembayaran


    def save(self, *args, **kwargs):
        if not self.id_pembayaran:
            self.id_pembayaran = self.generate_id_pembayaran(instance=self)
        super().save(*args, **kwargs)
            
    class Meta:
        db_table = "pembayaran"



    # def save(self, *args, **kwargs):
    #     last_id = Pembayaran.objects.order_by('-id_pembayaran').first()
    #     if last_id and last_id.id_pembayaran:
    #         last_id_number = int(last_id.id_pembayaran[1:])
    #         new_id_number = last_id_number + 1
    #         new_id_string = 'P' + str(new_id_number).zfill(3)
    #         self.id_pembayaran = new_id_string
    #     else:
    #         self.id_pembayaran = 'P001'
    #     super().save(*args, **kwargs)


class Guru(models.Model):
    nip = models.CharField(null=False, max_length=15)
    nama = models.CharField(null=False, max_length=30)
    alamat = models.CharField(null=False, max_length=40)
    no_handphone = models.CharField(null=False, max_length=15)

    class Meta:
        db_table = "guruu"  # Ubah nama tabel menjadi "guruu"

