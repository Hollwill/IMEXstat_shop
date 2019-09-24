from django.views import generic
from .models import(
    Research,
    Category
)
from orders.models import Cart
from .mixins import CategoryContextMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse


class ResearchListView(generic.ListView, CategoryContextMixin):
    context_object_name = 'researchs'
    def get_queryset(self):
        if self.request.GET.get('research'):
            return Research.objects.filter(title__icontains=self.request.GET.get('research'))
        else:
            try:
                return Research.objects.filter(research_type=self.kwargs['type'])
            except KeyError:
                return Research.objects.all()


            
class ResearchCategoryListView(generic.ListView, CategoryContextMixin):
    context_object_name = 'researchs'

    def get_queryset(self):
        return Research.objects.filter(category__slug=self.kwargs['slug'])

class ResearchDetailView(generic.DetailView, CategoryContextMixin):
    model = Research
    
class ResearchBuyView(generic.DetailView, CategoryContextMixin):
    model = Research
    template_name = 'products/research_buy.html'

