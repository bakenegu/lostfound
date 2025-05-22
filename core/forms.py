from django import forms
from .models import LostItem, FoundItem

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['title', 'description', 'date_lost', 'location', 'contact_info']
        widgets = {
            'date_lost': forms.DateInput(attrs={'type': 'date'}),
        }


class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ['title', 'description', 'photo', 'location']
