from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.CharField(initial=1,
    label=False, 
    widget=forms.NumberInput(attrs={
        'min': 1,
        'max': 99,
        'type': 'number',
        'class': 'cart-item__cnt'
    }))
    override = forms.BooleanField(required=False,
    initial=False, widget=forms.HiddenInput)
