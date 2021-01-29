from django import forms 
from .models import UserDetails

class EditItemForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ('profession','institute', 'institute_id', 'first_name', 'last_name')
class ItemForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ('gender', 'profession','institute', 'institute_id', 'first_name', 'last_name')