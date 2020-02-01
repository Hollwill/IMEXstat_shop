from products.models import Research
from .models import Tasks, ClientsImages, Products, Contacts
from django.views import generic
from .forms import ProfileForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from seo.mixins.models import SeoTagsMixin
def autocomplete(request):
	if request.is_ajax():
		queryset = Research.objects.filter(title__icontains=request.GET.get('search'))
		research_list = []
		for i in queryset:
			research_list.append(i.title)
		data = {
			'list': research_list
		}
		return JsonResponse(data)


class IndexFormView(generic.FormView):
	form_class = ProfileForm


	def form_valid(self, form):
		form.save()
		messages.add_message(self.request, messages.INFO,
							 'Наши менеджеры обязательно свяжутся с Вами и ответят на все Ваши вопросы.')

		return HttpResponseRedirect(self.success_url)


class IndexList(IndexFormView,  generic.TemplateView):
	template_name = 'index/index.html'
	success_url = reverse_lazy('index:index')

	def get_context_data(self, *args, **kwargs):
		context = super(IndexList, self).get_context_data(**kwargs)
		context['tasks'] = Tasks.objects.all()
		context['products'] = Products.objects.all()
		context['clients_images'] = ClientsImages.objects.all()
		return context


class ContactsList(generic.TemplateView):
	template_name = 'index/contacts.html'

	def get_context_data(self, **kwargs):
		context = super(ContactsList, self).get_context_data(**kwargs)
		context['contacts'] = Contacts.get_solo()
		return context



class InnView(generic.TemplateView, IndexFormView):
	template_name = 'index/inn.html'
	success_url = reverse_lazy('index:inn')


class AnalysisView(generic.TemplateView, IndexFormView):
	template_name = 'index/analysis.html'
	success_url = reverse_lazy('index:analysis')


class Analysis2View(generic.TemplateView, IndexFormView):
	template_name = 'index/analysis2.html'
	success_url = reverse_lazy('index:analysis2')


class ElectionView(generic.TemplateView, IndexFormView):
	template_name = 'index/election.html'
	success_url = reverse_lazy('index:election')


class SearchView(generic.TemplateView, IndexFormView):
	template_name = 'index/search.html'
	success_url = reverse_lazy('index:search')


class RobotsView(generic.TemplateView):
	template_name = 'robots.txt'