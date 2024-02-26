from django.db import models
from django.contrib.auth.models import User
from book.models import Book

class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    borrowed_books = models.ManyToManyField(Book, related_name="books")
    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super(UserAccount, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.first_name
    