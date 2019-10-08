from index.models import MenuManagement


def menu(request):
	return {'menu': MenuManagement.objects.all().order_by('priority')}