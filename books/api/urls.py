from    django.urls    import     path
from    .views         import    (BookAuthCreateAPIView,
                                  BookAuthRetrieveAPIView,
                                  BookAuthListAPIView,
                                  BookAuthUpdateAPIView,
                                  BookAuthDestroyAPIView,
                                  BookRulesCreateAPIView,
                                  BookRulesRetrieveAPIView,
                                  BookRulesListAPIView,
                                  BookRulesUpdateAPIView,
                                  BookRulesDestroyAPIView)

app_name     = 'books_api_app'

urlpatterns  = (
                 path(
                     route  = 'auth-create/',
                     view   = BookAuthCreateAPIView.as_view(),
                     name   = 'auth-create'),
                 path(
                     route  = 'auth-details/<str:title>/',
                     view   = BookAuthRetrieveAPIView.as_view(),
                     name   = 'auth-details'),
                 path(
                     route  = 'auth-list/',
                     view   = BookAuthListAPIView.as_view(),
                     name   = 'auth-list'),
                 path(
                     route  = 'auth-update/<str:title>/',
                     view   = BookAuthUpdateAPIView.as_view(),
                     name   = 'auth-update'),
                 path(
                     route  = 'auth-delete/<str:title>/',
                     view   = BookAuthDestroyAPIView.as_view(),
                     name   = 'auth-delete'),

                 path(
                     route  = 'rules-create/',
                     view   = BookRulesCreateAPIView.as_view(),
                     name   = 'rules-create'),
                 path(
                     route  = 'rules-details/<str:title>/',
                     view   = BookRulesRetrieveAPIView.as_view(),
                     name   = 'rules-details'),
                 path(
                     route  = 'rules-list/',
                     view   = BookRulesListAPIView.as_view(),
                     name   = 'rules-list'),
                 path(
                     route  = 'rules-update/<str:title>/',
                     view   = BookRulesUpdateAPIView.as_view(),
                     name   = 'rules-update'),
                 path(
                     route  = 'rules-delete/<str:title>/',
                     view   = BookRulesDestroyAPIView.as_view(),
                     name   = 'rules-delete'),
               )
