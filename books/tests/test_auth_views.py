import pytest

from django.contrib import auth
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from ..models import Book


@pytest.mark.django_db
class TestBookAuthViews:
    def test_model_perms(self, client, books):
        perms  = Permission.objects.filter(
                   content_type__app_label  = 'books',
                   content_type             = ContentType.objects.get_for_model(Book))

        assert set([perm.codename for perm in perms]) == set(['add_book', 'view_book', 'change_book', 'delete_book'])


    def test_user_has_perms(self, client, django_user_model, users, books):
        assert django_user_model.objects.get(username = 'user1').has_perm('books.add_book')    == True
        assert django_user_model.objects.get(username = 'user1').has_perm('books.view_book')   == True
        assert django_user_model.objects.get(username = 'user1').has_perm('books.change_book') == True
        assert django_user_model.objects.get(username = 'user1').has_perm('books.delete_book') == False

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


    def test_authenticated_user_can_create_book(self, client, users, books):
        if not client.login(username = 'user1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_web_app:auth-create'),
                             data  = {
                                       'title':   'Book 3',
                                       'isbn':    '789',
                                       'author':  'user1'
                                     }
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:auth-detail',
                                 kwargs    = {
                                               'title':  'Book 3'
                                             }
                               )
        assert set(map(str, Book.objects.all())) == set(['Book 1', 'Book 2', 'Book 3'])


    def test_anonymous_user_cannot_create_book(self, client, users, books):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_web_app:auth-create'),
                             data  = {
                                       'title':   'Book 3',
                                       'isbn':    '789',
                                       'author':  'user2'
                                     }
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:book-home'
                               )
        assert set(map(str, Book.objects.all())) == set(['Book 1', 'Book 2'])


    def test_authenticated_user_can_view_book(self, client, users, books):
        if not client.login(username = 'user1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_web_app:auth-detail',
                                       kwargs    = {
                                                     'title': 'Book 1'
                                                   }
                                     )
                           )

        assert response.status_code == 200


    def test_anonymous_user_cannot_view_book(self, client, users, books):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_web_app:auth-detail',
                                       kwargs    = {
                                                     'title':  'Book 1'
                                                   }
                                     )
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:book-home'
                               )


    def test_authenticated_user_can_update_book(self, client, users, books):
        if not client.login(username = 'user2', password = 'password'):
            pytest.fail('failed to login')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_web_app:auth-update',
                                       kwargs    = {
                                                     'title':  'Book 1',
                                                   }
                                     ),
                             data  = {
                                       'title':   'Book 1',
                                       'isbn':    '222',
                                       'author':  'user1'
                                     }
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:auth-detail',
                                 kwargs    = {
                                               'title':  'Book 1'
                                             }
                               )
        assert Book.objects.get(title = 'Book 1').isbn == '222'


    def test_anonymous_user_cannot_update_book(self, client, users, books):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_web_app:auth-update',
                                       kwargs    = {
                                                     'title':  'Book 1',
                                                   }
                                     ),
                             data  = {
                                       'title':   'Book 1',
                                       'isbn':    '222',
                                       'author':  'user1'
                                     }
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:book-home'
                               )


    def test_authenticated_user_can_delete_book(self, client, users, books):
        if not client.login(username = 'user3', password = 'password'):
            pytest.fail('failed to login')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_web_app:auth-delete',
                                       kwargs    = {
                                                     'title':  'Book 1'
                                                   }
                                     )
                           )

        assert set(map(str, Book.objects.all())) == set(['Book 2'])
        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:book-home'
                               )


    def test_anonymous_user_cannot_delete_book(self, client, users, books):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_web_app:auth-delete',
                                       kwargs    = {
                                                     'title': 'Book 1'
                                                   }
                                     )
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:book-home'
                               )
        assert set(map(str, Book.objects.all())) == set(['Book 1', 'Book 2'])
