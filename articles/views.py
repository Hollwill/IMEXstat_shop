from django.views import generic
from .models import Article, ArticleCategory, ArticleAuthor

from seo.mixins.views import (
    ModelInstanceViewSeoMixin,
)
from personal_cabinet.models import Client


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

    '''def sent_article_mail(self, request, *args, **kwargs):
        article = Article.objects.get(slug=request.GET['sent_article'])

        media_root = settings.MEDIA_ROOT
        message = EmailMessage('Ваша статья сэр',
                               'Прикрепляю статью к сообщению',
                               'from@example.com',
                               ['to@email.com'])
        message.attach_file('%s/%s' % (media_root, article.article_pdf))
        message.send()'''

    def dispatch(self, request, *args, **kwargs):
        try:
            client = Client.objects.get(user=request.user)
            article = Article.objects.get(slug=request.GET['sent_article'])
            article.sent_file_in_mail(client)
        finally:
            return super(ArticleDetailView, self).dispatch(request, *args, **kwargs)
