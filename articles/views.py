from django.views import generic
from .models import Article, ArticleCategory, ArticleAuthor

from seo.mixins.views import (
    ModelInstanceViewSeoMixin,
)

class ArticlesListView(generic.ListView):
	context_object_name = 'articles'

	def get_queryset(self):
		return Article.objects.all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["categories"] = ArticleCategory.objects.all()
		return context

class ArticleCategoryListView(generic.ListView):
	context_object_name = 'articles'

	def get_queryset(self):
		return Article.objects.filter(category__slug=self.kwargs['slug'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["categories"] = ArticleCategory.objects.all()
		return context

class ArticleDetailView(ModelInstanceViewSeoMixin, generic.DetailView):
	model = Article

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		article = self.get_object()
		context["articles"] = Article.objects.exclude(id=article.id).filter(category__in=article.category.all()).distinct()
		context["author"] = ArticleAuthor.objects.get(article=article)
		return context