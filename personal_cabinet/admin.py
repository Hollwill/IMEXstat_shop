from django.contrib import admin

from orders.models import Cart

from .models import (
    Client,
	Favorite
)
class CartInline(admin.TabularInline):
	model = Cart

class FavoriteInline(admin.TabularInline):
	model = Favorite

class ClientAdmin(admin.ModelAdmin):
	inlines = [
		CartInline,
		FavoriteInline
	]

admin.site.register(Client, ClientAdmin)
