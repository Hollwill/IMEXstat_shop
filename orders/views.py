from django.views import generic
from .models import Cart
from cart.cart import Cart as SessionCart
from products.models import Research

class CartListView(generic.ListView):
	context_object_name = 'research'
	template_name = 'orders/cart_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			context['cart'] = Cart.objects.get(client__user_id=self.request.user.id)
		else:
			context['cart'] = SessionCart(self.request)
		return context


	def get_queryset(self):
		if self.request.GET.get('remove_from_cart'):
			if self.request.user.is_authenticated:
				research = Research.objects.get(slug=self.request.GET.get('remove_from_cart'))
				cart = Cart.objects.get(client_id=self.request.user.id)
				cart.save()
				cart.research.remove(research)
		return Research.objects.filter(cart__client__user_id=self.request.user.id)

