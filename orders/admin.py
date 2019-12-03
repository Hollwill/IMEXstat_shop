from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	readonly_fields = ['price']
	raw_id_field = ['research']


class OrderAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'date', 'paid', 'get_total_cost')

	readonly_fields = ['date']
	list_filter = ['paid', 'date']
	inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)

