"""project_nama URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from listapp.views import (Home,
                AnggotaListView,
                person_create,
                person_show,
                AnggotaDetailView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$', Home.as_view(), name='my-view'),
    url(r'^list/$', AnggotaListView.as_view(), name='list-anggota'),
    url(r'^list/(?P<slug>\w+)/$', AnggotaDetailView.as_view(), name='list-detail'),
    url(r'^create/$', person_create),
    url(r'^$', person_show),
]
