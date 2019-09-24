from .models import Client
from django.contrib.auth.models import User
from orders.models import Cart
from .forms import ProfileForm, RequizitesForm
from multi_form_view import MultiModelFormView
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

@method_decorator(login_required, name='dispatch')
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
		return reverse('lk:settings')

	def forms_valid(self, forms):
		profile = forms['profile_form'].save()
		requizites = forms['requizites_form'].save()
		profile.save()
		requizites.save()
		return super(ProfileFormView, self).forms_valid(forms)

class RegisterFormView(FormView):
    form_class = UserCreationForm

    template_name = "registration/register.html"

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        user = User.objects.get(username=form.cleaned_data['username'])
        Client.objects.create(user=user)
        client = Client.objects.get(user=user)
        Cart.objects.create(client=client)
        return super(RegisterFormView, self).form_valid(form)