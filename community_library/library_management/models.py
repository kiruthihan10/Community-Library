from django.db import models
from django.core.validators import MinValueValidator
from user_management.models import Librarian, DeliveryMan, Reader

class Library(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.TextField(max_length=1000)
    librarian = models.OneToOneField(Librarian, on_delete=models.PROTECT)
    subscription_fee = models.IntegerField(validators=[MinValueValidator(0.0)])

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='library_name_index')
        ]
        unique_together = ['name', 'address']

    def __str__(self)->str:
        return f'{self.name} is managed by {self.librarian.username} in {self.address}. To join pay {self.subscription_fee}'
    
    def deliveryman_paid(self,deliveryman:DeliveryMan, amount:int)->None:
        payment = Payment.objects.get(deliveryman = deliveryman, library = self)
        payment.decrese_amount(amount)
        payment.save()

    def ban_reader(self, reader:Reader)->None:
        member = MemberShip.objects.get(lib=self, reader=reader)
        member.ban()

    def fine_user(self, reader:Reader, amount:int)->None:
        pass

class MemberShip(models.Model):
    ID = models.AutoField(primary_key=True)
    lib = models.ForeignKey(Library, on_delete = models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete = models.CASCADE)
    banned = models.BooleanField(default=0)
    fine = models.IntegerField(default=0,validators=[MinValueValidator(0.0)])

    class Meta:
        indexes = [
            models.Index(fields=['reader'],name='member_index')
        ]
        unique_together = ['lib','reader']

    def __str__(self)->str:
        ban_status = "banned" if self.banned else ""
        return f'{self.reader} is {ban_status} member of {self.library}'

    def ban(self)->None:
        self.banned = True
        self.save()

    def unban(self)->None:
        self.banned = False
        self.save()

    def add_fine(self, amount:int)->int:
        self.fine += amount
        self.save()
        return self.fine

    def pay_fine(self, amount:int, deliveryman: DeliveryMan)->int:
        self.fine -= amount
        self.save()
        payment = Payment.objects.get(deliveryman=deliverymanm, library=self.lib)
        payment.increase_amount(amount)
        return self.fine

    def pay_membership_fee(self, deliveryman: DeliveryMan)->None:
        payment = Payment.objects.get(deliveryman=deliveryman, library=self.lib)
        payment.increase_amount(self.lib.subscription_fee)

# Create your models here.

class Payment(models.Model):
    ID = models.AutoField(primary_key=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    deliveryman = models.ForeignKey(DeliveryMan, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0.0)])

    class Meta:
        indexes = [
            models.Index(fields=['library'],name='library_payment_index'),
            models.Index(fields=['deliveryman'],name='deliveryman_payment_index')
        ]
        unique_together=['library','deliveryman']

    def __str__(self)->None:
        return f'{self.deliveryman} owe {self.library} Rs {self.amount}'

    def increase_amount(self, amount:int):
        if type(amount) != int:
            raise TypeError
        self.amount += amount
        self.save()

    def decrese_amount(self, amount:int):
        if type(amount) != int:
            raise TypeError
        if self.amount - amount < 0:
            raise ValueError
        self.amount -= amount
        self.save()