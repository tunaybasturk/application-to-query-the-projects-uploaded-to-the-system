from os import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.login,name='login'),
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('dashboard/upload/',views.upload,name='upload'),
    path('yonetici_giris/',views.yonetici_giris,name='yonetici_giris'),
    path('yonetici/',views.yonetici,name='yonetici'),
    path('sorgu/',views.admin_sorgu,name="admin_sorgu"),
    path('sorgu1/',views.sorgu1,name="sorgu1"),
    path('kullanıcı_sorgu/',views.kullanıcı_sorgu,name="kullanıcı_sorgu"),
    path('kullanıcı_sorgu1/',views.kullanıcı_sorgu1,name="kullanıcı_sorgu1")

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)