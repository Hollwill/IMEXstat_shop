from django.contrib import admin
from .models import Category, Research

from seo.admin import ModelInstanceSeoInline

class ResearchAdmin(admin.ModelAdmin):
	inlines = [ModelInstanceSeoInline]
	prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Research, ResearchAdmin)
