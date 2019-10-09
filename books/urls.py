from django.urls import path, include
from django.views.generic import TemplateView
from .views import (BookAuthCreateView,
                    BookAuthDetailView,
                    BookAuthListView,
                    BookAuthUpdateView,
                    BookAuthDeleteView,
                    BookRulesCreateView,
                    BookRulesDetailView,
                    BookRulesListView,
                    BookRulesUpdateView,
                    BookRulesDeleteView,
                    BookRulesAVTCreateView,
                    BookRulesAVTDetailView,
                    BookRulesAVTListView,
                    BookRulesAVTUpdateView,
                    BookRulesAVTDeleteView)

app_name     = 'books_web_app'

urlpatterns  = [
                 path(
                   name   = 'book-home',
                   route  = '',
                   view   = TemplateView.as_view(template_name = 'books/book_home.html')),

                 path(
                   name   = 'auth-create',
                   route  = 'auth-create/',
                   view   = BookAuthCreateView.as_view()),
                 path(
                   name   = 'auth-detail',
                   route  = 'auth-detail/<str:title>/',
                   view   = BookAuthDetailView.as_view()),
                 path(
                   name   = 'auth-list',
                   route  = 'auth-list/',
                   view   = BookAuthListView.as_view()),
                 path(
                   name   = 'auth-update',
                   route  = 'auth-update/<str:title>/',
                   view   = BookAuthUpdateView.as_view()),
                 path(
                   name   = 'auth-delete',
                   route  = 'auth-delete/<str:title>/',
                   view   = BookAuthDeleteView.as_view()),

                 path(
                   name   = 'rules-create',
                   route  = 'rules-create/',
                   view   = BookRulesCreateView.as_view()),
                 path(
                   name   = 'rules-detail',
                   route  = 'rules-detail/<str:title>/',
                   view   = BookRulesDetailView.as_view()),
                 path(
                   name   = 'rules-list',
                   route  = 'rules-list/',
                   view   = BookRulesListView.as_view()),
                 path(
                   name   = 'rules-update',
                   route  = 'rules-update/<str:title>/',
                   view   = BookRulesUpdateView.as_view()),
                 path(
                   name   = 'rules-delete',
                   route  = 'rules-delete/<str:title>/',
                   view   = BookRulesDeleteView.as_view()),

                 path(
                   name   = 'rules-avt-create',
                   route  = 'rules-avt-create/',
                   view   = BookRulesAVTCreateView.as_view()),
                 path(
                   name   = 'rules-avt-detail',
                   route  = 'rules-avt-detail/<str:title>/',
                   view   = BookRulesAVTDetailView.as_view()),
                 path(
                   name   = 'rules-avt-list',
                   route  = 'rules-avt-list/',
                   view   = BookRulesAVTListView.as_view()),
                 path(
                   name   = 'rules-avt-update',
                   route  = 'rules-avt-update/<str:title>/',
                   view   = BookRulesAVTUpdateView.as_view()),
                 path(
                   name   = 'rules-avt-delete',
                   route  = 'rules-avt-delete/<str:title>/',
                   view   = BookRulesAVTDeleteView.as_view()),
               ]
