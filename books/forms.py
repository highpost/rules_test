from django.contrib.auth import get_user_model
from django.forms import ModelForm, CharField
from .models import Book, RBook


class BookCreateForm(ModelForm):
    title = CharField()
    isbn = CharField()
    author = CharField()

    class Meta:
        model = Book
        fields = ('title', 'isbn', 'author')

    def clean_author(self):
        return get_user_model().objects.get(username = self.data.get('author'))


class BookUpdateForm(ModelForm):
    title = CharField()
    isbn = CharField()
    author = CharField()

    class Meta:
        model = Book
        fields = ('title', 'isbn', 'author')

    def clean_author(self):
        return get_user_model().objects.get(username = self.data.get('author'))


class RBookCreateForm(ModelForm):
    title = CharField()
    isbn = CharField()
    author = CharField()

    class Meta:
        model = RBook
        fields = ('title', 'isbn', 'author')

    def clean_author(self):
        return get_user_model().objects.get(username = self.data.get('author'))


class RBookUpdateForm(ModelForm):
    title = CharField()
    isbn = CharField()
    author = CharField()

    class Meta:
        model = RBook
        fields = ('title', 'isbn', 'author')

    def clean_author(self):
        return get_user_model().objects.get(username = self.data.get('author'))
