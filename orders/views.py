from django.views import generic
from .models import Cart
from products.models import Research

class CartListView(generic.ListView):
	context_object_name = 'research'
	template_name = 'orders/cart_list.html'

	def get_queryset(self):
		if self.request.GET.get('add_to_cart'):
			research = Research.objects.get(slug=self.request.GET.get('add_to_cart'))
			cart = Cart.objects.get(client_id=self.request.user.id)
			cart.save()
			cart.research.remove(research)
		return Research.objects.filter(cart__client__user_id=self.request.user.id)