from django.views import generic
from .models import(
    Research,
    Category
)
from .mixins import CategoryContextMixin
from django.views import View

class ResearchListView(generic.ListView, CategoryContextMixin):
    context_object_name = 'researchs'

    def get_queryset(self):
        if self.request.GET.get('research'):
            return Research.objects.filter(title__icontains=self.request.GET.get('research'))
        else:
            return Research.objects.filter(research_type=self.kwargs['type'])

class ResearchCategoryListView(generic.ListView, CategoryContextMixin):
    context_object_name = 'researchs'

    def get_queryset(self):
        return Research.objects.filter(category_id=self.kwargs['pk'])

class ResearchDetailView(generic.DetailView, CategoryContextMixin):
    model = Research
    
class ResearchBuyView(generic.DetailView, CategoryContextMixin):
    model = Research
    template_name = 'products/research_buy.html'
