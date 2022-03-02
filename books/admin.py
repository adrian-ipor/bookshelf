from django.contrib import admin
from .models import Book

# admin.site.register(Book)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ['title', 'author', 'public_date', 'isbn_number', 'number_of_pages', 'language', 'link_to_cover']
    # exclude = ['title']
    list_display = ['title', 'author', 'public_date']
    list_filter = ['author', 'public_date']
    search_fields = ['title', 'author']
