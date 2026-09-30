from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


    
class Transaction(models.Model):
    TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    description = models.TextField(
        blank=True
    )

    date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.type} - {self.amount}"