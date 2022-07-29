from django import forms


class CheckoutForm(forms.Form):
    street_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder':'nwaiba road',
        'class':'form-control'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': '24',
        'class': 'form-control'
    }))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': '+234 7384762774',
        'class': 'form-control'
    }))
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)