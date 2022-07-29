import django_filters
from django_filters import CharFilter
from django.forms.widgets import TextInput
from stocks.models import *

class ItemFilter(django_filters.FilterSet):
    title = CharFilter(field_name='name', lookup_expr='icontain', widget= TextInput(attrs={
        'placeholder' : 'search',
        'class' : 'form-control'
    }))

    class Meta:
        model = Product
        fields = ['name', 'category']
        