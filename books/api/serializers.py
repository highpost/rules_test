from    rest_framework.serializers    import    CharField, SlugRelatedField, Serializer
from    django.contrib.auth           import    get_user_model
from    ..models                      import    Book, RBook


class BookSerializer(Serializer):
    title   = CharField(max_length = 100)
    isbn    = CharField(max_length = 50)
    author  = SlugRelatedField(
                slug_field  = 'username',
                queryset    = get_user_model().objects.all(),
                many        = False,
                read_only   = False
             )

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title   = validated_data.get('title',  instance.title)
        instance.isbn    = validated_data.get('isbn',   instance.isbn)
        instance.author  = validated_data.get('author', instance.author)
        instance.save()
        return instance


class RBookSerializer(Serializer):
    title   = CharField(max_length = 100)
    isbn    = CharField(max_length = 50)
    author  = SlugRelatedField(
                slug_field  = 'username',
                queryset    = get_user_model().objects.all(),
                many        = False,
                read_only   = False
             )

    def create(self, validated_data):
        return RBook.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title   = validated_data.get('title',  instance.title)
        instance.isbn    = validated_data.get('isbn',   instance.isbn)
        instance.author  = validated_data.get('author', instance.author)
        instance.save()
        return instance
