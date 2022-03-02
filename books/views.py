import json
import requests as requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm
from django.contrib.auth.decorators import login_required
from .filters import BookFilter
from rest_framework import viewsets, filters
from .serializer import BookSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from loguru import logger


class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('title', 'author', 'public_date')
    search_fields = ['title', 'author', 'public_date']
    ordering_fields = '__all__'
    ordering = ('title',)

    def get_queryset(self):
        all_books_from_db = Book.objects.all()
        return all_books_from_db

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BookSerializer(instance)
        return Response(serializer.data)


def all_books(request):
    all_book_from_db = Book.objects.all()
    return render(request, 'books.html', {'books_from_html': all_book_from_db})


@login_required()
def new_book(request):
    form = BookForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(all_books)

    return render(request, 'book_form.html', {'form': form})


@login_required()
def edit_book(request, id):
    book = get_object_or_404(Book, pk=id)
    form = BookForm(request.POST or None, instance=book)

    if form.is_valid():
        form.save()
        return redirect(all_books)

    return render(request, 'book_form.html', {'form': form})


@login_required()
def delete_book(request, id):
    book = get_object_or_404(Book, pk=id)

    if request.method == "POST":
        book.delete()
        return redirect(all_books)
    return render(request, 'submit.html', {'book': book})


def search_book(request):
    founds_book = BookFilter(request.GET, queryset=Book.objects.all())
    return render(request, 'search.html', {'books_from_html': founds_book})


def import_book_from_google(request):
    search_book_phrase = request.GET.get('phrase')
    logger.info(search_book_phrase)
    result = []

    if search_book_phrase is not None:
        try:
            logger.info(type(search_book_phrase))
            url = f"https://www.googleapis.com/books/v1/volumes?q={search_book_phrase}"
            logger.info("url adres is {}", url)
            res = requests.get(url)
            book_from_google = json.loads(res.content)
            logger.info(book_from_google['items'])

            result = mapping_books_to_table(book_from_google['items'])
            for book in result:
                book.save()

        except KeyError:
            pass

    return render(request, 'import_books.html', {'import_books_from_google': result})


def mapping_books_to_table(imported_book_from_google):
    books_table = []
    for book_form_google in imported_book_from_google:
        print(book_form_google)

        book = Book()
        try:
            book.title = str(book_form_google['volumeInfo']['title'])
            print(book.title)
        except KeyError:
            book.title = 'brak informacji'
        try:
            book.author = str(book_form_google['volumeInfo']['authors'][0])
        except KeyError:
            book.author = 'brak informacji o autorze'
        try:
            book.public_date = int(book_form_google['volumeInfo']['publishedDate'])
        except KeyError:
            book.public_date = 0
        try:
            book.isbn_number = str(book_form_google['volumeInfo']['industryIdentifiers'][0]['identifier'])
        except KeyError:
            book.isbn_number = 0
        try:
            book.number_of_pages = int(book_form_google['volumeInfo']['pageCount'])
        except KeyError:
            book.number_of_pages = 0
        try:
            book.language = str(book_form_google['volumeInfo']['language'])
        except KeyError:
            book.language = 'brak informacji'
        try:
            book.link_to_cover = 'brak informacji'
        except KeyError:
            book.link_to_cover = 'empty'
        books_table.append(book)

    return books_table
