from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import HandbookNode


class HandbookNodeAdmin(TreeAdmin):
    form = movenodeform_factory(HandbookNode)


admin.site.register(HandbookNode, HandbookNodeAdmin)