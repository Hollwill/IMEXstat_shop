from django.views import generic
from .models import Handbook


class HandbookList(generic.ListView):
	model = Handbook