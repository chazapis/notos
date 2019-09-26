from django.shortcuts import render, redirect, reverse
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout

from .models import Participant, Exhibit, ExhibitParticipation, TravelDetails
from .forms import ParticipantForm, ExhibitForm, ExhibitParticipationForm, TravelDetailsForm


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
            form = ParticipantForm(request.POST, instance=participant)
            if form.is_valid():
                participant = form.save(commit=False)
                participant.user = request.user
                participant.save()
        elif step == 'exhibit':
            form = ExhibitForm(request.POST, instance=participant.exhibits.first())
            if form.is_valid():
                exhibit = form.save(commit=False)
                exhibit.participant = participant
                exhibit.save()
        elif step == 'travel':
            form = TravelDetailsForm(request.POST, instance=participant.travel_details.first())
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
        form = ParticipantForm(instance=participant)
        formset = None
    elif step == 'exhibit':
        form = ExhibitForm(instance=participant.exhibits.first(), prefix='main')
        ExhibitParticipationFormSet = inlineformset_factory(Exhibit, ExhibitParticipation, form=ExhibitParticipationForm, extra=2, max_num=6)
        formset = ExhibitParticipationFormSet(instance=participant.exhibits.first(), prefix='nested')
    elif step == 'travel':
        form = TravelDetailsForm(instance=participant.travel_details.first())
        formset = None
    else:
        return redirect('register', step='personal')

    form.helper.form_action = reverse('register', kwargs={'step': step})
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
    return render(request, 'registrations/register.html', {'form': form, 'formset': formset, 'steps': steps})

def logout(request, next_page):
    auth_logout(request)
    return redirect(next_page)
