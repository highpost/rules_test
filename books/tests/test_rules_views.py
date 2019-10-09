import pytest

from django.contrib import auth
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from ..models import RBook


@pytest.mark.django_db
class TestBookRulesViews:
    def test_model_perms(self, client, rbooks):
        perms  = Permission.objects.filter(
                   content_type__app_label  = 'books',
                   content_type             = ContentType.objects.get_for_model(RBook))

        assert set([perm.codename for perm in perms]) == set(['add_rbook', 'view_rbook', 'change_rbook', 'delete_rbook'])


    def test_user_has_perms(self, client, django_user_model, rusers):
        assert django_user_model.objects.get(username = 'ruser1').has_perm('books.add_rbook')    == True
        assert django_user_model.objects.get(username = 'ruser1').has_perm('books.view_rbook')   == True
        assert django_user_model.objects.get(username = 'ruser1').has_perm('books.change_rbook') == False
        assert django_user_model.objects.get(username = 'ruser1').has_perm('books.delete_rbook') == False

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
                                       viewname  = 'books_web_app:rules-create'),
                             data  = {
                                       'title':   'RBook 3',
                                       'isbn':    '789',
                                       'author':  'ruser1'
                                     }
                           )

        assert response.status_code == 302
        assert response.url == reverse(
                                 viewname  = 'books_web_app:rules-detail',
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
                                       viewname  = 'books_web_app:rules-create'),
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
                                       viewname  = 'books_web_app:rules-detail',
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
                                       viewname  = 'books_web_app:rules-detail',
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
                                       viewname  = 'books_web_app:rules-update',
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
                                 viewname  = 'books_web_app:rules-detail',
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
                                       viewname  = 'books_web_app:rules-update',
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
                                 viewname  = 'books_web_app:rules-detail',
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
                                       viewname  = 'books_web_app:rules-delete',
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
                                       viewname  = 'books_web_app:rules-delete',
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
