# Generated by Django 3.2.9 on 2021-12-18 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_kullanıcı_super_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yazar_adı', models.CharField(max_length=50)),
                ('yazar_soyadı', models.CharField(max_length=50)),
                ('ogrenci_numarası', models.CharField(max_length=50)),
                ('ogretim_turu', models.CharField(max_length=50)),
                ('ders_adı', models.CharField(max_length=50)),
                ('proje_özeti', models.CharField(max_length=5000)),
                ('teslim_tarihi', models.CharField(max_length=50)),
                ('proje_başlığı', models.CharField(max_length=50)),
                ('danışman_adı', models.CharField(max_length=50)),
                ('danışman_soyadı', models.CharField(max_length=50)),
                ('danışman_ünvan', models.CharField(max_length=50)),
                ('jüri_ad', models.CharField(max_length=50)),
                ('jüri_soyad', models.CharField(max_length=50)),
                ('jüri_ünvan', models.CharField(max_length=50)),
                ('file_id', models.CharField(max_length=50)),
                ('user_id', models.CharField(max_length=50)),
            ],
        ),
    ]
