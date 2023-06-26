from django.shortcuts import render, redirect
from .models import User, Penilaian, Nilai_Ahp, Normalisasi, BobotNormalisasi, BobotPreferensi, PerhitunganDistanceIdeal, Perangkingan, BobotIdeal, Disiplin, Kehadiran, Performa_Penjualan, BobotKriteriaAhp, KriteriaAhp, EigenVektorAhp, KonsistensiAhp
from .forms import MyUserCreation, UserChange, DisiplinChange, KehadiranChange, PerformaPenjualanChange, AhpForm, PerbandinganAhpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.db import models
import math
import decimal
from django.db.models import DecimalField
from django import forms
from statistics import mean
from django.db.models import Q

@login_required(login_url='login')
def home(request):
    page = 'home'
    penilaian = Penilaian.objects.all() 
    if Nilai_Ahp.objects.exclude(nama_kriteria__isnull=False).exists():
        nilai_ahp_ada = 'No'
    elif Nilai_Ahp.objects.exclude(value_kriteria__isnull=False).exists():
        nilai_ahp_ada = 'No'
    elif Nilai_Ahp.objects.exists():
        nilai_ahp_ada = 'Yes'
    else:
        nilai_ahp_ada = 'No'
    context = {
        'penilaian': penilaian,
        'nilai_ahp_ada': nilai_ahp_ada,
        'page': page
    }
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def show_ahp(request):
    nilai_ahp = Nilai_Ahp.objects.all()
    page = 'ahp'
    if Nilai_Ahp.objects.count() < 3:
        nilai_ahp_ada = 'No'

    elif Nilai_Ahp.objects.exists():
        nilai_ahp_ada = 'Yes'
    else:
        nilai_ahp_ada = 'No'
    if request.method == "POST":
        form = AhpForm(request.POST)
        if form.is_valid():
            Nilai_Ahp.objects.all().delete()
            for field_name, checked in form.cleaned_data.items():
                if checked:
                    checked_score = Nilai_Ahp(nama_kriteria=field_name)
                    checked_score.save()
            return redirect('nilai_ahp')
    else:
        form = AhpForm()
    
    context = {
        'nilai_ahp': nilai_ahp,
        'page': page,
        'form': form,
        'nilai_ahp_ada': nilai_ahp_ada
    }
    return render(request, 'base/ahp.html', context)


@login_required(login_url='login')
def perhitungan_ahp(request):
    page = 'ahp'
    if request.method == "POST":
        form = PerbandinganAhpForm(request.POST)
        if form.is_valid():
            # Create a nested dictionary with field names as keys
            pilihan_kriteria = [obj.nama_kriteria for obj in Nilai_Ahp.objects.all()]
            data = {score: {} for score in pilihan_kriteria}
            for score_pair, pilihan_kepentingan in form.cleaned_data.items():
                score1, score2 = score_pair.split('/')
                data[score2][score1] = float(pilihan_kepentingan)
                data[score1][score2] = 1 / float(pilihan_kepentingan)

            # Add the diagonal elements
            for score in pilihan_kriteria:
                data[score][score] = 1.0

            # Create a DataFrame from the nested dictionary
            df = pd.DataFrame(data)
            df1 = pd.DataFrame(data)
            df = df.reindex(df.columns, axis=0)
            df1 = df1.reindex(df.columns, axis=0)
            df = df.to_html(classes="table table-borderless datatable")
            
            # Sum Column
            ef1_square = list()
            for i in range(len(df1.columns.values)):
                ef1_square.append(sum(df1[df1.columns.values[i]]))
            df2_square = pd.DataFrame([ef1_square], columns=df1.columns)
            ef = df1.append(df2_square, ignore_index=True)
            ef = df1.to_html(classes="table table-borderless datatable")
            # Sum Column End
            
            # Eigen Vektor 1
            ef1 = df1.copy()
            ef2 = df1.copy()
            for i in range(len(df1)):
                for j in range(len(df1)):
                    ef1.iloc[j, i] = df1.iloc[j, i] / ef1_square[i]
                    ef2.iloc[j, i] = df1.iloc[j, i] / ef1_square[i]
            ef1 = ef1.to_html(classes="table table-borderless datatable")
                
            # Eigen Vektor 1 End
            
            # Eigen Vektor 2
            f_square = list()
            f_square1 = list()
            for i in range(len(df1)):
                f_square.append(sum(ef2.iloc[i]))
                f_square1.append(mean(ef2.iloc[i]))

            ff = ef2.copy()
            ff['total'] = f_square
            ff['rata_rata'] = f_square1
            
            f_square2 = list()
            for i in range(len(ff.columns.values)):
                f_square2.append(sum(ff[ff.columns.values[i]]))
            f_square3 = pd.DataFrame([f_square2], columns=ff.columns)
            ff = ff.append(f_square3, ignore_index=True)
            ff = ff.to_html(classes="table table-borderless datatable")
            
            ff1 = ef2.copy()
            ff1['total'] = f_square
            ff1['rata_rata'] = f_square1
            # Eigen Vektor 2
            
            # Lambda, Ci, CR
            gf_square = list()
            for i in range(len(ff1['rata_rata'])):
                gf_square.append(ff1['rata_rata'][i]*ef1_square[i])
            # Lambda
            gf = sum(gf_square)
            gf = round(gf, 6)
            # CI
            hf = ((gf-len(df1))/(len(df1)-1))
            hf = round(hf, 6)
            # CR
            if len(df1) == 3:
                jf = hf/0.58
                jf = round(jf, 6)
            elif len(df1) == 4:
                jf = hf/0.90   
                jf = round(jf, 6)    
            elif len(df1) == 5:
                jf = hf/1.12   
                jf = round(jf, 6)
            elif len(df1) == 6:
                jf = hf/1.24   
                jf = round(jf, 6)
            elif len(df1) == 7:
                jf = hf/1.32   
                jf = round(jf, 6)
            elif len(df1) == 8:
                jf = hf/1.41   
                jf = round(jf, 6)
            elif len(df1) == 9:
                jf = hf/1.45   
                jf = round(jf, 6)
            elif len(df1) == 10:
                jf = hf/1.49
                jf = round(jf, 6)
            # Lambda, Ci, CR End     
            
            
            if jf <= 0.1:
                # Save into Value_kriteria       
                kf = f_square1
                
                # get the queryset for the rows you want to update
                nilai_kriteria = Nilai_Ahp.objects.all()

                # prepare the models for update
                for y, z in zip(nilai_kriteria, kf):
                    y.value_kriteria = z

                # bulk update the queryset
                Nilai_Ahp.objects.bulk_update(nilai_kriteria, ['value_kriteria'])



            
            
            # reorder rows to match column order

    else:
        form = PerbandinganAhpForm()
        df = 'Belum ada'
        ef = 'Belum ada'
        ef1 = 'Belum Ada'
        ff = 'ff',
        gf = 'gf',
        hf = 'hf',
        jf = 'jf',


    context = {
        'page': page,
        'form': form,
        'df': df,
        'ef': ef,
        'ef1': ef1,
        'ff': ff,
        'gf': gf,
        'hf': hf,
        'jf': jf,

    }
    return render(request, 'base/perhitungan_ahp.html', context)

@login_required(login_url='login')
def home1(request):
    page = 'home1'
    
    penilaian = Penilaian.objects.get(nama_id=request.user.id)
    kehadiran = Kehadiran.objects.get(nama_id=request.user.id)
    performa_penjualan = Performa_Penjualan.objects.get(nama_id=request.user.id)
    disiplin = Disiplin.objects.get(nama_id=request.user.id)
  
    context = {
        'penilaian': penilaian,
        'page': page,
        'kehadiran': kehadiran,
        'performa_penjualan': performa_penjualan,
        'disiplin':disiplin
        
    }
    return render(request, 'base/home1.html', context)

@login_required(login_url='login')
def perhitungan(request):


    page = 'perhitungan'
    penilaian = Penilaian.objects.all()
    # Retrieve all fields from the model
    fields = Penilaian._meta.get_fields()

    # Filter out only the decimal fields
    decimal_fields = [
        f.name for f in fields if isinstance(f, models.DecimalField)]

    # Retrieve only the decimal fields from the database
    objects = Penilaian.objects.values(*decimal_fields)

    # Convert queryset to a list, so pandas can handle it
    queryset = list(objects)

    # Convert the list to a dataframe
    pandaspd = pd.DataFrame.from_records(queryset)

    # Views Penilaian based on nama_kriteria in Nilai_Ahp
    nilai_ahps = Nilai_Ahp.objects.all()
    nilai_ahps_list = [nilai_ahp.nama_kriteria for nilai_ahp in nilai_ahps]
    filtered_scores3 = Penilaian.objects.values(*nilai_ahps_list)
    filtered_scores2 = list(filtered_scores3)
    filtered_scores = pd.DataFrame.from_records(filtered_scores2)
    filtered_scores = filtered_scores.to_html(classes="table table-condensed table-bordered table-striped table-hover", justify='left')




    # b_value = pd.DataFrame.from_records(queryset)
    # b_value1 = pd.DataFrame.from_records(queryset)
    # b_value2 = pd.DataFrame.from_records(queryset)
    # Normalisasi
    b_value = pd.DataFrame.from_records(filtered_scores2)
    b_value1 = pd.DataFrame.from_records(filtered_scores2)
    b_value2 = pd.DataFrame.from_records(filtered_scores2)
    b_square = list()
    for l in range(len(b_value.columns.values)):
        b_square.append(
            math.sqrt(sum(k**2 for k in pandaspd[pandaspd.columns.values[l]])))
    for i in range(len(b_value)):
        for j in range(len(b_value.columns.values)):
            b_value.iloc[i, j] = float(pandaspd.iloc[i, j]) / b_square[j]
            b_value1.iloc[i, j] = float(pandaspd.iloc[i, j]) / b_square[j]
            b_value2.iloc[i, j] = float(pandaspd.iloc[i, j]) / b_square[j]

    b_value = b_value.to_html(
        classes="table table-condensed table-bordered table-striped table-hover", justify='left')
    # Normalisasi Selesai

    # Normalisasi Terbobot
    scoreses = Nilai_Ahp.objects.all()
    #score_dict = {scorese.nama_kriteria: scorese.value_kriteria for scorese in scoreses}
    
    
    c_value = b_value1
    c_value1 = b_value2
    # c_square = {'nilai_performa_penjualan': 0.439605556,
    #             'nilai_pengetahuan_produk': 0.235712674,
    #             'nilai_disiplin': 0.151422771,
    #             'nilai_kehadiran': 0.0866295,
    #             'nilai_masa_kerja': 0.0866295
    #             }
    c_square = {scorese.nama_kriteria: float(scorese.value_kriteria) for scorese in scoreses}

    for i in range(len(c_value)):
        for j in range(len(c_value.columns.values)):
            c_value.iloc[i, j] = float(
                c_value.iloc[i, j]) * c_square[c_value.columns.values[j]]
            c_value1.iloc[i, j] = float(
                c_value1.iloc[i, j]) * c_square[c_value1.columns.values[j]]
    c_value = c_value.to_html(
        classes="table table-condensed table-bordered table-striped table-hover", justify='left')

    # Normalisasi Terbobot Selesai

    # Bobot Ideal
    d_square = list()
    d_square1 = list()
    d_square2 = list()
    for i in range(len(c_value1.columns.values)):
        d_square.append(c_value1.columns.values[i])
        d_square1.append(max(c_value1[c_value1.columns.values[i]]))
        d_square2.append(min(c_value1[c_value1.columns.values[i]]))

    d_square3 = pd.Series(d_square, name='nama_kriteria')
    d_square4 = pd.Series(d_square1, name='nilai_ideal_positif')
    d_square5 = pd.Series(d_square2, name='nilai_ideal_negatif')
    d_value = pd.concat([d_square3, d_square4, d_square5], axis=1)
    d_value1 = pd.concat([d_square3, d_square4, d_square5], axis=1)
    d_value = d_value.to_html(
        classes="table table-condensed table-bordered table-striped table-hover", justify='left')
    # Bobot Ideal Selesai

    # Jarak Ideal
    e_square = list()
    e_square1 = list()
    for i in range(len(c_value1)):
        timer = 0
        timer1 = 0
        for j in range(len(c_value1.columns.values)):
            perhitungan_positif = (c_value1.loc[i, c_value1.columns.values[j]] -
                                   d_value1[d_value1['nama_kriteria'] == c_value1.columns.values[j]]['nilai_ideal_positif'])**2
            perhitungan_negatif = (d_value1[d_value1['nama_kriteria'] == c_value1.columns.values[j]]
                                   ['nilai_ideal_negatif'] - c_value1.loc[i, c_value1.columns.values[j]])**2
            timer = float(timer)+float(perhitungan_positif)
            timer1 = float(timer1)+float(perhitungan_negatif)
            if j == (len(c_value1.columns.values) - 1):
                e_square.append(math.sqrt(timer))
                e_square1.append(math.sqrt(timer1))

    data_user = Penilaian.objects.values('nama_id__nama')
    data_nama = pd.DataFrame.from_records(list(data_user))
    data_nama.rename(columns={'nama_id__nama': 'nama'}, inplace=True)

    e_square3 = pd.Series(e_square, name='jarak_ideal_positif')
    e_square4 = pd.Series(e_square1, name='jarak_ideal_negatif')

    e_value = pd.concat([data_nama, e_square3, e_square4], axis=1)
    e_value1 = pd.concat([e_square3, e_square4], axis=1)
    e_value = e_value.to_html(
        classes="table table-condensed table-bordered table-striped table-hover", justify='left')
    # Jarak Ideal Selesai

    # Perhitungan Bobot Preferensi
    f_square = list()
    for i in range(len(e_value1)):
        f_square.append(
            (e_value1.iloc[i, 1]/(e_value1.iloc[i, 1]+e_value1.iloc[i, 0])))

    f_square1 = pd.Series(f_square, name='bobot_preferensi')
    f_value = pd.concat([data_nama, f_square1], axis=1)
    f_value1 = pd.concat([data_nama, f_square1], axis=1)
    # f_value['ranking'] = f_value['bobot_preferensi'].rank(method='dense', ascending=False)
    f_value = f_value.to_html(
        classes="table table-condensed table-bordered table-striped table-hover", justify='left')
    # Perhitungan Bobot Preferensi Selesai

    # Ranking
    penilaian_ranking = Penilaian.objects.values(
        'id', 'nama_id__nama', *nilai_ahps_list)
    g_square = pd.DataFrame.from_records(list(penilaian_ranking))
    g_value = pd.concat([g_square, f_square1], axis=1)

    g_value.rename(columns={'nama_id__nama': 'nama'}, inplace=True)
    g_value['ranking'] = g_value['bobot_preferensi'].rank(
        method='dense', ascending=False).round(1)

    cols = list(g_value.columns)
    # remove 'c' from the list of columns
    cols.remove('ranking')
    cols.remove('bobot_preferensi')

    # insert 'c' at the start of the list
    cols.insert(2, 'bobot_preferensi')
    cols.insert(3, 'ranking')

    # rearrange the columns
    g_value = g_value[cols]
    g_value['ranking'] = g_value['ranking'].astype(int)
    g_value = g_value.to_html(classes="table table-bordered table-striped table-hover table-condensed", justify='left')

    querypandas = pd.Series(
        pandaspd['nilai_kehadiran']*pandaspd['nilai_kehadiran'], name='Jumlah')

    data = pd.concat([pandaspd, querypandas], axis=1)
    htmlqu = data.to_html(
        classes="table table-condensed table-bordered table-striped table-hover", justify='left')
    
    # Data AHP
    data_ahp = Nilai_Ahp.objects.all().values()
    data_ahp = list(data_ahp)
    data_ahp = pd.DataFrame.from_records(data_ahp)
    data_ahp = data_ahp.to_html(
        classes="table table-condensed table-bordered table-striped table-hover", justify='left')

    context = {
        'penilaian': penilaian,
        'pandaspd': pandaspd,
        'page': page,
        'data': data,
        'querypandas': querypandas,
        'htmlqu': htmlqu,
        'b_value': b_value,
        'c_value': c_value,
        'd_value': d_value,
        'e_value': e_value,
        'f_value': f_value,
        'g_value': g_value,
        'filtered_scores': filtered_scores,
        'data_ahp': data_ahp
  
    }
    return render(request, 'base/perhitungan.html', context)

@login_required(login_url='login')
def karyawan(request):
    page = 'karyawan'
    user = User.objects.filter(brand__isnull=False).order_by('-tgl_masuk').exclude(brand='CV Bahtera Yendi Sejahtera')
    context = {
        'user': user,
        'page': page
    }
    return render(request, 'base/datakaryawan.html', context)

def logoutUser(request):
	logout(request)
	return redirect('home')

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('home')
        elif user is not None and user.is_staff == False:
            login(request, user)
            return redirect('home1')

        else:
            messages.error(request, 'Username or Password does not exists')

    context = {
        'page': page
    }
    return render(request, 'base/login.html', context)




@login_required(login_url='login')
def tambahkaryawan(request):
    page = 'karyawan'
    form = MyUserCreation()
    if request.method == 'POST':
        form = MyUserCreation(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            messages.success(request, 'Karyawan ' + user.username + ' berhasil ditambahkan')
            return redirect('data_karyawan')
        
        else:
            messages.error(request, 'An Error occured during registration')
    context = {
        'form': form,
        'page': page
    }
    return render(request, 'base/tambahkaryawan.html', context)

@login_required(login_url='login')
def profilkaryawan(request, pk):
    user = User.objects.get(id=pk)
    context = {
		'user': user
	}
    return render(request, 'base/profilkaryawan.html', context)

@login_required(login_url='login')
def ubahkaryawan(request, pk):
    page = 'ubahkaryawan'
    user = User.objects.get(id=pk)
    pengetahuan = User.objects.get(id=pk)
    form = UserChange(instance=user, initial={'password': ''})
    if request.method == 'POST':
        form = UserChange(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=False)
            user.nama = user.nama
            
            user.set_password(user.password)
            user.save()
            
            # Save into another model or table
            if user.nilai_pengetahuan_produk > 10 and user.nilai_pengetahuan_produk <= 100:
                nilai_pengetahuan = ((float(user.nilai_pengetahuan_produk)-0) / (100-0)) * (10-0) + 0
            elif user.nilai_pengetahuan_produk <= 5:
                nilai_pengetahuan = ((float(user.nilai_pengetahuan_produk)-0) / (5-0)) * (10-0) + 0
            else:
                nilai_pengetahuan = user.nilai_pengetahuan_produk
            
            user_pengetahuan = Penilaian.objects.get(nama=pengetahuan.id)
            user_pengetahuan.nilai_pengetahuan_produk = nilai_pengetahuan
            user_pengetahuan.save()
            

            messages.success(request, 'Karyawan bernama ' +
                             user.nama + ' berhasil diubah datanya')
            return redirect('data_karyawan')
    context = {
		'form': form,
        'page': page
	}
    return render(request, 'base/tambahkaryawan.html', context)

@login_required(login_url='login')
def ubahprofil(request):
    page = 'ubahprofil'
    user = request.user
    form = UserChange(instance=user, initial={'password': ''})
    if request.method == 'POST':
        form = UserChange(instance=user)
        if form.is_valid():
            form.save(commit=False)
            user.username = user.username
            user.save()
            messages.success(request, 'Berhasil Mengubah Profil ' + user.username)
            return redirect('profilkaryawan', pk=user.id)
    context = {
		'form': form,
        'page': page
	}
    return render(request, 'base/tambahkaryawan.html', context)

@login_required(login_url='login')
def hapuskaryawan(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.nama = user.nama
        user.delete()
        messages.success(request, 'Anda telah berhasil menghapus ' + user.nama)
        return redirect('data_karyawan')
    return render(request, 'base/hapus.html', {'obj': user})

@login_required(login_url='login')
def disiplin(request):
    page = 'disiplin'
    disiplin = Disiplin.objects.all()
    context = {
        'disiplin': disiplin,
        'page': page
    }
    return render(request, 'base/disiplin.html', context)

@login_required(login_url='login')
def ubahdisiplin(request, pk):
    page = 'disiplin'
    disiplin = Disiplin.objects.get(id=pk)
    form = DisiplinChange(instance=disiplin)
    if request.method == 'POST':
        form = DisiplinChange(request.POST, instance=disiplin)
        if form.is_valid():
            form.save(commit=False)
            disiplin.nama = disiplin.nama
            disiplin.kuota_disiplin = 5 - disiplin.nilai_pelanggaran
            disiplin.save()
            
            # Save into another model or table
            kuota_disiplin =  5 - disiplin.nilai_pelanggaran
            nama_disiplin = Penilaian.objects.get(nama=disiplin.nama)
            nama_disiplin.nilai_disiplin = kuota_disiplin
            nama_disiplin.save()
            
            messages.success(request, 'Karyawan bernama ' + str(disiplin.nama) + ' berhasil diubah Nilai Disiplinnya')
            return redirect('disiplin')
    context = {
		'form': form,
        'page': page
	}
    return render(request, 'base/ubahdisiplin.html', context)


@login_required(login_url='login')
def kehadiran(request):
    page = 'kehadiran'
    kehadiran = Kehadiran.objects.all()
    context = {
        'kehadiran': kehadiran,
        'page': page
    }
    return render(request, 'base/kehadiran.html', context)


@login_required(login_url='login')
def ubahkehadiran(request, pk):

    page = 'ubahkehadiran'
    kehadiran = Kehadiran.objects.get(id=pk)
    form = KehadiranChange(instance=kehadiran)
    if request.method == 'POST':
        form = KehadiranChange(request.POST, instance=kehadiran)
        if form.is_valid():
            form.save(commit=False)
            kehadiran.nama = kehadiran.nama
            kehadiran.save()
            
            # Save into another model or table
            
            nilai_kehadiran = (kehadiran.hari_masuk/kehadiran.banyak_hari) * 100
            if nilai_kehadiran < 0:
                nilai_kehadiran = 0
            elif nilai_kehadiran > 100:
                nilai_kehadiran = 100
            nama_kehadiran = Penilaian.objects.get(nama=kehadiran.nama)
            nama_kehadiran.nilai_kehadiran = nilai_kehadiran
            nama_kehadiran.save()
            
            messages.success(request, 'Karyawan bernama ' + str(kehadiran.nama) + ' berhasil diubah Nilai Kehadirannya')
            return redirect('kehadiran')
    context = {
		'form': form,
        'page': page
	}
    return render(request, 'base/ubahkehadiran.html', context)


@login_required(login_url='login')
def performa_penjualan(request):
    page = 'performa_penjualan'
    performa_penjualan = Performa_Penjualan.objects.all()
    context = {
        'performa_penjualan': performa_penjualan,
        'page': page
    }
    return render(request, 'base/performa_penjualan.html', context)


@login_required(login_url='login')
def ubahperforma_penjualan(request, pk):

    page = 'performa_penjualan'
    performa_penjualan = Performa_Penjualan.objects.get(id=pk)
    form = PerformaPenjualanChange(instance=performa_penjualan)
    if request.method == 'POST':
        form = PerformaPenjualanChange(request.POST, instance=performa_penjualan)
        if form.is_valid():
            form.save(commit=False)
            performa_penjualan.nama = performa_penjualan.nama
            performa_penjualan.save()
            
            # Save into another model or table
            
            nilai_performa_penjualan = (2*performa_penjualan.jual_brands)+performa_penjualan.jual_brands_lain
            nama_performa_penjualan = Penilaian.objects.get(nama=performa_penjualan.nama)
            nama_performa_penjualan.nilai_kehadiran = nilai_performa_penjualan
            nama_performa_penjualan.save()
            
            messages.success(request, 'Karyawan bernama ' + str(performa_penjualan.nama) + ' berhasil diubah Performa Penjualannya')
            return redirect('performapenjualan')
    context = {
		'form': form,
        'page': page
	}
    return render(request, 'base/ubahperforma_penjualan.html', context)





# Create your views here.


# def home(request):
#     page = 'home'
#     penilaian = Penilaian.objects.all()
#     # Retrieve all fields from the model
#     fields = Penilaian._meta.get_fields()

#     # Filter out only the decimal fields
#     decimal_fields = [f.name for f in fields if isinstance(f, models.DecimalField)]

#     # Retrieve only the decimal fields from the database
#     objects = Penilaian.objects.values(*decimal_fields)

    
#     # Convert queryset to a list, so pandas can handle it
#     queryset = list(objects)

#     # Convert the list to a dataframe
#     pandaspd = pd.DataFrame.from_records(queryset)


#     # Normalisasi
#     b_value = pd.DataFrame.from_records(queryset)
#     b_value1 = pd.DataFrame.from_records(queryset)
#     b_value2 = pd.DataFrame.from_records(queryset)
#     b_square = list()
#     for l in range(len(b_value.columns.values)):
#         b_square.append(math.sqrt(sum(k**2 for k in pandaspd[pandaspd.columns.values[l]])))
#     for i in range(len(b_value)):
#         for j in range(len(b_value.columns.values)):
#             b_value.iloc[i, j] = float(pandaspd.iloc[i, j]) / b_square[j]
#             b_value1.iloc[i, j] = float(pandaspd.iloc[i, j]) / b_square[j]
#             b_value2.iloc[i, j] = float(pandaspd.iloc[i, j]) / b_square[j]

#     b_value = b_value.to_html(classes="table table-borderless datatable")
#     # Normalisasi Selesai

    
#     # Normalisasi Terbobot
#     c_value = b_value1
#     c_value1 = b_value2
#     c_square = {'nilai_performa_penjualan': 0.439605556, 
#                 'nilai_pengetahuan_produk': 0.235712674,
#                 'nilai_disiplin': 0.151422771, 
#                 'nilai_kehadiran': 0.0866295, 
#                 'nilai_masa_kerja': 0.0866295
#                 }

#     for i in range(len(c_value)):
#         for j in range(len(c_value.columns.values)):
#             c_value.iloc[i, j] = float(c_value.iloc[i, j]) * c_square[c_value.columns.values[j]]
#             c_value1.iloc[i, j] = float(c_value1.iloc[i, j]) * c_square[c_value1.columns.values[j]]
#     c_value = c_value.to_html(classes="table table-borderless datatable")
    
#     # Normalisasi Terbobot Selesai

#     # Bobot Ideal
#     d_square = list()
#     d_square1 = list()
#     d_square2 = list()
#     for i in range(len(c_value1.columns.values)):
#         d_square.append(c_value1.columns.values[i])
#         d_square1.append(max(c_value1[c_value1.columns.values[i]]))
#         d_square2.append(min(c_value1[c_value1.columns.values[i]]))

#     d_square3 = pd.Series(d_square, name='nama_kriteria')
#     d_square4 = pd.Series(d_square1, name='nilai_ideal_positif')
#     d_square5 = pd.Series(d_square2, name='nilai_ideal_negatif')
#     d_value = pd.concat([d_square3, d_square4, d_square5], axis=1)
#     d_value1 = pd.concat([d_square3, d_square4, d_square5], axis=1)
#     d_value = d_value.to_html(classes="table table-borderless datatable")
#     # Bobot Ideal Selesai
    
#     # Jarak Ideal 
#     e_square = list()
#     e_square1 = list()
#     for i in range(len(c_value1)):
#         timer = 0
#         timer1 = 0
#         for j in range(len(c_value1.columns.values)):
#             perhitungan_positif = (c_value1.loc[i, c_value1.columns.values[j]]-d_value1[d_value1['nama_kriteria'] == c_value1.columns.values[j]]['nilai_ideal_positif'])**2
#             perhitungan_negatif = (d_value1[d_value1['nama_kriteria'] == c_value1.columns.values[j]]['nilai_ideal_negatif'] - c_value1.loc[i, c_value1.columns.values[j]])**2
#             timer = float(timer)+float(perhitungan_positif)
#             timer1 = float(timer1)+float(perhitungan_negatif)
#             if j == (len(c_value1.columns.values) - 1):
#                 e_square.append(math.sqrt(timer)) 
#                 e_square1.append(math.sqrt(timer1))
                
#     data_user = Penilaian.objects.values('nama_id__nama')
#     data_nama = pd.DataFrame.from_records(list(data_user))
#     data_nama.rename(columns={'nama_id__nama': 'nama'}, inplace=True)
    
#     e_square3 = pd.Series(e_square, name='jarak_ideal_positif')
#     e_square4 = pd.Series(e_square1, name='jarak_ideal_negatif')
    
#     e_value = pd.concat([data_nama, e_square3, e_square4], axis=1)
#     e_value1 = pd.concat([e_square3, e_square4], axis=1)
#     e_value = e_value.to_html(classes="table table-borderless datatable")
#     # Jarak Ideal Selesai
    
#     # Perhitungan Bobot Preferensi
#     f_square = list()
#     for i in range(len(e_value1)):
#         f_square.append((e_value1.iloc[i, 1]/(e_value1.iloc[i, 1]+e_value1.iloc[i, 0])))
    
#     f_square1 = pd.Series(f_square, name='bobot_preferensi')
#     f_value = pd.concat([data_nama, f_square1], axis=1)
#     f_value1 = pd.concat([data_nama, f_square1], axis=1)
#     #f_value['ranking'] = f_value['bobot_preferensi'].rank(method='dense', ascending=False)
#     f_value = f_value.to_html(classes="table table-borderless datatable")
#     # Perhitungan Bobot Preferensi Selesai
    
    
#     # Ranking 
#     penilaian_ranking = Penilaian.objects.values('id', 'nama_id__nama', *decimal_fields)
#     g_square = pd.DataFrame.from_records(list(penilaian_ranking))
#     g_value = pd.concat([g_square, f_square1], axis=1)
    
#     g_value.rename(columns={'nama_id__nama': 'nama'}, inplace=True)
#     g_value['ranking'] = g_value['bobot_preferensi'].rank(method='dense', ascending=False).round(1)


#     cols = list(g_value.columns)
#     # remove 'c' from the list of columns
#     cols.remove('ranking')
#     cols.remove('bobot_preferensi')

#     # insert 'c' at the start of the list
#     cols.insert(2, 'bobot_preferensi')
#     cols.insert(3, 'ranking')

#     # rearrange the columns
#     g_value = g_value[cols]
#     g_value['ranking'] = g_value['ranking'].astype(int)
#     g_value = g_value.to_html(classes="table table-borderless datatable")
    
    
    
#     querypandas = pd.Series(
#         pandaspd['nilai_kehadiran']*pandaspd['nilai_kehadiran'], name='Jumlah')

#     data = pd.concat([pandaspd, querypandas], axis=1)
#     htmlqu = data.to_html(classes="table table-borderless datatable")
    

#     context = {
#         'penilaian': penilaian,
#         'pandaspd': pandaspd,
#         'page': page,
#         'data': data,
#         'querypandas': querypandas,
#         'htmlqu': htmlqu,
#         'b_value': b_value,
#         'c_value': c_value,
#         'd_value': d_value,
#         'e_value': e_value,
#         'f_value': f_value,
#         'g_value': g_value
#     }
#     return render(request, 'base/home.html', context)

