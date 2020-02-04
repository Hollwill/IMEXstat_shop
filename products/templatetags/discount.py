
from django.template import Library


register = Library()


@register.simple_tag(name='discount_cost', takes_context=True)
def discount_cost(context, value):
    research = context['r']
    return research.get_discount_cost(value)


@register.inclusion_tag('products/cost_template.html', takes_context=True)
def get_cost(context, cost):
    return {
        'r': context['research'],
        'cost': cost
    }