from django.views import generic
from .models import Research
from orders.models import Cart
from cart.cart import Cart as SessionCart
from .mixins import CategoryContextMixin
from django.urls import reverse_lazy, reverse
from .forms import IndividualResearchFeedbackForm, CartItemCreateForm
from seo.mixins.views import ModelInstanceViewSeoMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages



class IndividualResearchFeedbackView(generic.CreateView):
    form_class = IndividualResearchFeedbackForm
    template_name = 'products/research_individual_order.html'
    success_url = reverse_lazy('research:individual')

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, 'Ваш заказ был принят, мы скоро с вами свяжемся')
        return super().form_valid(form)


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


class ResearchListView(generic.ListView, CategoryContextMixin):
    context_object_name = 'researchs'

    def get_queryset(self):
        if self.request.GET.get('research'):
            return Research.objects.filter(title__icontains=self.request.GET.get('research'))
        else:
            try:
                return Research.objects.filter(research_type=self.kwargs['type'])
            except KeyError:
                return Research.objects.all()


class ResearchCategoryListView(generic.ListView, CategoryContextMixin):
    context_object_name = 'researchs'

    def get_queryset(self):
        return Research.objects.filter(category__slug=self.kwargs['slug'])


class ResearchDetailView(ModelInstanceViewSeoMixin, generic.DetailView, CategoryContextMixin):
    model = Research


class ResearchBuyView(ModelInstanceViewSeoMixin, generic.DetailView, CategoryContextMixin, generic.CreateView):
    model = Research
    form_class = CartItemCreateForm
    template_name = 'products/research_buy.html'

    def get_success_url(self):
        return reverse('index:index')

    def get_context_data(self, *args, **kwargs):
        context = super(ResearchBuyView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            model_instance = form.save(commit=False)
            model_instance.research = Research.objects.get(slug=self.kwargs['slug'])
            model_instance.cart = Cart.objects.get(client__user=self.request.user)
            model_instance.save()
        else:
            model_instance = form.save(commit=False)
            model_instance.research = Research.objects.get(slug=self.kwargs['slug'])
            model_instance.save()
            cart = SessionCart(self.request)
            cart.add(model_instance, model_instance.research.nominal)
        return HttpResponseRedirect(self.get_success_url())
