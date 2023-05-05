from django import forms
from auctions.models import *


class EditForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
