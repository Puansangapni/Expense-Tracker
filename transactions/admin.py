from django.contrib import admin
from .models import Category, Transaction

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name", 
        "type", 
        "user", 
        "created_at",
    )
    list_filter = (
        "type",
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "description",
        "type",
        "amount",
        "category",
        "user",
    )

    list_filter = (
        "type",
        "category",
        "date",
    )

    search_fields = (
        "description",
    )
