from django.db import models
from django.core.validators import MinValueValidator

from usermanagement.models import Librarian,DeliveryMan,Reader
from library_management.models import Book

class Library(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.TextField(max_length=1000)
    librarian = models.OneToOneField(Librarian, on_delete=models.PROTECT)
    subscription_fee = models.IntegerField(validators=[MinValueValidator(0.0)])

    def get_books(self)->list:
        pass

    def lend_book(self, book:Book, reader:Reader):
        pass

    def get_librarian(self)->Librarian:
        return self.librarian

    def deliveryman_paid(self,deliveryman:DeliveryMan, amount:int)->None:
        deliveryman.cash_balance -= amount
        deliveryman.save()

    def ban_user(self, reader:Reader)->None:
        pass

    def fine_user(self, reader:Reader, amount: int)->None:
        pass

    def __str__(self)->str:
        return f'{self.name} is managed by {self.librarian.username} in {self.address}. To join pay {self.subscription_fee}'
    
    def get_books(self) -> list[Book]:
        return Book.objects.filter(library = self)

    def get_available_book_list(self)->list[Book]:
        pass

# Create your models here.
