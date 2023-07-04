"""
URL configuration for percobaan_0 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home1, name='home1'),
    path('perhitungan/', views.perhitungan, name='perhitungan'),
    path('perhitungan_wp/', views.perhitungan_wp, name='perhitungan_wp'),
    path('perhitungan_saw/', views.perhitungan_saw, name='perhitungan_saw'),
    
    path('datakaryawan/', views.karyawan, name='data_karyawan'),
    path('tambahkaryawan/', views.tambahkaryawan, name='tambah_karyawan'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name="logout"),
    path('hapuskaryawan/<str:pk>', views.hapuskaryawan, name="hapuskaryawan"),
    path('profilkaryawan/<str:pk>/', views.profilkaryawan, name='profil_karyawan'),
    path('ubahkaryawan/<str:pk>/', views.ubahkaryawan, name='ubahkaryawan'),
    path('ubahprofil/', views.ubahprofil, name='ubahprofil'),
    path('disiplin/', views.disiplin, name='disiplin'),
    path('ubahdisiplin/<str:pk>/', views.ubahdisiplin, name='ubahdisiplin'),
    path('kehadiran/', views.kehadiran, name='kehadiran'),
    path('ubahkehadiran/<str:pk>/', views.ubahkehadiran, name='ubahkehadiran'),
    
    path('performapenjualan/', views.performa_penjualan, name='performapenjualan'),
    path('ubahperformapenjualan/<str:pk>/', views.ubahperforma_penjualan, name='ubahperformapenjualan'),
    
    path('ahp/', views.show_ahp, name='nilai_ahp'),
    path('ahp/perhitungan_ahp', views.perhitungan_ahp, name='perhitungan_ahp'),
    
    
    
]
