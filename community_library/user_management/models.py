from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Reader(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    address = models.TextField(max_length = 100)
    ratings = models.FloatField(
        default=2.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )

    def __str__(self)->str:
        return f'{self.get_full_name()} is on {self.address}'

    @property
    def user_name(self)->str:
        return self.user.username

class Librarian(models.Model):
    reader = models.OneToOneField(Reader, on_delete=models.CASCADE, primary_key = True)

class DeliveryMan(models.Model):
    reader = models.OneToOneField(Reader, on_delete=models.CASCADE, primary_key = True)

# Create your models here.
