from django.db import models

from library_management.models import Library
from user_management.models import Reader

from django.core.validators import MaxValueValidator, MinValueValidator

class Book(models.Model):

    class Languages(models.TextChoices):
        tamil = 'Tamil'
        english = 'English'
        sinhala = 'Sinhala'

    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.IntegerField(validators=[MinValueValidator(0.0)])
    language = models.CharField(
        max_length = 10,
        choices=Languages.choices,
        default=Languages.tamil)
    quality = models.IntegerField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['name'],name='name_index'),
            models.Index(fields=['author'],name='author_index'),
            models.Index(fields=['language'],name='language_index')
        ]

    def __str__(self)->str:
        return f'{self.name} is  written by {self.author} in {self.language} for a price of {self.price}. It is currently in {self.library} with {self.quality} quality.'
    

class Wishlist(models.Model):
    ID = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['book'],name='book_index')
        ]
        unique_together = ['book','reader']
# Create your models here.