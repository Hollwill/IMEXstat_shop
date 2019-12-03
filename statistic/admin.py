from django.contrib import admin
from .models import StatisticData

from django.core.paginator import Paginator
from django.core.cache import cache


# Modified version of a GIST I found in a SO thread
class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)


class StatisticDataAdmin(admin.ModelAdmin):
    model = StatisticData
    list_per_page = 35
    show_full_result_count = False
    paginator = CachingPaginator


admin.site.register(StatisticData, StatisticDataAdmin)
