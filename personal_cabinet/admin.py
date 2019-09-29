from django.contrib import admin

from orders.models import Cart

from .models import (
    Client
)
class CartInline(admin.TabularInline):
	model = Cart

class ClientAdmin(admin.ModelAdmin):
	inlines = [
		CartInline
	]

admin.site.register(Client, ClientAdmin)
