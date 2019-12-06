from django.contrib import admin
from .models import Tasks, Feedback, ClientsImages, MenuManagement, Products


class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('name', 'contact_details', 'date')
	readonly_fields = ['date']


class TasksAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'priority']
	list_editable = ['priority']


admin.site.register(MenuManagement)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(ClientsImages)
admin.site.register(Products)