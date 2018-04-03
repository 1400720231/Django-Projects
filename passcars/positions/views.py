from django.shortcuts import render

# Create your views here.


from . models import CarPosition

def all_positions(request):
	all_positions_informations = CarPosition.objects.filter(is_occupied='0')
	context = {
		'all':all_positions_informations
	}
	return render(request,'all_positions.html',context=context)