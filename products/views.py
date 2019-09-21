from django.views import generic
from .models import(
    Research,
    Category
)
from .mixins import CategoryContextMixin

class ResearchListView(generic.ListView, CategoryContextMixin):
    context_object_name = 'researchs'

    def get_queryset(self):
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
