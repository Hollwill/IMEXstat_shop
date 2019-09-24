from django.views.generic.base import ContextMixin
from .models import Category
from personal_cabinet.models import Client
from .models import Research
from orders.models import Cart



class CategoryContextMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.GET.get('add_to_cart'):
			research = Research.objects.get(slug=self.request.GET.get('add_to_cart'))
			cart = Cart.objects.get(client__user=self.request.user)
			try:
				Cart.objects.get(research__slug=self.request.GET.get('add_to_cart'), client__user=self.request.user)
				context["message"] = 'Исследование уже в корзине'
			except:
				cart.save()
				cart.research.add(research)
				context["message"] = 'исследование успешно добавлено'
		
		context["categories"] = Category.objects.all()
		return context