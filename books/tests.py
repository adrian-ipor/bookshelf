from django.test import TestCase
from django.urls import  resolve, reverse
from .views import import_book_from_google, all_books
# Create your tests here.
class bookshelfTests(TestCase):

    def test_url_books(self):
        url = reverse('all_books')
        self.assertEquals(resolve(url).func, all_books)