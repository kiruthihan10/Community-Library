from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Reader(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    address = models.TextField(max_length = 100)
    ratings = models.FloatField(
        default=2.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )

    def __str__(self)->str:
        return f'{self.get_full_name()} is on {self.address}'

    def finish_book(self):
        pass

    def get_Notifications(self)->list:
        pass

    def view_wishlist(self)->list:
        pass

class Librarian(models.Model):
    reader = models.OneToOneField(Reader, on_delete=models.CASCADE)

class DeliveryMan(models.Model):
    reader = models.OneToOneField(Reader, on_delete=models.CASCADE)
    cash_balance = models.IntegerField(
        validators=[MinValueValidator(0.0)]
    )
    
# Create your models here.
