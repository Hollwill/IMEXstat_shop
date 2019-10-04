from django.views import generic
from personal_cabinet.models import Client
from .models import Cart, Order, OrderItem
from cart.cart import Cart as SessionCart
from products.models import Research
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from multi_form_view import MultiFormView
from .forms import EntityForm, IndividualForm, Formset
from django.urls import reverse
from django import forms


import datetime
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
class CartPurchaseView(MultiFormView):
	form_classes = {
			'entity_form': EntityForm,
			'individual_form': IndividualForm,
			'order_form': Formset
	}
	template_name = 'orders/cart_purchase.html'



	def get_initial(self):
		initial = super(CartPurchaseView, self).get_initial()
		client = Client.objects.get(user=self.request.user)
		c = client

		initial['entity_form'] = {
			'lastname': c.lastname, 
			'firstname': c.firstname,
			'firm_name': c.firm_name,
			'email': c.email,
			'phone': c.phone,
			'INN': c.INN,
			'KPP': c.KPP
		}
		initial['individual_form'] = {
			'lastname': c.lastname, 
			'firstname': c.firstname,
			'email': c.email,
			'phone': c.phone,
		}
		return initial
		
	def get_success_url(self):
		return reverse('/')

	def forms_valid(self, forms):
		profile = forms['entity_form'].save()
		requizites = forms['individual_form'].save()
		requizites.save()
		return super(CartPurchaseView, self).forms_valid(forms)


'''
@method_decorator(login_required, name='dispatch')
class CartPurchaseView(generic.edit.FormView):
	template_name = 'orders/cart_purchase.html'
	form_class = CartResearchForm
	success_url = '/'
	now = datetime.datetime.now()

	def get_context_data(self, **kwargs):
		data = super(CartPurchaseView, self).get_context_data(**kwargs)
		cart = Cart.objects.get(client__user=self.request.user)
		research = cart.research.all()
		FormSet = forms.formset_factory(CartResearchForm, max_num=len(research))
		formset = FormSet(initial=[{'research': x.id} for x in research])
		data['cart'] = formset
		data['research'] = research
		return data

	def post(self, request, *args, **kwargs):

		
		cart = Cart.objects.get(client__user=self.request.user)
		research = cart.research.all()
		FormSet = forms.formset_factory(CartResearchForm, max_num=len(research))
		formset = FormSet(request.POST or None)
		form = formset
		if formset.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)


	def form_valid(self, form):
		client = Client.objects.get(user=self.request.user)
		Order.objects.create(client=client)
		order = Order.objects.latest()
		for item in form:
			order_cart = item.save(commit=False)
			order_cart.order = order
			order_cart.save()
		Cart.objects.get(client__user=self.request.user).delete()
		Cart.objects.create(client=client)

		return super().form_valid(form)
'''