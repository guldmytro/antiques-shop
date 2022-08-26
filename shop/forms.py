from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'placeholder': 'Поиск',
        'class': 'form-search__input',
        'type': 'search',
        }))