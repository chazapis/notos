from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout

from .models import Participant, Exhibit, ExhibitParticipation, TravelDetails
from .forms import ParticipantForm, ExhibitForm, TravelDetailsForm


def register(request, step='personal'):
    if not request.user.is_authenticated:
        return render(request, 'registrations/login.html')

    try:
        participant = Participant.objects.get(user=request.user)
    except Participant.DoesNotExist:
        participant = None

    if not participant and step != 'personal':
        return redirect('register', step='personal')

    if request.method == 'POST':
        if step == 'personal':
            if participant:
                form = ParticipantForm(request.POST, instance=participant)
            else:
                form = ParticipantForm(request.POST)
            if form.is_valid():
                participant = form.save(commit=False)
                participant.user = request.user
                participant.save()
        elif step == 'exhibit':
            if participant.exhibits.count() == 0:
                form = ExhibitForm(request.POST, instance=participant.exhibits.first())
            else:
                form = ExhibitForm(request.POST)
            if form.is_valid():
                exhibit = form.save(commit=False)
                exhibit.participant = participant
                exhibit.save()
        elif step == 'travel':
            if participant.travel_details.count() == 0:
                form = TravelDetailsForm(request.POST, instance=participant.travel_details.first())
            else:
                form = TravelDetailsForm(request.POST)
            if form.is_valid():
                travel_details = form.save(commit=False)
                travel_details.participant = participant
                travel_details.save()

        next_step = 'personal'
        if participant.exhibits.count() == 0:
            next_step = 'exhibit'
        elif participant.travel_details.count() == 0:
            next_step = 'travel'

        return redirect('register', step=next_step)

    if step == 'personal':
        if participant:
            form = ParticipantForm(instance=participant)
        else:
            form = ParticipantForm()
    elif step == 'exhibit':
        if participant.exhibits.count() == 0:
            form = ExhibitForm(instance=participant.exhibits.first())
        else:
            form = ExhibitForm()
    elif step == 'travel':
        if participant.travel_details.count() == 0:
            form = TravelDetailsForm(instance=participant.travel_details.first())
        else:
            form = TravelDetailsForm()
    else:
        return redirect('register', step='personal')

    action = reverse('register', kwargs={'step': step})
    steps = [{'title': 'Personal',
              'description': 'Name and contact details',
              'done': True if participant else False,
              'current': step == 'personal',
              'url': reverse('register', kwargs={'step': 'personal'})},
             {'title': 'Entries',
              'description': 'Exhibit(s) participating',
              'done': participant and participant.exhibits.count(),
              'current': step == 'exhibit',
              'url': reverse('register', kwargs={'step': 'exhibit'})},
             {'title': 'Travel details',
              'description': 'Arrival and departure',
              'done': participant and participant.travel_details.count(),
              'current': step == 'travel',
              'url': reverse('register', kwargs={'step': 'travel'})}]
    return render(request, 'registrations/register.html', {'action': action, 'form': form, 'steps': steps})

def logout(request, next_page):
    auth_logout(request)
    return redirect(next_page)
