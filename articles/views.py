from django.views import generic
from .models import Article, ArticleCategory, ArticleAuthor

from seo.mixins.views import (
    ModelInstanceViewSeoMixin,
)
from personal_cabinet.models import Client, Favorite
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

    def sent_mail(self, request):
        try:
            client = Client.objects.get(user=request.user)
            article = Article.objects.get(slug=request.GET['sent_article'])
            if article.sent_file_in_mail(client, request) == 1:
                messages.add_message(request, messages.INFO, 'Почта была успешно отправлена')
            else:
                messages.add_message(request, messages.INFO, 'Почта не была отправлена')
        except:
            pass

    def add_to_favorite(self, request, **kwargs):
        ADDED = 70
        NOT_ADDED = 80
        if self.request.GET.get('add_to_favorite'):
            article = Article.objects.get(slug=self.request.GET.get('add_to_favorite'))
            if self.request.user.is_authenticated:
                favorite = Favorite.objects.get(client__user=self.request.user)
                try:
                    Favorite.objects.get(articles__slug=self.request.GET.get('add_to_favorite'),
                                         client__user=self.request.user)
                    messages.add_message(request, NOT_ADDED, 'Исследование уже в избранном')

                except:
                    favorite.save()
                    favorite.articles.add(article)
                    messages.add_message(request, ADDED, 'Исследование успешно добавлено в избранное')
            else:
                messages.add_message(request, messages.ERROR, 'Войдите, прежде чем добавлять статью в избранное')

    def dispatch(self, request, *args, **kwargs):
        self.sent_mail(request)
        self.add_to_favorite(request)
        return super(ArticleDetailView, self).dispatch(request, *args, **kwargs)
