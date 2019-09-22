from .models import Client
from .forms import ProfileForm, RequizitesForm
from django.views.generic.edit import FormView
from multi_form_view import MultiFormView
from django.urls import reverse
from django.views.generic import TemplateView

class ProfileSettingsView(TemplateView):
	template_name = 'personal_cabinet/pk_settings.html'

	def get(self, request, *args, **kwargs):
		profile_form = ProfileForm(self.request.GET or None)
		requizites_form = RequizitesForm(self.request.GET or None)
		context = self.get_context_data(**kwargs)
		context['profile_form'] = profile_form
		context['requizites_form'] = requizites_form
		context['client'] = Client.objects.get(user=self.request.user)
		return self.render_to_response(context)


class ProfileFormView(FormView):
	form_class = ProfileForm
	template_name = 'personal_cabinet/pk_settings.html'
	success_url = '/'



	def post(self, request, *args, **kwargs):
		profile_form = self.form_class(request.POST)
		requizites_form = RequizitesForm()
		if profile_form.is_valid():
			profile_form.save()
			return self.render_to_response(
				self.get_context_data(
					success=True
					)
				)
		else:
			return self.render_to_response(
				self.get_context_data(
					profile_form=profile_form,
					)
				)

class RequizitesFormView(FormView):
	form_class = RequizitesForm
	template_name = 'personal_cabinet/pk_settings.html'
	success_url = '/'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["client"] = Client.objects.get(user=self.request.user)
		return context

	def post(self, request, *args, **kwargs):
		requizites_form = self.form_class(request.POST)
		profile_form = ProfileForm()
		if requizites_form.is_valid():
			requizites_form.save()
			return self.render_to_response(
				self.get_context_data(
					success=True
					)
				)
		else:
			return self.render_to_response(
				self.get_context_data(
					requizites_form=requizites_form,
					)
				)

'''
class ProfileFormView(MultiFormView):
	form_classes = {
	'requizites': RequizitesForm,
	'profile': ProfileForm
	}
	template_name = 'personal_cabinet/pk_settings.html'

	def get_form_kwargs(self):
		kwargs = super(ProfileFormView, self).get_form_kwargs()
		kwargs['requizites']['prefix'] = 'avatar'
		kwargs['profile']['prefix'] = 'background'
		return kwargs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["client"] = Client.objects.get(user=self.request.user)
		return context

	def get_objects(self):
		self.client_slug = self.kwargs['slug']
		client = Client.objects.get(slug=self.client_slug)
		return {
		'requizites': client,
		'profile': client
		}

	def get_success_url(self):
		return reverse('research_list')

	def forms_valid(self, forms):
		profile = forms['profile'].save()
		requizites = forms['requizites'].save()
		return super(ProfileFormView, self).forms_valid(forms)

'''