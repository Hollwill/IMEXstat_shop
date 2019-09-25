from django.shortcuts import render

from products.models import Research
from django.views import generic

class IndexList(generic.ListView):
	context_object_name = 'research'
	template_name = 'index/index.html'

	def get_queryset(self):
		return Research.objects.all().order_by('-pk')[:3]


