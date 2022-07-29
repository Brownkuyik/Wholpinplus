from django.contrib import admin
from .models import *

# Register your models here.
class productInline(admin.StackedInline):
    model = Product
    admin.site.register(Product)




class categoryInline(admin.TabularInline):
    model = Category
    admin.site.register(Category)
 


admin.site.register(Order)
admin.site.register(OrderGoods)
admin.site.register(Payment)
admin.site.register(Address)
