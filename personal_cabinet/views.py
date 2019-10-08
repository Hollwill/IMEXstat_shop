from .models import Client, Favorite
from django.contrib.auth.models import User
from orders.models import Cart
from .forms import ProfileForm, RequizitesForm
from multi_form_view import MultiModelFormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from cart.cart import Cart as SessionCart
from products.models import Research

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

		return super(ProfileFormView, self).forms_valid(forms)
@method_decorator(login_required, name='dispatch')
class FavoriteArticles(generic.TemplateView):
	template_name = 'personal_cabinet/favorite_articles.html'


@method_decorator(login_required, name='dispatch')
class FavoriteReports(generic.TemplateView):
	template_name = 'personal_cabinet/favorite_reports.html'


@method_decorator(login_required, name='dispatch')
class FavoriteResearchs(generic.ListView):
	model = Favorite
	template_name = 'personal_cabinet/favorite_research.html'
	context_object_name = 'research'

	def delete_from_favorite(self, request, *args, **kwargs):
		if self.request.GET.get('delete_from_favorite'):
			research = Research.objects.get(slug=self.request.GET.get('delete_from_favorite'))

			favorite = Favorite.objects.get(client__user=self.request.user)
			favorite.save()
			favorite.research.remove(research)

	def dispatch(self, request, *args, **kwargs):
		self.delete_from_favorite(request)
		return super(FavoriteResearchs, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		favorite = Favorite.objects.get(client__user=self.request.user)
		return Research.objects.filter(favorite=favorite)


class RegisterFormView(generic.edit.FormView):
    form_class = UserCreationForm

    template_name = "registration/register.html"

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        SessionCart(self.request)
        form.save()
        cart = Cart.objects.get(client__user__username=form.cleaned_data['username'])
        #сохранение корзины из сессии в аккаунт
        for item in SessionCart(self.request):
        	id = item.product.id
        	cart.research.add(Research.objects.get(id=id))
        return super(RegisterFormView, self).form_valid(form)

