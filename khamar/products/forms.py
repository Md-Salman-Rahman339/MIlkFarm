from django import forms
from .models import Review,Product

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'


class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['product','user','comment']