from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from dashboard import views as dashboard
from website import views as website
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from AllyGG.schema import schema


router = routers.DefaultRouter()
router.register(r'users', dashboard.UserViewSet)
router.register(r'summoners', dashboard.SummonerViewSet)
router.register(r'matches', dashboard.MatchViewSet)
router.register(r'players', dashboard.PlayerViewSet)
router.register(r'champions', dashboard.ChampionViewSet)
router.register(r'items', dashboard.ItemViewSet)
router.register(r'chat/room', dashboard.ChatRoomViewSet)
router.register(r'accesscodes', dashboard.AccessCodeViewSet)

urlpatterns = [
                  path('', website.home, name='home'),

                  path('register', website.register, name='register'),

                  path('profiles/<username>/', dashboard.profile, name='profile'),

                  path('chat/', dashboard.chat, name='chat'),

                  path('summoners/', dashboard.summoners, name='summoners'),

                  path('summoners/<summonerName>/', dashboard.summonerDetails, name='summonerDetails'),

                  path('admin/', admin.site.urls),

                  path('api/', include(router.urls)),

                  url(r'^api/game/$', dashboard.GameView.as_view()),

                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

                  url(r'^s3direct/', include('s3direct.urls')),

                  url(r'^accounts/', include('registration.backends.simple.urls')),

                  url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
