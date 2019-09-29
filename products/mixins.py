from django.views.generic.base import ContextMixin
from .models import Category
from personal_cabinet.models import Client
from .models import Research
from orders.models import Cart
from cart.cart import Cart as SessionCart


class CategoryContextMixin(ContextMixin):
	additional_context = None
	

	def add_to_cart(self, request, **kwargs):
		if self.request.GET.get('add_to_cart'):
			research = Research.objects.get(slug=self.request.GET.get('add_to_cart'))
			if self.request.user.is_authenticated:
				
				cart = Cart.objects.get(client__user=self.request.user)
				try:
					Cart.objects.get(research__slug=self.request.GET.get('add_to_cart'), client__user=self.request.user)
					self.additional_context = 'Исследование уже в корзине'
				except:
					cart.save()
					cart.research.add(research)
					self.additional_context = 'Исследование успешно добавлено'
			else:
				cart = SessionCart(request)
				if cart.have(research):
					self.additional_context = ' Исследование уже добавлено в корзину'
				else:
					cart.add(research, research.OM_cost)
					self.additional_context = 'Исследование успешно добавлено'



	def dispatch(self, request, *args, **kwargs):
		self.add_to_cart(request)
		return super(CategoryContextMixin, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if not self.additional_context == None:
			context['message'] = self.additional_context
		context["categories"] = Category.objects.all()
		return context