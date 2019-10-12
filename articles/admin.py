from django.contrib import admin

from .models import ArticleCategory, Article, ArticleAuthor
from seo.admin import ModelInstanceSeoInline


class ArticleAdmin(admin.ModelAdmin):
	inlines = [ModelInstanceSeoInline]
	prepopulated_fields = {'slug': ('title',)}

class ArticleCategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(ArticleAuthor)
