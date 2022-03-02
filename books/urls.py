from django.urls import path
from books.views import all_books, new_book, delete_book, edit_book, import_book_from_google, search_book


urlpatterns = [
    path('all/', all_books, name="all_books"),
    path('add/', new_book, name="add_book"),
    path('edit/<int:id>/', edit_book, name="edit_book"),
    path('delete/<int:id>/', delete_book, name="delete_book"),
    path('search/', search_book, name='search'),
    path('import', import_book_from_google, name="import_books")

]
