from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=50)
    author=models.CharField(max_length=50)
    genre=models.CharField(max_length=50)
    description=models.TextField(null=True)
    mrp=models.PositiveIntegerField()
    rating = models.IntegerField(default = 0,validators=[MinValueValidator(0),MaxValueValidator(10)])
    rated_by = models.PositiveIntegerField(default = 1)
    class Meta:
        ordering=('title',)
    def __str__(self):
        return f'{self.title} by {self.author}'

class BookCopy(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    borrow_date=models.DateField(null=True)
    # 1 means available for issue, 0 means not
    status=models.BooleanField(default=False)
    borrower=models.ForeignKey(User,related_name='borrower',null=True,on_delete=models.SET_NULL)
    def __str__(self):
        return f'{self.book.title} , {str(self.borrow_date)}'

