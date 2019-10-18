import pytest

from    django.contrib            import    auth
from    django.contrib.auth.models        import    Permission
from    django.contrib.contenttypes.models    import    ContentType
from    django.urls               import    reverse
from    ...models                 import    Book


class TestBookAuthAPIViews:
    def test_model_perms(self, client, books):
        perms  = Permission.objects.filter(
                   content_type__app_label  = 'books',
                   content_type             = ContentType.objects.get_for_model(Book))

        assert set([perm.codename for perm in perms]) == set(['add_book', 'view_book', 'change_book', 'delete_book'])


    def test_user_has_perms(self, client, django_user_model, users):
        assert django_user_model.objects.get(username = 'user1').has_perm('books.add_book')    == True
        assert django_user_model.objects.get(username = 'user1').has_perm('books.view_book')   == True
        assert django_user_model.objects.get(username = 'user1').has_perm('books.change_book') == True
        assert django_user_model.objects.get(username = 'user1').has_perm('books.delete_book') == True

        assert django_user_model.objects.get(username = 'user2').has_perm('books.add_book')    == False
        assert django_user_model.objects.get(username = 'user2').has_perm('books.view_book')   == False
        assert django_user_model.objects.get(username = 'user2').has_perm('books.change_book') == True
        assert django_user_model.objects.get(username = 'user2').has_perm('books.delete_book') == False

        assert django_user_model.objects.get(username = 'user3').has_perm('books.add_book')    == False
        assert django_user_model.objects.get(username = 'user3').has_perm('books.view_book')   == False
        assert django_user_model.objects.get(username = 'user3').has_perm('books.change_book') == False
        assert django_user_model.objects.get(username = 'user3').has_perm('books.delete_book') == True

        assert django_user_model.objects.get(username = 'user4').has_perm('books.add_book')    == False
        assert django_user_model.objects.get(username = 'user4').has_perm('books.view_book')   == False
        assert django_user_model.objects.get(username = 'user4').has_perm('books.change_book') == False
        assert django_user_model.objects.get(username = 'user4').has_perm('books.delete_book') == False


    def test_authenticated_user_with_permission_can_create_book(self, client, users, books):
        if not client.login(username = 'user1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_api_app:auth-create',
                                     ),
                             data  = {
                                       'title':   'Book 3',
                                       'isbn':    '678',
                                       'author':  'user1'
                                     }
                           )

        assert response.status_code == 201
        assert set(map(str, Book.objects.all())) == set(['Book 1', 'Book 2', 'Book 3'])


    def test_anonymous_user_cannot_create_book(self, client, users, books):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_api_app:auth-create'
                                     ),
                             data  = {
                                       'title':   'Book 3',
                                       'isbn':    '678',
                                       'author':  'user1'
                                     }
                           )

        assert response.status_code == 302
        assert response.url == (
                                  reverse(
                                    viewname  = 'login'
                                  ) + '?next=' +
                                  reverse(
                                    viewname  = 'books_api_app:auth-create'
                                  )
                               )


    def test_authenticated_user_with_permission_can_view_book(self, client, users, books):
        if not client.login(username = 'user1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_api_app:auth-details',
                                       kwargs    = {
                                                     'title':  'Book 1'
                                                   }
                                     )
                            )

        assert response.status_code == 200
        assert response.data['isbn'] == '123'


    def test_anonymous_user_cannot_view_book(self, client, users, books):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_api_app:auth-details',
                                       kwargs    = {
                                                     'title':  'Book 1'
                                                   }
                                     )
                           )

        assert response.status_code == 302
        #
        # HACK: this is a workaround for what looks like a bug in python-django.
        # response.url is getting urlencoded twice and until I dig out the source
        # of this behaviour I'll add a %20 to the right side of the assertion.
        #
        assert response.url == (
                                  reverse(
                                    viewname  = 'login'
                                  ) + '?next=' +
                                  reverse(
                                    viewname  = 'books_api_app:auth-details',
                                    kwargs    = {
                                                  'title':  'Book%201'
                                                }
                                  )
                               )


    def test_authenticated_user_without_permission_cannot_view_book(self, client, users, books):
        if not client.login(username = 'user4', password = 'password'):
            pytest.fail('failed to login')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_api_app:auth-details',
                                       kwargs    = {
                                                     'title':  'Book 1'
                                                   }
                                     )
                           )

        assert response.status_code == 403


    def test_authenticated_user_with_permission_can_list_book(self, client, users, books):
        if not client.login(username = 'user1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_api_app:auth-list'
                                     )
                           )

        assert response.status_code == 200
        assert set([book['title'] for book in response.data]) == set(['Book 1', 'Book 2'])


    def test_anonymous_user_cannot_list_book(self, client, users, books):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_api_app:auth-list'
                                     )
                           )

        assert response.status_code == 302
        assert response.url == (
                                  reverse(
                                    viewname  = 'login'
                                  ) + '?next=' +
                                  reverse(
                                    viewname  = 'books_api_app:auth-list'
                                  )
                               )


    def test_authenticated_user_with_permission_can_update_book(self, client, users, books):
        if not client.login(username = 'user1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.patch(
                             path          = reverse(
                                               viewname  = 'books_api_app:auth-update',
                                               kwargs    = {
                                                             'title':  'Book 1'
                                                           }
                                             ),
                             data          = {
                                               'isbn':    '222',
                                             },
                             content_type  = 'application/json'
                           )

        assert response.status_code == 200
        assert Book.objects.get(title = 'Book 1').isbn == '222'


    def test_anonymous_user_cannot_update_book(self, client, users, books):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.patch(
                             path          = reverse(
                                               viewname  = 'books_api_app:auth-update',
                                               kwargs    = {
                                                             'title':  'Book 1'
                                                           }
                                             ),
                             data          = {
                                               'isbn':    '222',
                                             },
                             content_type  = 'application/json'
                           )

        assert response.status_code == 302
        assert response.url == (
                                  reverse(
                                    viewname  = 'login'
                                  ) + '?next=' +
                                  reverse(
                                    viewname  = 'books_api_app:auth-update',
                                    kwargs    = {
                                                  'title':  'Book%201'
                                                }
                                  )
                               )


    def test_authenticated_user_with_permission_can_delete_book(self, client, users, books):
        if not client.login(username = 'user1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.delete(
                             path  = reverse(
                                       viewname  = 'books_api_app:auth-delete',
                                       kwargs    = {
                                                     'title':  'Book 1'
                                                   }
                                     )
                           )

        assert response.status_code == 204
        assert set(map(str, Book.objects.all())) == set(['Book 2'])


    def test_anonymous_user_cannot_delete_book(self, client, users, books):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.delete(
                             path  = reverse(
                                       viewname  = 'books_api_app:auth-delete',
                                       kwargs    = {
                                                     'title':  'Book 1'
                                                   }
                                     )
                           )

        assert response.status_code == 302
        assert response.url == (
                                  reverse(
                                    viewname  = 'login'
                                  ) + '?next=' +
                                  reverse(
                                    viewname  = 'books_api_app:auth-delete',
                                    kwargs    = {
                                                  'title':  'Book%201'
                                                }
                                  )
                               )
        assert set(map(str, Book.objects.all())) == set(['Book 1', 'Book 2'])
