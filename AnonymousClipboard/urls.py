"""AnonymousClipboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin

from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth.models import User, Group

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import permissions, routers, serializers, viewsets
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from clipboard import views as v
from frontend import views




# Routers provide an easy way of automatically determining the URL conf
#router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
#router.register(r'groups', GroupViewSet)
urlpatterns = [
    url(r'^sign_up/$', v.SignUp.as_view(), name="sign_up"),

    #url(r'^', include(router.urls)),

	url(r'^api/', include('clipboard.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    #path('', include('frontend.urls')),
    url(r'^admin/', admin.site.urls),


]
