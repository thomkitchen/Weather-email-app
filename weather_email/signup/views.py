from django.shortcuts import render
from .models import Subscriber
from .forms import AddSub

def index(request):
	sub = Subscriber.objects.all()
	if request.method == "POST":
		form = AddSub(request.POST)
		if form.is_valid():
			cust = form.save(commit=False)
			cust.save()
	else:
		form = AddSub()
	return render(request, 'signup/index.html', {'subscriber': sub, 'form': form,})