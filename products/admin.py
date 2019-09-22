from django.contrib import admin
from .models import Category, Research

class ResearchAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Research, ResearchAdmin)
