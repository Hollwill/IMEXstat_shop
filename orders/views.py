from django.views import generic
from personal_cabinet.models import Client
from .models import Order
from orders.cart import Cart
from products.models import Research
from multi_form_view import MultiFormView
from .forms import EntityForm, IndividualForm, CartResearchForm
from django.urls import reverse
from django import forms


class CartListView(generic.TemplateView):
    template_name = 'orders/cart_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cart'] = Cart(self.request)
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('remove_from_cart'):
            self.remove_from_cart(request)
        return super(CartListView, self).dispatch(request, *args, **kwargs)

    def remove_from_cart(self, request, **kwargs):
        research = Research.objects.get(slug=self.request.GET.get('remove_from_cart'))
        cart = Cart(self.request)
        cart.remove(research)
        # if self.request.user.is_authenticated:
        #     cart = Cart.objects.get(client_id=self.request.user.id)
        #     CartItem.objects.get(cart=cart, research=research).delete()
        # else:
        #     cart = Cart(self.request)
        #     for item in cart:
        #         if item.get_product().research == research:
        #             cart.remove(item.product)


class CartPurchaseView(MultiFormView):
    form_classes = {
        'entity_form': EntityForm,
        'individual_form': IndividualForm,
    }
    template_name = 'orders/cart_purchase.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('remove_from_cart'):
            self.remove_from_cart(request)
        return super(CartPurchaseView, self).dispatch(request, *args, **kwargs)

    # def remove_from_cart(self, request, **kwargs):
    #     if self.request.GET.get('remove_from_order'):
    #         research = Research.objects.get(slug=self.request.GET.get('remove_from_order'))
    #
    #         if self.request.user.is_authenticated:
    #             cart = Cart.objects.get(client_id=self.request.user.id)
    #             CartItem.objects.get(cart=cart, research=research).delete()
    #         else:
    #             cart = Cart(self.request)
    #             for item in cart:
    #                 if item.get_product().research == research:
    #                     cart.remove(item.product)

    def remove_from_cart(self, request, **kwargs):
        research = Research.objects.get(slug=self.request.GET.get('remove_from_cart'))
        cart = Cart(self.request)
        cart.remove(research)

    def get_context_data(self, **kwargs):
        data = super(CartPurchaseView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        #     cart = Cart.objects.get(client__user=self.request.user)
        #     research = cart.items.all()
        # else:
        #     cart = Cart(self.request)
        #     research = [a.product for a in cart]
        cart = Cart(self.request)
        research = cart.cart.cartitem_set.all()

        FormSet = forms.formset_factory(CartResearchForm, max_num=len(research), min_num=len(research))
        formset = FormSet(initial=[{
            'research': x.research,
            'duration': x.duration,
            'update_frequency': x.update_frequency
        } for x in research])

        try:
            data['cart'] = kwargs['form']
            data['formset'] = zip(kwargs['form'], research)
        except:
            data['cart'] = formset
            data['formset'] = zip(formset, research)
        finally:
            return data

    def post(self, request, *args, **kwargs):
        cart = Cart(self.request)
        research = cart.cart.cartitem_set.all()
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

        Cart(self.request).clear()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            client = Client.objects.get(user=self.request.user)
            for form in self.form_classes:
                for field in self.form_classes[form].base_fields:
                    initial[form][field] = getattr(client, field)
        return initial

    def get_success_url(self):
        return reverse('orders:cart')

    def forms_valid(self, forms):
        client = Client.objects.get(user=self.request.user) if self.request.user.is_authenticated else None
        order = Order.objects.latest()
        for form in self.form_classes:
            for field in self.form_classes[form].base_fields:
                if self.request.user.is_authenticated:
                    client.__dict__[field] = forms[form].cleaned_data[field]
                else:
                    order.__dict__[field] = forms[form].cleaned_data[field]
        client.save() if self.request.user.is_authenticated else None
        order.save()
        return super(CartPurchaseView, self).forms_valid(forms)
