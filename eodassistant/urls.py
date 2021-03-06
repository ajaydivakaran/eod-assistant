"""eodassistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers

from eod.views import TeamViewSet, ContributorViewSet, EndOfDayItemViewSet

router = routers.DefaultRouter()
router.register(r'team', TeamViewSet)
router.register(r'contributor', ContributorViewSet)
router.register(r'eod', EndOfDayItemViewSet, base_name='eod-list')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
]

urlpatterns += staticfiles_urlpatterns()
