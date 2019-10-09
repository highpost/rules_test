from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import BookCreateForm, BookUpdateForm, RBookCreateForm, RBookUpdateForm
from .models import Book, RBook


class BookAuthCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookCreateForm
    template_name = 'books/book_create.html'
    permission_required = 'books.add_book'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:auth-detail',
                 kwargs    = {'title': self.object.title})

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookAuthDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = 'books/book_detail.html'
    permission_required = 'books.view_book'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:auth-detail',
                 kwargs    = {'title': self.object.title})

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookAuthListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Book
    template_name = 'books/book_list.html'
    permission_required = 'books.view_book'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:auth-list')

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookAuthUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookUpdateForm
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = 'books/book_update.html'
    permission_required = 'books.change_book'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:auth-detail',
                 kwargs    = {'title': self.object.title})

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookAuthDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = 'books/book_delete.html'
    permission_required = 'books.delete_book'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:book-home')

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


from rules.contrib.views import PermissionRequiredMixin


class BookRulesCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = RBook
    form_class = RBookCreateForm
    template_name = 'books/book_rules_create.html'
    permission_required = 'books.add_rbook'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:rules-detail',
                 kwargs    = {'title': self.object.title})

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookRulesDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = RBook
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = 'books/book_rules_detail.html'
    permission_required = 'books.view_rbook'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:rules-detail',
                 kwargs    = {'title': self.object.title})

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookRulesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = RBook
    template_name = 'books/book_rules_list.html'
    permission_required = 'books.view_rbook'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:rules-list')

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookRulesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RBook
    form_class = RBookUpdateForm
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = 'books/book_rules_update.html'
    permission_required = 'books.change_rbook'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:rules-detail',
                 kwargs    = {'title': self.object.title})

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookRulesDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = RBook
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = 'books/book_rules_delete.html'
    permission_required = 'books.delete_rbook'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:book-home')

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


from rules.contrib.views import AutoPermissionRequiredMixin


class BookRulesAVTCreateView(AutoPermissionRequiredMixin, CreateView):
    model = RBook
    form_class = RBookCreateForm
    template_name = 'books/book_rules_create.html'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:rules-avt-detail',
                 kwargs    = {'title': self.object.title})

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookRulesAVTDetailView(AutoPermissionRequiredMixin, DetailView):
    model = RBook
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = 'books/book_rules_detail.html'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:rules-avt-detail',
                 kwargs    = {'title': self.object.title})

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookRulesAVTListView(AutoPermissionRequiredMixin, ListView):
    model = RBook
    template_name = 'books/book_rules_list.html'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:rules-avt-list')

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookRulesAVTUpdateView(AutoPermissionRequiredMixin, UpdateView):
    model = RBook
    form_class = RBookUpdateForm
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = 'books/book_rules_update.html'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:rules-avt-detail',
                 kwargs    = {'title': self.object.title})

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')


class BookRulesAVTDeleteView(AutoPermissionRequiredMixin, DeleteView):
    model = RBook
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = 'books/book_rules_delete.html'

    def get_success_url(self):
        return reverse(
                 viewname  = 'books_web_app:book-home')

    def handle_no_permission(self):
        return redirect(
                 to  = 'books_web_app:book-home')
