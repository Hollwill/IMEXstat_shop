from django.contrib import admin
from solo.admin import SingletonModelAdmin
from nested_admin.nested import NestedStackedInline, NestedModelAdmin, InlineModelAdmin
from .models import Tasks, Feedback, ClientsImages, MenuManagement, Products, Contacts, ContactsPhone, ContactsOffice, \
	ContactsOfficeImage, ContactsTeam


class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('name', 'contact_details', 'date')
	readonly_fields = ['date']


class TasksAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'priority']
	list_editable = ['priority']


class ContactsPhoneInline(admin.TabularInline):
	model = ContactsPhone


class ContactsOfficeImageInline(admin.TabularInline):
	model = ContactsOfficeImage


class ContactsOfficeInline(NestedStackedInline):
	model = ContactsOffice
	inlines = [
		ContactsOfficeImageInline
	]


class ContactsTeamInline(NestedStackedInline):
	model = ContactsTeam


class ContactsAdmin(NestedModelAdmin, SingletonModelAdmin):
	inlines = [
		ContactsPhoneInline,
		ContactsOfficeInline,
		ContactsTeamInline,
	]


admin.site.register(Contacts, ContactsAdmin)
admin.site.register(MenuManagement)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(ClientsImages)
admin.site.register(Products)
