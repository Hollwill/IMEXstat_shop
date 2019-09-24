from django.contrib import admin
from .models import Order, Cart

class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'research', 'update_frequency', 'duration', 'cost', 'date')
    exclude = ['cost']



admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
