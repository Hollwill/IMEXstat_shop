from products.models import Research
from .models import Products
from .models import Tasks, ClientsImages
from django.views import generic
from .forms import ProfileForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse


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

	def get_success_url(self):
		return self.request.GET['next']

	def get_template_names(self):
		try:	
			if self.request.GET['next'] == '/':
				return ['index/index.html']
			elif self.request.GET['next'] == '/inn/':
				return ['index/inn.html']
		except:
			return [self.template_name]

	def form_valid(self, form):
		form.save()
		messages.add_message(self.request, messages.INFO, 'Наши менеджеры обязательно свяжутся с Вами и ответят на все Ваши вопросы.')
		return HttpResponseRedirect(self.get_success_url())


class IndexList(generic.TemplateView, IndexFormView):
	template_name = 'index/index.html'

	def get_context_data(self, *args, **kwargs):
		context = super(IndexList, self).get_context_data(**kwargs)
		context['tasks'] = Tasks.objects.all()
		context['products'] = Products.objects.all()
		context['clients_images'] = ClientsImages.objects.all()
		return context

class ContactsList(generic.TemplateView):
	template_name = 'index/contacts.html'

class InnView(generic.TemplateView, IndexFormView):
	template_name = 'index/inn.html'