from django.shortcuts import render
from stocks.models import Category, Product

from django.views.generic import ListView

from Purchase.filters import ItemFilter





# Create your views here.
class Home_page(ListView):
    def get(self, *arges, **kwargs):

        category = Category.objects.all()
        product = Product.objects.all()
        filtes = ItemFilter(self.request.GET, queryset=product)
        items = filtes.qs
        context ={
            'filt':items,
            'pro':product,
            'cat':category
        }
        return render(self.request, 'pages/home_page.html')


def About_page(request):
    return render(request, 'pages/about.html')


class ClothsViews(ListView):
    def get(self, *arges, **kwargs):

        category = Category.objects.all()
        product = Product.objects.all()
        filtes = ItemFilter(self.request.Get, queryset=Product)
        items = filtes.qs
        context ={
            'filt':items,
            'pro':product,
            'cat':category
        }
        return render(self.request, 'pages/cloth.html', context)

