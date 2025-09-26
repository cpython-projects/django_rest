from django.utils import timezone
from rest_framework import serializers
from .models import Author, Publisher, Book





class BookSerializer(serializers.ModelSerializer):
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all())
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True, required=False)

    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('include_related'):
            representation['genres'] = ['111', '222', '333']
        else:
            representation.pop('genres', None)
        return representation
    #
    # def create(self, validated_data):
    #     authors = validated_data.pop('authors', [])
    #
    #     book = Book.objects.create(**validated_data)
    #     book.authors.set(authors)
    #
    #     return book
    #
    # def update(self, instance, validated_data):
    #     authors = validated_data.pop('authors', None)
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #
    #     instance.save()
    #     if authors is not None:
    #         instance.authors.set(authors)
    #     return instance
    #
    #




class ListOfPublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'website']


class DetailPublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class CreatePublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'established_date', 'website']

    def create(self, validated_data):
        if 'established_date' not in validated_data:
            validated_data['established_date'] = timezone.now()
        return Publisher.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.website = validated_data.get('website', instance.website)

        instance.save()
        return instance

        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        #
        # instance.save()
        # return instance

class AuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

# class AuthorsListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = ['id', 'first_name', 'last_name',]


class BookListSerializer(serializers.ModelSerializer):
    publisher = serializers.StringRelatedField()
    authors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'publisher', 'authors', 'published_date', 'is_bestseller']