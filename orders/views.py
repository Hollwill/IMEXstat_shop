from django.views import generic
from personal_cabinet.models import Client
from .models import Cart, Order
from cart.cart import Cart as SessionCart
from products.models import Research
from multi_form_view import MultiFormView
from .forms import EntityForm, IndividualForm, CartResearchForm
from django.urls import reverse, reverse_lazy
from django import forms


class CartListView(generic.ListView):
    context_object_name = 'cart'
    template_name = 'orders/cart_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.get(client__user_id=self.request.user.id)
        else:
            return SessionCart(self.request)

    def dispatch(self, request, *args, **kwargs):
        self.remove_from_cart(request)
        return super(CartListView, self).dispatch(request, *args, **kwargs)

    def remove_from_cart(self, request, **kwargs):
        if self.request.GET.get('remove_from_cart'):
            research = Research.objects.get(slug=self.request.GET.get('remove_from_cart'))

            if self.request.user.is_authenticated:
                cart = Cart.objects.get(client_id=self.request.user.id)
                cart.save()
                cart.research.remove(research)
            else:
                cart = SessionCart(self.request)
                cart.remove(research)


# @method_decorator(login_required, name='dispatch')
class CartPurchaseView(MultiFormView):
    form_classes = {
        'entity_form': EntityForm,
        'individual_form': IndividualForm,
    }
    template_name = 'orders/cart_purchase.html'

    def dispatch(self, request, *args, **kwargs):
        self.remove_from_cart(request)
        return super(CartPurchaseView, self).dispatch(request, *args, **kwargs)

    def remove_from_cart(self, request, **kwargs):
        if self.request.GET.get('remove_from_order'):
            research = Research.objects.get(slug=self.request.GET.get('remove_from_order'))

            cart = Cart.objects.get(client_id=self.request.user.id)
            cart.save()
            cart.research.remove(research)

    def get_context_data(self, **kwargs):
        data = super(CartPurchaseView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = Cart.objects.get(client__user=self.request.user)
            research = cart.research.all()
        else:
            cart = SessionCart(self.request)
            research = [a for a in cart]

        FormSet = forms.formset_factory(CartResearchForm, max_num=len(research), min_num=len(research))
        formset = FormSet(initial=[{'research': x if self.request.user.is_authenticated else x.product} for x in research])
        data['researchs'] = research
        try:
            data['cart'] = kwargs['form']
        except:
            data['cart'] = formset
        finally:
            return data

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            cart = Cart.objects.get(client__user=self.request.user)
            research = cart.research.all()
        else:
            cart = SessionCart(self.request)
            research = [a.product for a in cart]
        FormSet = forms.formset_factory(CartResearchForm, max_num=len(research))
        formset = FormSet(request.POST or None)
        get_forms = self.get_forms()
        if formset.is_valid() and self.are_forms_valid(get_forms):
            self.form_valid(formset)
            return self.forms_valid(get_forms)
        elif not self.are_forms_valid(get_forms):
            return self.forms_invalid(get_forms)
        else:
            return self.form_invalid(formset)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            client = Client.objects.get(user=self.request.user)
            Order.objects.create(client=client)
        else:
            Order.objects.create()
        order = Order.objects.latest()
        for item in form:
            order_cart = item.save(commit=False)
            order_cart.order = order
            order_cart.save()
        if self.request.user.is_authenticated:
            Cart.objects.get(client__user=self.request.user).delete()
            Cart.objects.create(client=client)
        else:
            SessionCart(self.request).clear()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            client = Client.objects.get(user=self.request.user)
            initial['individual_form'] = {
                'lastname': client.lastname,
                'firstname': client.firstname,
                'email': client.email,
                'phone': client.phone
            }
            initial['entity_form'] = {
                'firm_name': client.firm_name,
                'INN': client.INN,
                'KPP': client.KPP
            }
        return initial

    def get_success_url(self):
        return reverse('index:index')

    def forms_valid(self, forms):
        if self.request.user.is_authenticated:
            client = Client.objects.get(user=self.request.user)
            client.firstname = forms['individual_form'].cleaned_data['firstname']
            client.lastname = forms['individual_form'].cleaned_data['lastname']
            client.email = forms['individual_form'].cleaned_data['email']
            client.phone = forms['individual_form'].cleaned_data['phone']
            client.firm_name = forms['entity_form'].cleaned_data['firm_name']
            client.INN = forms['entity_form'].cleaned_data['INN']
            client.KPP = forms['entity_form'].cleaned_data['KPP']
            client.save()
        else:
            order = Order.objects.latest()
            order.firstname = forms['individual_form'].cleaned_data['firstname']
            order.lastname = forms['individual_form'].cleaned_data['lastname']
            order.email = forms['individual_form'].cleaned_data['email']
            order.phone = forms['individual_form'].cleaned_data['phone']
            order.firm_name = forms['entity_form'].cleaned_data['firm_name']
            order.INN = forms['entity_form'].cleaned_data['INN']
            order.KPP = forms['entity_form'].cleaned_data['KPP']
            order.save()
        return super(CartPurchaseView, self).forms_valid(forms)
