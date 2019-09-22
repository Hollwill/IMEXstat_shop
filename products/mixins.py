from django.views.generic.base import ContextMixin
from .models import Category
from personal_cabinet.models import Client

class CategoryContextMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["client"] = Client.objects.get(user=self.request.user)
		context["categories"] = Category.objects.all()
		return context