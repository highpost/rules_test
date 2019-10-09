from django.contrib import admin
from django.urls import include, path

urlpatterns  = [
                 path(
                   route  = 'admin/',
                   view   = admin.site.urls),
                 path(
                   route  = 'accounts/',
                   view   = include('django.contrib.auth.urls')),
                 path(
                   route  = 'books_api_app/',
                   view   = include('books.api.urls')),
                 path(
                   route  = 'books_web_app/',
                   view   = include('books.urls')),
               ]
