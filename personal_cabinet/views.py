from .models import Client
from .forms import ProfileForm, RequizitesForm
from multi_form_view import MultiModelFormView
from django.urls import reverse


class ProfileFormView(MultiModelFormView):
	form_classes = {
	'requizites_form': RequizitesForm,
	'profile_form': ProfileForm
	}
	template_name = 'personal_cabinet/pk_settings.html'

	def get_objects(self):
		self.client_slug = self.kwargs.get('slug', None)
		client = Client.objects.get(user=self.request.user)
		return {
			'requizites_form': client,
			'profile_form': client
		}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["client"] = Client.objects.get(user=self.request.user)
		return context

	def get_success_url(self):
		return reverse('lk_settings')

	def forms_valid(self, forms):
		profile = forms['profile_form'].save()
		requizites = forms['requizites_form'].save()
		profile.save()
		requizites.save()
		return super(ProfileFormView, self).forms_valid(forms)