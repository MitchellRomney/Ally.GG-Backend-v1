from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import RedirectView
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from AllyGG.schema import schema
from AllyGG import settings
from . import views

urlpatterns = [
                  path('admin/', admin.site.urls),

                  path('', RedirectView.as_view(url='https://www.ally.gg')),

                  path('activate/<username>/<token>', views.activate, name='activate'),

                  url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
