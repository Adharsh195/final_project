from django import forms
from .models import Provider, ProviderService

class ProviderEditForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['company_name', 'phone', 'address']


class ProviderServicePriceForm(forms.ModelForm):
    class Meta:
        model = ProviderService
        fields = ['price']
        widgets = {
            'price': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'form-control'
            })
        }