from    rest_framework.serializers    import    ModelSerializer, SlugRelatedField
from    django.contrib.auth           import    get_user_model
from    ..models                      import    Book, RBook


class BookSerializer(ModelSerializer):
    author  = SlugRelatedField(
                queryset    = get_user_model().objects.all(),
                many        = False,
                read_only   = False,
                slug_field  = 'username'
             )

    class Meta:
        model   = Book
        fields  = '__all__'


class RBookSerializer(ModelSerializer):
    author  = SlugRelatedField(
                queryset    = get_user_model().objects.all(),
                many        = False,
                read_only   = False,
                slug_field  = 'username'
             )

    class Meta:
        model   = RBook
        fields  = '__all__'
