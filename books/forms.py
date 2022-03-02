from django.forms import ModelForm
from .models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'public_date', 'isbn_number', 'number_of_pages', 'language', 'link_to_cover']