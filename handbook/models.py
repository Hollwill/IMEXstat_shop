from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


'''
class HandbookNode(MP_Node):
    node_order_by = ['group', 'name']

    group = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return '%s - %s' % (self.group, self.name)

'''

class Handbook(MPTTModel):
	name = models.CharField(max_length=200)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	class MPTTMeta:
		order_insertion_by = ['name']

