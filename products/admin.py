from django.contrib import admin
from .models import Category, Research, IndividualResearchFeedback
from mptt.admin import DraggableMPTTAdmin
from seo.admin import ModelInstanceSeoInline

class ResearchAdmin(admin.ModelAdmin):
	inlines = [ModelInstanceSeoInline]
	prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(DraggableMPTTAdmin):
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(IndividualResearchFeedback)