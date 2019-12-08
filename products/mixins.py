from django.views.generic.base import ContextMixin
from .models import Category
from personal_cabinet.models import Favorite
from .models import Research

from orders.cart import Cart as SessionCart
from django.contrib import messages


class CategoryContextMixin(ContextMixin):

	def add_to_cart(self, request, **kwargs):
		ADDED = 50
		NOT_ADDED = 60
		research_slug = request.GET.get('add_to_cart')

		research = Research.objects.get(slug=research_slug)
		success_message = '<span class="font-weight-bold">"%s"</span>, по цене <span class="text-nowrap font-weight-bold">%s руб.</span><br />' % (research.title, research.nominal)
		cart = SessionCart(request)
		if cart.add(research):
			messages.add_message(request, ADDED, success_message)
		else:
			messages.add_message(request, NOT_ADDED, 'Исследование уже в корзине')
		# if self.request.user.is_authenticated:
		# 	cart = Cart.objects.get(client__user=self.request.user)
		# 	try:
		# 		CartItem.objects.get(research__slug=self.request.GET.get('add_to_cart'), cart=cart)
		# 		messages.add_message(request, NOT_ADDED, 'Исследование уже в корзине')
		# 	except:
		# 		cartitem = CartItem.objects.get_or_create(research=research, cart=cart)[0]
		# 		cartitem.price = research.nominal
		# 		cartitem.save()
		# 		messages.add_message(request, ADDED, success_message)
		# else:
		# 	cart = SessionCart(request)
		#
		# 	for item in SessionCart(request):
		# 		if item.get_product() in CartItem.objects.filter(research=research):
		# 			messages.add_message(request, NOT_ADDED, 'Исследование уже в корзине')
		# 			break
		# 	else:
		# 		CartItem.objects.create(research=research)
		# 		item = CartItem.objects.latest()
		# 		cart.add(item, item.research.nominal)
		# 		messages.add_message(request, ADDED, success_message)

	def add_to_favorite(self, request, **kwargs):
		ADDED = 70
		NOT_ADDED = 80
		if self.request.GET.get('add_to_favorite'):
			research = Research.objects.get(slug=self.request.GET.get('add_to_favorite'))
			if self.request.user.is_authenticated:
				favorite = Favorite.objects.get(client__user=self.request.user)
				try:
					Favorite.objects.get(research__slug=self.request.GET.get('add_to_favorite'), client__user=self.request.user)
					messages.add_message(request, NOT_ADDED, 'Исследование уже в избранном')
				except:
					favorite.save()
					favorite.research.add(research)
					messages.add_message(request, ADDED, 'Исследование успешно добавлено в избранное')
			else:
				messages.add_message(request, messages.ERROR, 'Войдите, прежде чем добавлять товар в избранное')

	def dispatch(self, request, *args, **kwargs):
		if request.GET.get('add_to_cart'):
			self.add_to_cart(request)
		self.add_to_favorite(request)
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["categories"] = Category.objects.all()
		return context
