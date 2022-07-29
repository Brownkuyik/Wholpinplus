from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View



from .forms import CheckoutForm
from stocks.models import *

from pypaystack import Transaction
import string
import random
from django.http import JsonResponse

# Create your views here.


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item = OrderGoods.objects.get_or_create(
        item = item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order-item.save()
            messages.info(request, 'The quantity of this item was added')
            return redirect("buy:order_summary")
        else:
            messages.info(request, f"Dear {order_qs} theitem has been added to cart")
            order.items.add(order_item)
            return redirect('buy:order_summary')  
    else:
        ordered_date = timezone.now()
        orders = Order.objects.create(user=request.user, ordered_date=ordered_date)
        orders.items.add(order_item)
        messages.info(request, "this item was added to your cart")
        return redirect("buy:order_sumarry")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderGoods.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, f"Dear {order_qs} this item was removed from your cart")
            return redirect('k_store:homePage')
        else:
            messages.info(request, f"Dear {order_qs} This item is not in your cart")
            return redirect('product_page', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('k_store:homePage', slug=slug)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderGoods.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated")
            return redirect('order_summary')
        else:
            messages.info(request, "This item is not in your cart")
            return redirect('k_store:homePage', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('k_store:homePage', slug=slug)

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order

            }
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update({'default_shipping_address': shipping_address_qs[0]})

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("buy:checkout")

        return render(self.request, "pages/home_page.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:

                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        street = address_qs[0]
                        order.shipping_address = street
                        order.save()
                        
                    else:
                        messages.info(self.request, "No default address")
                        return redirect("buy:checkout")
                else:
                    print('User is entering new adrress')

                    street = form.cleaned_data.get('street_address')
                    house_number = form.cleaned_data.get('apartment_address')
                    phone_number = form.cleaned_data.get('phone_number')
                    # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                    # save_info = form.cleaned_data.get('save_info')

                    if is_valid_form([street, phone_number]):
                        shipping_address = Address(
                            user=self.request.user,
                            street=street,
                            house_number=house_number,
                            phone_number=phone_number,
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                            return redirect('buy:f_checkout')

                    else:
                        messages.info(self.request, "Please fill in the requred ")
                return redirect('buy:f_checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have active orders")
            return redirect('buy:checkout')


def final_checkout(request):
    order = Order.objects.get(user=request.user, ordered=False)
    if order.shipping_address:
        context = {
            'order': order,
        }
        return render(request, 'pages/final_checkout.html', context)
    else:
        messages.warning(request, "You have not added an address")
        return redirect("buy:checkout")

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=18))
class PaymentView(View):
    def get(self, *args, **kwargs):
        transaction = Transaction(authorization_key='s')
        response = transaction.verify(kwargs['id'])
        data = JsonResponse(response, safe=False)

        if response[3]:
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                payment = Payment()
                payment.paystack_id = kwargs['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "order was successful")
                return redirect("/")
            except ObjectDoesNotExist:
                messages.success(self.request, "Your order was successful")
                return redirect("/")
        else:
            messages.danger(self.request, "Could not verify the transaction")
            return redirect("/")


