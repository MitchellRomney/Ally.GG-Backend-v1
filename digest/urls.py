from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView
from dashboard import views as dashboard
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

router = routers.DefaultRouter()
router.register(r'users', dashboard.UserViewSet)
router.register(r'summoners', dashboard.SummonerViewSet)

urlpatterns = [
    path('', dashboard.home,name='home'),

    path('summoners/<summonerName>/', dashboard.summonerDetails, name='summonerDetails'),

    path('api/', include(router.urls)),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
