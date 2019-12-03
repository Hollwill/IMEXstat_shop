from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client, Favorite
from orders.models import Cart

@receiver(post_save, sender=User)
def create_user_client(sender, instance, created, **kwargs):
	if created:
		Client.objects.create(user=instance)
		client = Client.objects.get(user=instance)
		Cart.objects.create(client=client)
		Favorite.objects.create(client=client)
		client.email = instance.email
		client.save()
