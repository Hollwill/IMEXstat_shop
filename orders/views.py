from django.views import generic
from personal_cabinet.models import Client
from .models import Cart, Order, OrderItem
from cart.cart import Cart as SessionCart
from products.models import Research
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from multi_form_view import MultiModelFormView
from .forms import EntityForm, IndividualForm


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


@method_decorator(login_required, name='dispatch')
class CartPurchaseView(MultiModelFormView):
	form_classes = {
	'entity_form': EntityForm,
	'individual_form': IndividualForm,
	}
	template_name = 'orders/cart_purchase.html'


	def get_objects(self):
		self.client_slug = self.kwargs.get('slug', None)
		client = Client.objects.get(user=self.request.user)
		order = Order.objects.create(client=client)
		return {
		'entity_form': client,
		'individual_form': client,
		}
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def get_success_url(self):
		return reverse('/')

	def forms_valid(self, forms):
		profile = forms['entity_form'].save()
		requizites = forms['individual_form'].save()
		'''order = forms['order_items'].save()
								order.save()'''
		profile.save()
		requizites.save()
		return super(CartPurchaseView, self).forms_valid(forms)
'''
@method_decorator(login_required, name='dispatch')
class CartPurchaseView(generic.edit.CreateView):
	model = Order
	fields = ['client', ]
	template_name = 'orders/cart_purchase.html'
'''