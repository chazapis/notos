from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout

from .models import Participant, Exhibit, ExhibitParticipation, TravelDetails
from .forms import ParticipantForm


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'registrations/login.html')

    valid = False
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            valid = True
        #     return HttpResponseRedirect('/thanks/')

    # participant = Participant.objects.get(pk=1)
    # form = ParticipantForm(instance=participant)
    else:
        form = ParticipantForm()

    return render(request, 'registrations/index.html', {'form': form})

def logout(request, next_page):
    auth_logout(request)
    return redirect(next_page)
