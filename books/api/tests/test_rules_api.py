import pytest

from    django.contrib                        import    auth
from    django.contrib.auth.models            import    Permission
from    django.contrib.contenttypes.models    import    ContentType
from    django.urls                           import    reverse
from    ...models                             import    RBook


class TestBookRulesAPIViews:
    def test_model_perms(self, client, rbooks):
        perms  = Permission.objects.filter(
                   content_type__app_label  = 'books',
                   content_type             = ContentType.objects.get_for_model(RBook))

        assert set([perm.codename for perm in perms]) == set(['add_rbook', 'view_rbook', 'change_rbook', 'delete_rbook'])


    def test_user_has_perms(self, client, django_user_model, rusers):
        assert django_user_model.objects.get(username = 'ruser1').has_perm('books.add_rbook')    == True
        assert django_user_model.objects.get(username = 'ruser1').has_perm('books.view_rbook')   == True
        assert django_user_model.objects.get(username = 'ruser1').has_perm('books.change_rbook') == True
        assert django_user_model.objects.get(username = 'ruser1').has_perm('books.delete_rbook') == True

        assert django_user_model.objects.get(username = 'ruser2').has_perm('books.add_rbook')    == True
        assert django_user_model.objects.get(username = 'ruser2').has_perm('books.view_rbook')   == True
        assert django_user_model.objects.get(username = 'ruser2').has_perm('books.change_rbook') == True
        assert django_user_model.objects.get(username = 'ruser2').has_perm('books.delete_rbook') == False

        assert django_user_model.objects.get(username = 'ruser3').has_perm('books.add_rbook')    == True
        assert django_user_model.objects.get(username = 'ruser3').has_perm('books.view_rbook')   == True
        assert django_user_model.objects.get(username = 'ruser3').has_perm('books.change_rbook') == False
        assert django_user_model.objects.get(username = 'ruser3').has_perm('books.delete_rbook') == False


    def test_authenticated_user_can_create_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.post(
                      path  = reverse(
                                viewname  = 'books_api_app:rules-create'
                              ),
                      data  = {
                                'title':   'RBook 3',
                                'isbn':    '678',
                                'author':  'ruser1'
                              }
                    )

        assert response.status_code == 201
        assert set(map(str, RBook.objects.all())) == set(['RBook 1', 'RBook 2', 'RBook 3'])


    def test_anonymous_user_cannot_create_book(self, client, rusers, rbooks):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_api_app:rules-create'
                                     ),
                             data  = {
                                       'title':   'Book 3',
                                       'isbn':    '678',
                                       'author':  'ruser1'
                                     }
                            )

        assert response.status_code == 302
        assert response.url == (
                                 reverse(
                                   viewname  = 'login'
                                 ) + '?next=' +
                                 reverse(
                                   viewname  = 'books_api_app:rules-create'
                                 )
                               )


    def test_authenticated_user_can_view_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_api_app:rules-details',
                                       kwargs    = {
                                                     'title':  'RBook 1'
                                                   }
                                     )
                           )

        assert response.status_code == 200
        assert response.data['isbn'] == '123'


    def test_anonymous_user_cannot_view_book(self, client, rusers, rbooks):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_api_app:rules-details',
                                       kwargs    = {
                                                     'title':  'RBook 1'
                                                   }
                                     )
                           )

        assert response.status_code == 302
        assert response.url == (
                                  reverse(
                                    viewname  = 'login'
                                  ) + '?next=' +
                                  reverse(
                                    viewname  = 'books_api_app:rules-details',
                                    kwargs    = {
                                                   'title':  'RBook%201'
                                                }
                                  )
                               )


    def test_authenticated_user_can_list_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_api_app:rules-list'
                                     )
                           )

        assert response.status_code == 200
        assert set([book['title'] for book in response.data]) == set(['RBook 1', 'RBook 2'])


    def test_anonymous_user_cannot_list_book(self, client, users, books):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_api_app:rules-list'
                                     )
                           )

        assert response.status_code == 302
        assert response.url == (
                                  reverse(
                                    viewname  = 'login'
                                  ) + '?next=' +
                                  reverse(
                                    viewname  = 'books_api_app:rules-list'
                                  )
                               )


    def test_authenticated_user_can_update_own_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser3', password = 'password'):
            pytest.fail('failed to login')

        #
        # /opt/alex/pyvenv/venv/lib/python3.7/site-packages/django/contrib/auth/mixins.py(83)dispatch()
        # /opt/alex/pyvenv/venv/lib/python3.7/site-packages/rules/contrib/views.py(60)has_permission()
        # /opt/alex/pyvenv/venv/lib/python3.7/site-packages/rules/contrib/views.py(56)get_permission_object()
        # /opt/alex/pyvenv/venv/lib/python3.7/site-packages/rest_framework/generics.py(99)get_object()
        # /opt/alex/pyvenv/venv/lib/python3.7/site-packages/rest_framework/views.py(344)check_object_permissions()
        #
        # b /opt/alex/pyvenv/venv/lib/python3.7/site-packages/django/contrib/auth/mixins.py:83
        # b /opt/alex/pyvenv/venv/lib/python3.7/site-packages/rest_framework/views.py:342
        #
        # https://stackoverflow.com/a/51747714/1953757
        # https://github.com/encode/django-rest-framework/issues/918
        # https://github.com/JamesRitchie/django-rest-framework-expiring-tokens/issues/11
        #
        response  = client.patch(
                             path          = reverse(
                                               viewname  = 'books_api_app:rules-update',
                                               kwargs    = {
                                                             'title':  'RBook 1'
                                                           }
                                             ),
                             data          = {
                                               'isbn':  '222'
                                             },
                             content_type  = 'application/json'
                           )

        assert response.status_code == 200
        assert RBook.objects.get(title = 'RBook 2').isbn == '222'


    def test_anonymous_user_cannot_update_book(self, client, rusers, rbooks):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.patch(
                             path  = reverse(
                                       viewname  = 'books_api_app:rules-update',
                                       kwargs    = {
                                                     'title':  'RBook 1'
                                                   }
                                     ),
                             data  = {
                                       'isbn':  '222'
                                     }
                           )

        assert response.status_code == 302
        assert response.url == (
                                  reverse(
                                    viewname  = 'login'
                                  ) + '?next=' +
                                  reverse(
                                    viewname  = 'books_api_app:rules-update',
                                    kwargs    = {
                                                   'title':  'RBook%201'
                                                }
                                  )
                               )


    def test_authenticated_user_with_user_permission_can_update_another_users_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.patch(
                             path          = reverse(
                                               viewname  = 'books_api_app:rules-update',
                                               kwargs    = {
                                                             'title':  'RBook 1'
                                                           }
                                             ),
                             data          = {
                                               'isbn':  '222'
                                             },
                             content_type  = 'application/json'
                           )

        assert response.status_code == 200
        assert RBook.objects.get(title = 'RBook 1').isbn == '222'


    def test_authenticated_user_with_group_permission_can_update_another_users_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser2', password = 'password'):
            pytest.fail('failed to login')

        response  = client.patch(
                             path          = reverse(
                                               viewname  = 'books_api_app:rules-update',
                                               kwargs    = {
                                                             'title':  'RBook 1'
                                                           }
                                             ),
                             data          = {
                                               'isbn':  '222'
                                             },
                             content_type  = 'application/json'
                           )

        assert response.status_code == 200
        assert RBook.objects.get(title = 'RBook 1').isbn == '222'


    def test_authenticated_user_can_delete_own_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser3', password = 'password'):
            pytest.fail('failed to login')

        response  = client.delete(
                             path  = reverse(
                                       viewname  = 'books_api_app:rules-delete',
                                       kwargs    = {
                                                     'title':  'RBook 2'
                                                   }
                                     )
                           )

        assert response.status_code == 204
        assert set(map(str, RBook.objects.all())) == set(['RBook 1'])


    def test_authenticated_user_with_user_permission_can_delete_another_users_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.delete(
                             path  = reverse(
                                       viewname  = 'books_api_app:rules-delete',
                                       kwargs    = {
                                                     'title':  'RBook 1'
                                                   }
                                     )
                           )

        assert response.status_code == 204
        assert set(map(str, RBook.objects.all())) == set(['RBook 2'])


    def test_anonymous_user_cannot_delete_book(self, client, rusers, rbooks):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.delete(
                             path  = reverse(
                                       viewname  = 'books_api_app:rules-delete',
                                       kwargs    = {
                                                     'title':  'RBook 1'
                                                   }
                                     )
                           )

        assert response.status_code == 302
        assert response.url == (
                                  reverse(
                                    viewname  = 'login'
                                  ) + '?next=' +
                                  reverse(
                                    viewname  = 'books_api_app:rules-delete',
                                    kwargs    = {
                                                   'title':  'RBook%201'
                                                }
                                  )
                               )


    def test_authenticated_user_without_permission_cannot_delete_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser3', password = 'password'):
            pytest.fail('failed to login')

        response  = client.delete(
                             path  = reverse(
                                       viewname  = 'books_api_app:rules-delete',
                                       kwargs    = {
                                                     'title':  'RBook%201'
                                                   }
                                     )
                           )

        assert response.status_code == 404
        assert set(map(str, RBook.objects.all())) == set(['RBook 1', 'RBook 2'])
