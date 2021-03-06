"""bakpak_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


app_name = "bakpak_website"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bakpak/', include('bakpak_website.urls'), name="home_page"),
    path('', include('bakpak_website.urls'), name="home_page"),
    path(
            "favicon.ico",
            RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
        ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Brasserie Bakapker"
admin.site.site_title = "Administration Bakpaker"
admin.site.index_title = "Administration Bakpaker"
admin.site.site_url = "/bakpak/"
