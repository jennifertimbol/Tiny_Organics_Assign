from django import forms
from .models import Customer, Child

class childForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'allergies']
        labels = {
            'allergies' : "List any allergies your child may have"
        }