from django.contrib.auth import get_user_model
from django.db.models import CharField, ForeignKey, Model, CASCADE
from django.urls import reverse


#
# simple Book model
#
class Book(Model):
    title = CharField(max_length = 100)
    isbn = CharField(max_length = 50, unique = True)
    author = ForeignKey(to = get_user_model(), on_delete = CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
                 viewname  = 'books:book-detail',
                 kwargs    = {'pk': self.pk})


from rules import is_authenticated, is_group_member, predicate
from rules.contrib.models import RulesModel


@predicate
def is_book_author(user, book):
    if not book:
        return False
    return book.author == user

is_editor = is_group_member('reditors')


#
# modified Book model for testing Rules
#
class RBook(RulesModel):
    title = CharField(max_length = 100)
    isbn = CharField(max_length = 50, unique = True)
    author = ForeignKey(to = get_user_model(), on_delete = CASCADE)

    class Meta:
        rules_permissions = {
                               'add':     is_authenticated,
                               'view':    is_authenticated,
                               'change':  is_book_author | is_editor,
                               'delete':  is_book_author
                            }

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
                 viewname  = 'books:book-rules-detail',
                 kwargs    = {'pk': self.pk})
