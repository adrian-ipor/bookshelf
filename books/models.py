from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator
import datetime

current_year = datetime.date.today().year


class Book(models.Model):
    title = models.CharField(max_length=140, blank=False, unique=False, validators=[MinLengthValidator(3)])
    author = models.CharField(max_length=140, blank=False, unique=False, validators=[MinLengthValidator(3)])
    public_date = models.PositiveSmallIntegerField(blank=False, unique=False, validators=[
        MaxValueValidator(current_year)])
    isbn_number = models.CharField(blank=False, max_length=140)
    number_of_pages = models.PositiveSmallIntegerField(blank=False, validators=[MinValueValidator(1)])
    language = models.CharField(max_length=140, blank=False, validators=[MaxLengthValidator(3)])
    link_to_cover = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return self.title + ' (' + str(self.public_date) + ')'
