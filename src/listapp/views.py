from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from .models import GENDER, Person
from .forms import PersonCreate, PersonShow
# Create your views here.
class Home(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        return

class AnggotaListView(ListView):
    queryset = Person.objects.all()

class AnggotaDetailView(DetailView):
    queryset = Person.objects.all()

def person_create(request):
    form = PersonCreate(request.POST or None)
    if form.is_valid():
        obj = Person.objects.create(
            first_name  = form.cleaned_data.get('first_name'),
            last_name   = form.cleaned_data.get('last_name'),
            gender      = form.cleaned_data.get('gender'),
            father      = form.cleaned_data.get('father'),
            mother      = form.cleaned_data.get('mother'),
            date_birth  = form.cleaned_data.get('date_birth'),
        )
        return HttpResponseRedirect('/list/')
    template_name = 'listapp/create_list.html'
    context = {"form": form}
    return render(request, template_name, context)

def person_show(request):
    form = PersonShow(request.POST or None)
    #print(form)
    if form.is_valid():
        f = form.cleaned_data
        slug = f.get('first_name').slug
        return HttpResponseRedirect('list/' + slug)
    template_name = 'listapp/detail_person.html'
    context = {"form": form}
    return render(request, template_name, context)
