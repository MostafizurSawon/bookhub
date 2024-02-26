from django.db import models
from .constants import TRANSACTION_TYPES
from users.models import UserAccount

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPES)
    balance_after_transaction = models.DecimalField(max_digits=8, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.amount)