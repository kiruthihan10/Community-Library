from django.db import models

from book_management.models import Book
from user_management.models import Reader, DeliveryMan

from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import date, timedelta

class Borrowel(models.Model):
    ID = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True)
    deadline = models.DateField(default=date.today() + timedelta(days=7))
    start_quality = models.IntegerField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    end_quality = models.IntegerField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    class Meta:
        indexes = [
            models.Index(models.F('end_quality')-models.F('start_quality'),name='quality_reduction'),
            models.Index(fields=['-deadline','start_date'],name='Date_difference_index'),
            models.Index(fields=['book'],name='borrowel_book_index'),
            models.Index(fields=['reader'],name='borrowel_reader_index')
        ]
        unique_together = ['book','start_date']

    def get_quality_different(self):
        return 0 if self.end_quality is None else self.start_quality - self.end_quality

    def extend_permite_day(self)->None:
        self.deadline += timedelta(days=7)

    def return_book(self, quality:int = 3, date:type(date.today()) = date.today()):
        self.return_date = date
        self.end_quality = quality
        self.save()

class Request(models.Model):
    ID = models.AutoField(primary_key=True)
    user = models.ForeignKey(Reader,on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    Date_applied = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['book'],name='book_request_index'),
            models.Index(fields=['Date_applied'],name='applied_date_index'),
        ]
        unique_together = ['user','book']

class Notification(models.Model):
    ID = models.AutoField(primary_key=True)
    head = models.CharField(max_length=20, null=True)
    body = models.TextField(max_length=500)
    user = models.ForeignKey(Reader,on_delete=models.CASCADE)

class Complaints(models.Model):
    ID = models.AutoField(primary_key=True)
    by = models.ForeignKey(Reader, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on = models.ForeignKey(DeliveryMan, on_delete=models.CASCADE)

# Create your models here.
