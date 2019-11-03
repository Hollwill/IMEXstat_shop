from django.urls import path
from .views import CartListView, CartPurchaseView

app_name='orders'

urlpatterns = [
	path('cart/', CartListView.as_view(), name='cart'),
	path('cart/purchase/', CartPurchaseView.as_view(), name='cart_purchase')
]