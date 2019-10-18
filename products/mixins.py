from django.views.generic.base import ContextMixin
from .models import Category
from personal_cabinet.models import Client, Favorite
from .models import Research
from orders.models import Cart
from cart.cart import Cart as SessionCart
from django.contrib import messages

class CategoryContextMixin(ContextMixin):
	additional_context = None
	

	def add_to_cart(self, request, **kwargs):
		if self.request.GET.get('add_to_cart'):
			research = Research.objects.get(slug=self.request.GET.get('add_to_cart'))
			success_message = '<span class="font-weight-bold">"%s"</span>, по цене <span class="text-nowrap font-weight-bold">%s руб.</span><br />' % (research.title, research.OM_cost)
			if self.request.user.is_authenticated:
				cart = Cart.objects.get(client__user=self.request.user)
				try:
					Cart.objects.get(research__slug=self.request.GET.get('add_to_cart'), client__user=self.request.user)
					messages.add_message(request, messages.ERROR, 'Исследование уже в корзине')
				except:
					cart.save()
					cart.research.add(research)
					messages.add_message(request, messages.INFO, success_message)

			else:
				cart = SessionCart(request)
				if cart.have(research):
					messages.add_message(request, messages.ERROR, 'Исследование уже в корзине')
				else:
					cart.add(research, research.OM_cost)
					messages.add_message(request, messages.INFO, success_message)


	def add_to_favorite(self, request, **kwargs):
		if self.request.GET.get('add_to_favorite'):
			research = Research.objects.get(slug=self.request.GET.get('add_to_favorite'))
			if self.request.user.is_authenticated:
				favorite = Favorite.objects.get(client__user=self.request.user)
				try:
					Favorite.objects.get(research__slug=self.request.GET.get('add_to_favorite'), client__user=self.request.user)
					self.additional_context = 'Исследование уже в избранном'
				except:
					favorite.save()
					favorite.research.add(research)
					self.additional_context = 'Исследование успешно добавлено в избранное'
			else:
				self.additional_context = 'Войдите, прежде чем добавлять товар в избранное.'



	def dispatch(self, request, *args, **kwargs):
		self.add_to_cart(request)
		self.add_to_favorite(request)
		return super(CategoryContextMixin, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if not self.additional_context == None:
			context['message'] = self.additional_context
		context["categories"] = Category.objects.all()
		return context