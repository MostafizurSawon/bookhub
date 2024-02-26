from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    borrow_price = models.DecimalField(max_digits=6, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name="categories")
    image = models.ImageField(upload_to='book/media/uploads/', blank = True, null = True)
    
    def __str__(self):
        return self.title