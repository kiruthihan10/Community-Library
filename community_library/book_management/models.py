from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from library_management.models import Library
from usermanagement.models import Reader

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
        choices=Languages.choices,
        default=Languages.tamil)
    quality = models.IntegerField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    def get_past_borrowers()->list[Reader]:
        pass

    def __str__(self)->str:
        return f'{self.name} is  written by {self.author} in {self.language} for a price of {self.price}. It is currently in {self.library} with {self.quality} quality.'
    
# Create your models here.
