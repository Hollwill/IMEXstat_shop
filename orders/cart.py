import datetime
from . import models

CART_ID = 'CART-ID'


class ItemAlreadyExists(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class Cart:
    def __init__(self, request):
        if not request.user.is_authenticated:
            cart_id = request.session.get(CART_ID)
            if cart_id:
                try:
                    cart = models.Cart.objects.get(id=cart_id)
                except models.Cart.DoesNotExist:
                    cart = self.new(request)
            else:
                cart = self.new(request)
        else:
            cart = models.Cart.objects.get(client__user=request.user)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.cartitem_set.all():
            yield item

    def new(self, request):
        cart = models.Cart()
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    def add(self, research):
        try:
            models.CartItem.objects.get(
                cart=self.cart,
                research=research,
            )
            return False
        except models.CartItem.DoesNotExist:
            item = models.CartItem()
            item.cart = self.cart
            item.research = research
            item.save()
            return True

    def remove(self, research):
        try:
            item = models.CartItem.objects.get(
                cart=self.cart,
                research=research,
            )
        except models.CartItem.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    # def update(self, product, quantity, unit_price=None):
    #     try:
    #         item = models.CartItem.objects.get(
    #             cart=self.cart,
    #             product=product,
    #         )
    #     except models.CartItem.DoesNotExist:
    #         raise ItemDoesNotExist
    #     else:  # ItemAlreadyExists
    #         if quantity == 0:
    #             item.delete()
    #         else:
    #             item.unit_price = unit_price
    #             item.quantity = int(quantity)
    #             item.save()

    def have(self, product):
        try:
            item = models.CartItem.objects.get(
                cart=self.cart,
                product=product,
            )
            return True
        except:
            return False

    def summary(self):
        result = self.cart.summary_price()
        return result

    def clear(self):
        for item in self.cart.cartitem_set.all():
            item.delete()