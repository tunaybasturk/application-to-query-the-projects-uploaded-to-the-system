from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, FilePathField


class kullanıcı(models.Model):
    username=CharField(max_length=40)
    password=CharField(max_length=40)
    super_user=CharField(max_length=40)
    def __str__(self):
        return self.username

class File(models.Model):
    name= models.CharField(max_length=500)
    filepath= models.FileField( null=True, verbose_name="")
    user_id=models.IntegerField()

    def __str__(self):
        return self.name + ": " + str(self.filepath)

class content(models.Model):
    yazar_adı=models.CharField(max_length=50)
    yazar_soyadı=models.CharField(max_length=50)
    ogrenci_numarası=models.CharField(max_length=50)
    ogretim_turu=models.CharField(max_length=50)
    ders_adı=models.CharField(max_length=50)
    proje_özeti=models.CharField(max_length=5000)
    teslim_tarihi=models.CharField(max_length=50)
    proje_başlığı=models.CharField(max_length=50)
    danışman_adı=models.CharField(max_length=50)
    danışman_soyadı=models.CharField(max_length=50)
    danışman_ünvan=models.CharField(max_length=50)
    jüri_ad=models.CharField(max_length=50)
    jüri_soyad=models.CharField(max_length=50)
    jüri_ünvan=models.CharField(max_length=50)
    filepath=models.FileField( null=True, verbose_name="")
    file_id=models.CharField(max_length=50)
    user_id=models.CharField(max_length=50)
    
    def __str__(self):
        return self.yazar_adı

class yazar(models.Model):
    yazar_ad=models.CharField(max_length=50)
    yazar_soyad=models.CharField(max_length=50)
    yazar_ad_soyad=models.CharField(max_length=50)
    öğrenci_numarası=models.CharField(max_length=50)
    öğretim_türü=models.CharField(max_length=50)
    filepath=models.CharField(max_length=50)
    file_id=models.CharField(max_length=50)
    kullanıcı_id=models.CharField(max_length=50)


class anahtar_kelime(models.Model):
    anahtar_kelime=models.CharField(max_length=50)
    filepath=models.CharField(max_length=50)
    file_id=models.CharField(max_length=50)
    kullanıcı_id=models.CharField(max_length=50)

class juri(models.Model):
    jüri_ad=models.CharField(max_length=50)
    jüri_soyad=models.CharField(max_length=50)
    jüri_ünvan=models.CharField(max_length=50)
    file_id=models.CharField(max_length=50)
    filepath=models.CharField(max_length=50)
    kullanıcı_id=models.CharField(max_length=50)


class danışman(models.Model):
    danışman_ad=models.CharField(max_length=50)
    danışman_soyad=models.CharField(max_length=50)
    danışman_ünvan=models.CharField(max_length=50)
    file_id=models.CharField(max_length=50)
    filepath=models.CharField(max_length=50)
    kullanıcı_id=models.CharField(max_length=50)