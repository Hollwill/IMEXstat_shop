from django.contrib import admin
from .models import Category, Research, IndividualResearchFeedback
from mptt.admin import DraggableMPTTAdmin
from seo.admin import ModelInstanceSeoInline

class ResearchAdmin(admin.ModelAdmin):
	inlines = [ModelInstanceSeoInline]
	prepopulated_fields = {'slug': ('title',)}
	list_filter = ('category', 'research_type')
	list_display = ('__str__', 'stock', 'discount', 'nominal', 'has_image', 'has_file')
	# readonly_fields = ['has_image']
	list_editable = ('stock', 'discount', 'nominal')

	def has_image(self, obj):
		if obj.image:
			return True
		else:
			return False
	has_image.boolean = True
	has_image.short_description = 'Изображение'

	def has_file(self, obj):
		if obj.demo:
			return True
		else:
			return False
	has_file.boolean = True
	has_file.short_description = 'Демо файл'

class CategoryAdmin(DraggableMPTTAdmin):
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(IndividualResearchFeedback)