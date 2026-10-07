from django import forms
from .models import Transaction, Category


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = [
            "category",
            "type",
            "amount",
            "description",
            "date",
        ]

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter amount",
                    "min": "0",
                    "step": "0.01"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter description",
                    "rows": 3
                }
            ),

            "date" :forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["category"].queryset = Category.objects.filter(
                user=user
            )
        else:
            self.fields["category"].queryset = Category.objects.none()