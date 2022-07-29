from urllib.parse import uses_params
from django.urls import reverse
from django.conf import settings
from django.db import models

# Create your models here.
class Category(models.Model):
    Name = models.CharField(max_length=20, help_text='Enter the categoty of the product')

    def __str__(self):
        return self.Name



class Product(models.Model):
    name = models.CharField(max_length=50, help_text='enter the product name')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    desc = models.CharField(max_length=250, help_text='Enter the product')
    slug = models.SlugField(default='http')
    image = models.ImageField(upload_to=f'media/')
    fprice= models.IntegerField(help_text='first price')
    lprice = models.IntegerField(help_text='Last price')
    is_available = models.BooleanField(default=True)


    def __str__(self) -> str:
        return f"{self.category} is {self.name}"
        

    def get_absolute_url(self):
        return reverse("pages/home_page.html", kwargs={'slug':self.slug})
    
    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug':self.slug})
    def get_remove_add_to_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug':self.slug})


class Users(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)



class OrderGoods(Users):
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.quantity} of {self.item.name}"

    def get_total_price(self):
        return self.quantity * self.item.price

    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price
    
    
    def get_amount_saved(self):
        return self.get_total_price() - self.get_total_discount_price()
    
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_price()


class Order(Users):
    ref_code =models.CharField(max_length=230)
    items = models.ManyToManyField(OrderGoods)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True,blank=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True,blank=True)
    being_delivered = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)



    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total +=order_item.get_last_price()
        return total
	


class Address(Users):
    street = models.CharField(max_length=250)
    house_number = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=300)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paystack_id = models.CharField(max_length=30)
    amount = models.FloatField()
    buy_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

