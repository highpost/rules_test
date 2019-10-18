import pytest

from    django.contrib.auth.models    import    Group, Permission
from    ..models                      import    Book, RBook


@pytest.fixture()
def users(django_user_model):
    add_book     = Permission.objects.get(codename = 'add_book')
    view_book    = Permission.objects.get(codename = 'view_book')
    change_book  = Permission.objects.get(codename = 'change_book')
    delete_book  = Permission.objects.get(codename = 'delete_book')

    user1    = django_user_model.objects.create(
                 username      = 'user1',
                 is_superuser  = False,
                 is_staff      = False
               )
    user1.set_password('password'),
    user1.user_permissions.add(add_book)
    user1.user_permissions.add(view_book)
    user1.user_permissions.add(change_book)
    user1.save()

    user2    = django_user_model.objects.create(
                 username      = 'user2',
                 is_superuser  = False,
                 is_staff      = False
               )
    user2.set_password('password'),
    user2.user_permissions.add(change_book)
    user2.save()

    user3    = django_user_model.objects.create(
                 username      = 'user3',
                 is_superuser  = False,
                 is_staff      = False
               )
    user3.set_password('password'),
    user3.user_permissions.add(delete_book)
    user3.save()

    user4    = django_user_model.objects.create(
                 username      = 'user4',
                 is_superuser  = False,
                 is_staff      = False
               )
    user4.set_password('password'),
    user4.save()

@pytest.fixture()
def books(django_user_model, users):
    Book.objects.create(
      title   = 'Book 1',
      isbn    = '123',
      author  = django_user_model.objects.get(username = 'user1')
    )
    Book.objects.create(
      title   = 'Book 2',
      isbn    = '456',
      author  = django_user_model.objects.get(username = 'user2')
    )

@pytest.fixture()
def rusers(django_user_model):
    add_rbook     = Permission.objects.get(codename = 'add_rbook')
    view_rbook    = Permission.objects.get(codename = 'view_rbook')
    change_rbook  = Permission.objects.get(codename = 'change_rbook')
    delete_rbook  = Permission.objects.get(codename = 'delete_rbook')

    editors  = Group.objects.create(name = 'reditors')

    user1    = django_user_model.objects.create(
                 username      = 'ruser1',
                 is_superuser  = False,
                 is_staff      = False
               )
    user1.set_password('password'),
    user1.save()

    user2    = django_user_model.objects.create(
                 username      = 'ruser2',
                 is_superuser  = False,
                 is_staff      = False
               )
    user2.set_password('password'),
    user2.groups.add(editors)
    user2.save()

    user3    = django_user_model.objects.create(
                 username      = 'ruser3',
                 is_superuser  = False,
                 is_staff      = False
               )
    user3.set_password('password'),
    #
    # user3.user_permissions.add(delete_rbook)
    #   this successfully adds a permission that has_perm() can detect,
    #   but then an actual test of delete() fails
    #
    user3.save()

@pytest.fixture()
def rbooks(django_user_model, rusers):
    RBook.objects.create(
      title   = 'RBook 1',
      isbn    = '123',
      author  = django_user_model.objects.get(username = 'ruser1')
    )
    RBook.objects.create(
      title   = 'RBook 2',
      isbn    = '456',
      author  = django_user_model.objects.get(username = 'ruser3')
    )
