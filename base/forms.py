from django.forms import ModelForm
from .models import User, Disiplin, Kehadiran, Performa_Penjualan, Penilaian, Nilai_Ahp
from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import date
import calendar
from itertools import combinations
from django.db.models import DecimalField

class MyUserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['nama', 'username', 'email', 'brand', 'nilai_pengetahuan_produk', 'tgl_masuk', 'password1', 'password2']
        #tgl_masuk = forms.SplitDateTimeWidget()
    def __init__(self, *args, **kwargs):
        super(MyUserCreation, self).__init__(*args, **kwargs)
        self.fields['tgl_masuk'] = forms.DateField(initial=date.today())
        

class UserChange(ModelForm):
    class Meta:
        model = User
        fields = ['nama', 'username', 'email', 'brand', 'nilai_pengetahuan_produk', 'tgl_masuk', 'password']
        #tgl_masuk = forms.SplitDateTimeWidget()
    def __init__(self, *args, **kwargs):
        super(UserChange, self).__init__(*args, **kwargs)
        self.fields['tgl_masuk'] = forms.DateField(initial=date.today())


class DisiplinChange(ModelForm):
    class Meta:
        model = Disiplin
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(DisiplinChange, self).__init__(*args, **kwargs)
        self.fields['nilai_pelanggaran'] = forms.ChoiceField(choices=[(0, '0'),(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
        self.fields['kuota_disiplin'].disabled = True


class KehadiranChange(ModelForm):
    class Meta:
        model = Kehadiran
        fields = '__all__'

class PerformaPenjualanChange(ModelForm):
    class Meta:
        model = Performa_Penjualan
        fields = '__all__'


# class AhpForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in Penilaian._meta.get_fields():
#             if isinstance(field, DecimalField):
#                 self.fields[field.name] = forms.BooleanField(required=False)
class AhpForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in Penilaian._meta.get_fields():
            if isinstance(field, DecimalField):
                self.fields[field.name] = forms.BooleanField(required=False)


    def clean(self):
        cleaned_data = super().clean()

        # Check how many boxes were checked
        num_checked = sum(bool(cleaned_data.get(name)) for name in cleaned_data)

        # If less than 3 were checked, raise an error
        if num_checked < 3:
            raise forms.ValidationError("Untuk Perhitungan AHP, Tolong untuk Centang setidaknya 3 Checkbox, Karena jika hanya mencentang 1 atau 2 kriteria, Random Index AHP-nya adalah 0.00, sehingga tidak dapat dilakukan perhitungan AHP")

        return cleaned_data

class PerbandinganAhpForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pilihan_kepentingan = [(i, str(i)) for i in range(1, 10)]
        self.pilihan_kriteria = [obj.nama_kriteria for obj in Nilai_Ahp.objects.all()]
        for score1, score2 in combinations(self.pilihan_kriteria, 2):
            perbandingan = f'{score1}/{score2}'
            self.fields[perbandingan] = forms.ChoiceField(choices=self.pilihan_kepentingan)


# class PerbandinganAhpForm(forms.Form):
#     pilihan_kepentingan = [(i, str(i)) for i in range(1, 10)]
#     pilihan_kriteria = [obj.nama_kriteria for obj in Nilai_Ahp.objects.all()]
#     for score1, score2 in combinations(pilihan_kriteria, 2):
#         perbandingan = f'{score1}/{score2}'
#         locals()[perbandingan] = forms.ChoiceField(choices=pilihan_kepentingan)
    


        



        

        