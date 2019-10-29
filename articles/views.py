from django.views import generic
from .models import Article, ArticleCategory, ArticleAuthor

from seo.mixins.views import (
    ModelInstanceViewSeoMixin,
)
from personal_cabinet.models import Client
from django.contrib import messages


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
        context["articles"] = Article.objects.exclude(id=article.id).filter(
            category__in=article.category.all()).distinct()
        context["author"] = ArticleAuthor.objects.get(article=article)
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            slug = request.GET['sent_article']
            client = Client.objects.get(user=request.user)
            article = Article.objects.get(slug=request.GET['sent_article'])
            if article.sent_file_in_mail(client) == 1:
                messages.add_message(request, messages.INFO, 'Почта была успешно отправлена')
            else:
                messages.add_message(request, messages.INFO, 'Почта не была отправлена')
        finally:
            return super(ArticleDetailView, self).dispatch(request, *args, **kwargs)
