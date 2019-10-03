from django.shortcuts import render, redirect, reverse
from django.forms import inlineformset_factory
from django.contrib.auth import logout as auth_logout

from .models import Participant, Appointments, Exhibit, ExhibitParticipation, TravelDetails
from .forms import ParticipantForm, AppointmentsForm, ExhibitForm, ExhibitParticipationForm, TravelDetailsForm


def register(request, step=None):
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
            form = ParticipantForm(request.POST, request.FILES, instance=participant)
            if form.is_valid():
                participant = form.save(commit=False)
                participant.user = request.user
                participant.save()
        elif step == 'appointments':
            form = AppointmentsForm(request.POST, instance=participant.appointments.first())
            if form.is_valid():
                appointments = form.save(commit=False)
                appointments.participant = participant
                appointments.save()
        elif step == 'exhibit':
            # form = ExhibitForm(request.POST, instance=participant.exhibits.first())
            form = ExhibitForm(request.POST, request.FILES, instance=participant.exhibits.first(), prefix='main')
            ExhibitParticipationFormSet = inlineformset_factory(Exhibit, ExhibitParticipation, form=ExhibitParticipationForm, extra=1, max_num=6)
            formset = ExhibitParticipationFormSet(request.POST, instance=participant.exhibits.first(), prefix='nested')
            if form.is_valid() and formset.is_valid():
                exhibit = form.save(commit=False)
                exhibit.participant = participant
                exhibit.save()
                formset.save()
        elif step == 'travel':
            form = TravelDetailsForm(request.POST, instance=participant.travel_details.first())
            if form.is_valid():
                travel_details = form.save(commit=False)
                travel_details.participant = participant
                travel_details.save()
        else:
            step = 'personal'

        return redirect('register', step=step)

    if step == 'personal':
        form = ParticipantForm(instance=participant)
        formset = None
    elif step == 'appointments':
        form = AppointmentsForm(instance=participant.appointments.first())
        formset = None
    elif step == 'exhibit':
        form = ExhibitForm(instance=participant.exhibits.first(), prefix='main')
        ExhibitParticipationFormSet = inlineformset_factory(Exhibit, ExhibitParticipation, form=ExhibitParticipationForm, extra=1, max_num=6)
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
             {'title': 'Appointments',
              'description': 'Commissioner/Jury data',
              'done': participant and participant.appointments.count(),
              'current': step == 'appointments',
              'url': reverse('register', kwargs={'step': 'appointments'})},
             {'title': 'Entry forms',
              'description': 'Exhibit(s) participating',
              'done': participant and participant.exhibits.count(),
              'current': step == 'exhibit',
              'url': reverse('register', kwargs={'step': 'exhibit'})},
             {'title': 'Travel details',
              'description': 'Arrival and departure',
              'done': participant and participant.travel_details.count(),
              'current': step == 'travel',
              'url': reverse('register', kwargs={'step': 'travel'})}]
    required_done = True if participant else False
    return render(request, 'registrations/register.html', {'form': form, 'formset': formset, 'steps': steps, 'required_done': required_done})

def logout(request, next_page):
    auth_logout(request)
    return redirect(next_page)
