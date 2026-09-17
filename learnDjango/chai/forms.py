from django import forms
from .models import ChaiVarity


class ChaiVarietyForm(forms.Form):

    chai_variety = forms.ModelChoiceField(
        queryset=ChaiVarity.objects.all(),
        label="Select Chai Variety",
        widget=forms.Select(attrs={
            'class': 'bg-black text-white border border-gray-600 rounded-lg px-4 py-2'
        })
    )
    
    