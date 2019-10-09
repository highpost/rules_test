from    rest_framework.permissions    import   (AllowAny,
                                                IsAuthenticated,
                                                IsAdminUser,
                                                IsAuthenticatedOrReadOnly,
                                                DjangoModelPermissions,
                                                DjangoModelPermissionsOrAnonReadOnly,
                                                DjangoObjectPermissions)
from    rest_framework.generics       import   (CreateAPIView,
                                                ListAPIView,
                                                RetrieveAPIView,
                                                UpdateAPIView,
                                                DestroyAPIView)
from    django.contrib.auth.mixins    import    LoginRequiredMixin, PermissionRequiredMixin
from    ..models                      import    Book, RBook
from    .serializers                  import    BookSerializer, RBookSerializer


class BookAuthCreateAPIView(LoginRequiredMixin, PermissionRequiredMixin, CreateAPIView):
    queryset             = Book.objects.all()
    serializer_class     = BookSerializer
    permission_classes   = (DjangoModelPermissions,)
    permission_required  = 'books.add_book'


class BookAuthRetrieveAPIView(LoginRequiredMixin, PermissionRequiredMixin, RetrieveAPIView):
    lookup_field         = 'title'
    queryset             = Book.objects.all()
    serializer_class     = BookSerializer
    permission_classes   = (DjangoModelPermissions,)
    permission_required  = 'books.view_book'


class BookAuthListAPIView(LoginRequiredMixin, PermissionRequiredMixin, ListAPIView):
    queryset             = Book.objects.all()
    serializer_class     = BookSerializer
    permission_classes   = (DjangoModelPermissions,)
    permission_required  = 'books.view_book'


class BookAuthUpdateAPIView(LoginRequiredMixin, PermissionRequiredMixin, UpdateAPIView):
    lookup_field         = 'title'
    queryset             = Book.objects.all()
    serializer_class     = BookSerializer
    permission_classes   = (DjangoModelPermissions,)
    permission_required  = 'books.change_book'


class BookAuthDestroyAPIView(LoginRequiredMixin, PermissionRequiredMixin, DestroyAPIView):
    lookup_field         = 'title'
    queryset             = Book.objects.all()
    serializer_class     = BookSerializer
    permission_classes   = (DjangoModelPermissions,)
    permission_required  = 'books.delete_book'


from    rules.contrib.views           import    PermissionRequiredMixin


class BookRulesCreateAPIView(LoginRequiredMixin, PermissionRequiredMixin, CreateAPIView):
    queryset             = RBook.objects.all()
    serializer_class     = RBookSerializer
    permission_classes   = (DjangoObjectPermissions,)
    permission_required  = 'books.add_rbook'


class BookRulesRetrieveAPIView(LoginRequiredMixin, PermissionRequiredMixin, RetrieveAPIView):
    lookup_field         = 'title'
    queryset             = RBook.objects.all()
    serializer_class     = RBookSerializer
    permission_classes   = (DjangoObjectPermissions,)
    permission_required  = 'books.view_rbook'


class BookRulesListAPIView(LoginRequiredMixin, PermissionRequiredMixin, ListAPIView):
    queryset             = RBook.objects.all()
    serializer_class     = RBookSerializer
    permission_classes   = (DjangoObjectPermissions,)
    permission_required  = 'books.view_rbook'


class BookRulesUpdateAPIView(LoginRequiredMixin, PermissionRequiredMixin, UpdateAPIView):
    lookup_field         = 'title'
    queryset             = RBook.objects.all()
    serializer_class     = RBookSerializer
    permission_classes   = (DjangoObjectPermissions,)
    permission_required  = 'books.change_rbook'


class BookRulesDestroyAPIView(LoginRequiredMixin, PermissionRequiredMixin, DestroyAPIView):
    lookup_field         = 'title'
    queryset             = RBook.objects.all()
    serializer_class     = RBookSerializer
    permission_classes   = (DjangoObjectPermissions,)
    permission_required  = 'books.delete_rbook'
