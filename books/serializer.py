from .models import Book
from rest_framework import serializers

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'language', 'isbn_number', 'number_of_pages', 'public_date', 'link_to_cover']
