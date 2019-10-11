from django.shortcuts import render

from products.models import Research
from .models import Tasks, ClientsImages
from django.views import generic
from .forms import ProfileForm
from django.http import HttpResponseRedirect
from django.contrib import messages

class IndexFormView(generic.FormView):
	form_class = ProfileForm


	def get_success_url(self):
		return self.request.GET['next']


	def form_valid(self, form):
		form.save()
		messages.add_message(self.request, messages.INFO, 'Запрос успешно отправлен, скоро мы вам ответим.')
		return HttpResponseRedirect(self.get_success_url())



class IndexList( generic.ListView, IndexFormView ):
	context_object_name = 'research'
	template_name = 'index/index.html'

	def get_queryset(self):
		return Research.objects.all().order_by('-pk')[:3]

	def get_context_data(self, *args, **kwargs):
		context = super(IndexList, self).get_context_data(**kwargs)
		context['tasks'] = Tasks.objects.all()
		context['clients_images'] = ClientsImages.objects.all()
		return context

class ContactsList(generic.TemplateView):
	template_name = 'index/contacts.html'

class InnView(generic.TemplateView, IndexFormView):
	template_name = 'index/inn.html'