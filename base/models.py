from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from month.models import MonthField

    
class User(AbstractUser):
    nama = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    brand = models.CharField(max_length=200, null=True)
    tgl_masuk = models.DateTimeField(null=True)
    hari_ini = models.DateTimeField(auto_now=True)
    nilai_pengetahuan_produk = models.DecimalField(null=True, blank=False, max_digits=7, decimal_places=4)
    deskripsi_pengetahuan_produk = models.CharField(max_length=200, null=True, blank=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
    def __str__(self):
        return f'{self.nama}'

class Penilaian(models.Model):
    nama = models.ForeignKey(User, on_delete=models.CASCADE)
    nilai_performa_penjualan = models.DecimalField(null=True, blank=False, max_digits=10,decimal_places=4)
    nilai_pengetahuan_produk = models.DecimalField(null=True, blank=False, max_digits=10, decimal_places=4)
    nilai_disiplin = models.DecimalField(null=True, blank=False, max_digits=10, decimal_places=4)
    nilai_kehadiran = models.DecimalField(null=True, blank=False, max_digits=10, decimal_places=4)
    nilai_masa_kerja = models.DecimalField(null=True, blank=False, max_digits=10, decimal_places=4)
    bulan_penilaian = MonthField("Month Value", help_text="some help...", default='2023-05')
    def __str__(self):
        return f'{self.nama} {self.nilai_performa_penjualan} {self.nilai_pengetahuan_produk} {self.nilai_disiplin} {self.nilai_kehadiran} {self.nilai_masa_kerja}'
    

class Kehadiran(models.Model):
    nama = models.ForeignKey(User, on_delete=models.CASCADE)
    hari_masuk = models.IntegerField(null=True, blank=False)
    banyak_hari = models.IntegerField(null=True, blank=False)
    bulan_kehadiran = MonthField("Month Value", help_text="some help...", default='2023-05')
    hari_libur = models.IntegerField(null=True, blank=False)
    hari_cuti = models.IntegerField(null=True, blank=False)
    def __str__(self):
        return f'{self.nama} {self.banyak_hari}'


class Disiplin(models.Model):
    nama = models.ForeignKey(User, on_delete=models.CASCADE)
    kuota_disiplin = models.IntegerField(null=True, blank=False)
    nilai_pelanggaran = models.IntegerField(null=True, blank=False)
    bulan_disiplin = MonthField("Month Value", help_text="some help...", default='2023-05')
    deskripsi = models.TextField(null=True, blank=True)
    def __str__(self):
        return f'{self.nama}{self.kuota_disiplin}{self.nilai_pelanggaran}{self.deskripsi}'
    
class Performa_Penjualan(models.Model):
    nama = models.ForeignKey(User, on_delete=models.CASCADE)
    jual_brands = models.IntegerField(null=True, blank=False)
    jual_brands_lain = models.IntegerField(null=True, blank=False)
    bulan_performa_penjualan = MonthField("Month Value", help_text="some help...", default='2023-05')
    def __str__(self):
        return f'{self.nama}{self.jual_brands}{self.jual_brands_lain}'


class Nilai_Ahp(models.Model):
    id = models.AutoField(primary_key=True)
    nama_kriteria = models.CharField(null=True, blank=True, max_length=200)
    value_kriteria = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=8)

    def __str__(self):
        return f'{self.nama_kriteria}{self.value_kriteria}'


# class Komparasi_Ahp(models.Model):
#     id = models.AutoField(primary_key=True)
#     nama_kriteria = models.CharField(null=True, blank=False)
#     value_kriteria = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=4)

#     def __str__(self):
#         return f'{self.nama_kriteria}{self.value_kriteria}'


     
    
 
 
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class Normalisasi(models.Model):
    no_field = models.DecimalField(db_column='No.', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    nama = models.CharField(blank=True, null=True, max_length=200)
    nilai_kehadiran = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_performa_penjualan = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_disiplin = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_masa_kerja = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_pengetahuan_produk = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'normalisasi'
class BobotNormalisasi(models.Model):
    no_field = models.DecimalField(db_column='No.', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    nama = models.CharField(blank=True, null=True, max_length=200)
    nilai_kehadiran = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_performa_penjualan = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_disiplin = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_masa_kerja = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_pengetahuan_produk = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bobot_normalisasi'
        
class BobotIdeal(models.Model):
    no_field = models.DecimalField(db_column='No.', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    # Field name made lowercase.
    nama = models.CharField(db_column='Nama', blank=True,
                            null=True, max_length=200)
    nilai_ideal_positif = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_ideal_negatif = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bobot_ideal'


class PerhitunganDistanceIdeal(models.Model):
    no_field = models.DecimalField(db_column='No.', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    nama = models.CharField(blank=True, null=True, max_length=200)
    nilai_ideal_positif = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_ideal_negatif = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'perhitungan_distance_ideal'


class BobotPreferensi(models.Model):
    no_field = models.DecimalField(db_column='No.', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    nama = models.CharField(blank=True, null=True, max_length=200)
    bobo_preferensi = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bobot_preferensi'






class Perangkingan(models.Model):
    no_field = models.DecimalField(db_column='No.', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    nama = models.CharField(blank=True, null=True, max_length=200)
    hasil = models.DecimalField(db_column='Hasil', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ranking = models.DecimalField(db_column='Ranking', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'perangkingan'



class BobotKriteriaAhp(models.Model):
    nomor = models.CharField(blank=True, null=True, max_length=200)
    nilai_performa_penjualan = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_pengetahuan_produk = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_disiplin = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_kehadiran = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_masa_kerja = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bobot_kriteria_ahp'





class EigenVektorAhp(models.Model):
    nomor = models.CharField(blank=True, null=True, max_length=200)
    nilai_performa_penjualan = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_pengetahuan_produk = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_disiplin = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_kehadiran = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nilai_masa_kerja = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    jumlah = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rata_rata = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eigen_vektor_ahp'


class KonsistensiAhp(models.Model):
    nama_perhitungan = models.CharField(blank=True, null=True, max_length=200)
    perhitungan = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'konsistensi_ahp'


class KriteriaAhp(models.Model):
    nomor = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    prioritas_kriteria = models.CharField(blank=True, null=True, max_length=200)
    kriteria = models.CharField(blank=True, null=True, max_length=200)
    tingkat_kepentingan = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kriteria_ahp'

