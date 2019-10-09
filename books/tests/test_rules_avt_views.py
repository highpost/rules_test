import pytest

from django.contrib import auth
from django.urls import reverse
from ..models import RBook


@pytest.mark.django_db
class TestBookRulesViews:
    def test_authenticated_user_can_create_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_web_app:rules-avt-create'),
                             data  = {
                                       'title':   'RBook 3',
                                       'isbn':    '789',
                                       'author':  'ruser1'
                                     }
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:rules-avt-detail',
                                 kwargs    = {
                                               'title':  'RBook 3'
                                             }
                               )
        assert set(map(str, RBook.objects.all())) == set(['RBook 1', 'RBook 2', 'RBook 3'])


    def test_anonymous_user_cannot_create_book(self, client, rusers, rbooks):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_web_app:rules-avt-create'),
                             data  = {
                                       'title':   'RBook 3',
                                       'isbn':    '789',
                                       'author':  'ruser2'
                                     }
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:book-home'
                               )
        assert set(map(str, RBook.objects.all())) == set(['RBook 1', 'RBook 2'])


    def test_authenticated_user_can_view_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_web_app:rules-avt-detail',
                                       kwargs    = {
                                                     'title': 'RBook 1'
                                                   }
                                     )
                           )

        assert response.status_code == 200


    def test_anonymous_user_cannot_view_book(self, client, rusers, rbooks):
        if not auth.get_user(client).is_anonymous:
            pytest.fail('not anonymous user')

        response  = client.get(
                             path  = reverse(
                                       viewname  = 'books_web_app:rules-avt-detail',
                                       kwargs    = {
                                                     'title':  'RBook 1'
                                                   }
                                     )
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:book-home'
                               )


    def test_authenticated_user_can_update_own_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_web_app:rules-avt-update',
                                       kwargs    = {
                                                     'title':  'RBook 1'
                                                   }
                                     ),
                             data  = {
                                       'title':   'RBook 1',
                                       'isbn':    '222',
                                       'author':  'ruser1'
                                     }
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:rules-avt-detail',
                                 kwargs    = {
                                               'title':   'RBook 1'
                                             }
                           )
        assert RBook.objects.get(title = 'RBook 1').isbn == '222'


    def test_user_with_group_permission_updates_another_users_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser2', password = 'password'):
            pytest.fail('failed to login')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_web_app:rules-avt-update',
                                       kwargs    = {
                                                     'title':  'RBook 1'
                                                   }
                                     ),
                             data  = {
                                       'title':   'RBook 1',
                                       'isbn':    '222',
                                       'author':  'ruser1'
                                     }
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:rules-avt-detail',
                                 kwargs    = {
                                               'title':   'RBook 1'
                                             }
                               )
        assert RBook.objects.get(title = 'RBook 1').isbn == '222'


    def test_authenticated_user_can_delete_own_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser1', password = 'password'):
            pytest.fail('failed to login')

        response  = client.post(
                             path  = reverse(
                                       viewname  = 'books_web_app:rules-avt-delete',
                                       kwargs    = {
                                                     'title':  'RBook 1'
                                                   }
                                     )
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:book-home'
                               )
        assert set(map(str, RBook.objects.all())) == set(['RBook 2'])


    def test_authenticated_user_without_permission_cannot_delete_book(self, client, rusers, rbooks):
        if not client.login(username = 'ruser3', password = 'password'):
            pytest.fail('failed to login')

        response  = client.delete(
                             path  = reverse(
                                       viewname  = 'books_web_app:rules-avt-delete',
                                       kwargs    = {
                                                     'title': 'RBook 1'
                                                   }
                                     )
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:book-home'
                               )
        assert set(map(str, RBook.objects.all())) == set(['RBook 1', 'RBook 2'])
