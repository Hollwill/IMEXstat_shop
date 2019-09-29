from django.views import generic
from .models import Cart
from cart.cart import Cart as SessionCart
from products.models import Research

class CartListView(generic.ListView):
	context_object_name = 'cart'
	template_name = 'orders/cart_list.html'

	def get_queryset(self):
		if self.request.user.is_authenticated:
			return Cart.objects.get(client__user_id=self.request.user.id)
		else:
			return SessionCart(self.request)

	def dispatch(self, request, *args, **kwargs):
		self.remove_from_cart(request)
		return super(CartListView, self).dispatch(request, *args, **kwargs)
			
	def remove_from_cart(self, request, **kwargs):
		if self.request.GET.get('remove_from_cart'):
			research = Research.objects.get(slug=self.request.GET.get('remove_from_cart'))

			if self.request.user.is_authenticated:
				cart = Cart.objects.get(client_id=self.request.user.id)
				cart.save()
				cart.research.remove(research)
			else:
				cart = SessionCart(self.request)
				cart.remove(research)

