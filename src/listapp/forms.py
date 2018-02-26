from django import forms
from django.forms.extras.widgets import SelectDateWidget
from .models import GENDER, Person
import datetime

queryset_father = Person.objects.filter(gender='M')
queryset_mother = Person.objects.filter(gender='F')
queryset_person = Person.objects.all()
year_now = datetime.datetime.now().year

class PersonCreate(forms.Form):

    first_name      = forms.CharField(label='Nama Depan')
    last_name       = forms.CharField(label='Nama Belakang')
    gender          = forms.CharField(label='Jenis Kelamin', max_length=1, widget=forms.Select(choices= GENDER))
    father          = forms.ModelChoiceField(queryset_father, label='Ayah', empty_label='-', required=False)
    mother          = forms.ModelChoiceField(queryset_mother,label='Ibu', empty_label='-', required=False)
    date_birth      = forms.DateField(widget=SelectDateWidget(years=range(1900, year_now)), label='Tanggal Lahir')

class PersonShow(forms.Form):

    first_name      = forms.ModelChoiceField(queryset_person, label='Nama', empty_label=None, required=False)
