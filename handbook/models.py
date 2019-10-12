from treebeard.mp_tree import MP_Node
from django.db import models


class HandbookNode(MP_Node):
    node_order_by = ['group', 'name']

    group = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return '%s - %s' % (self.group, self.name)
