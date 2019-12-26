from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.forms import inlineformset_factory
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout as auth_logout, BACKEND_SESSION_KEY, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from textwrap import shorten

from .models import Participant, Appointments, Exhibit, ExhibitParticipation, TravelDetails
from .forms import ParticipantForm, AppointmentsForm, ExhibitForm, ExhibitParticipationForm, TravelDetailsForm, SignUpForm, ChangePasswordForm, ForgotPasswordForm, ResetPasswordForm
from .tokens import account_activation_token


@login_required
def register(request, step=None, exhibit_id=None):
    if step == 'exhibit' and settings.ENTRY_FORMS_HIDDEN:
        return redirect('register', step='personal')

    try:
        participant = Participant.objects.get(user=request.user)
    except Participant.DoesNotExist:
        participant = None

    if step == 'personal':
        form_title = 'Personal'
        remove_url = None
    elif step == 'appointments':
        form_title = 'Appointments'
        remove_url = None
    elif step == 'exhibit':
        if exhibit_id is not None:
            try:
                exhibit = participant.exhibits.get(id=exhibit_id)
            except Exhibit.DoesNotExist:
                return redirect('register', step='exhibit')
        else:
            exhibit = None

        if exhibit is None:
            form_title = 'Add entry'
            remove_url = None
        else:
            form_title = '<a href="' + reverse('register', kwargs={'step': step}) + '" class="text-dark">Entry forms</a> &gt; Edit entry'
            remove_url = reverse('remove_exhibit', kwargs={'exhibit_id': exhibit.id})
    elif step == 'travel':
        form_title = 'Travel details'
        remove_url = None
    else:
        return redirect('register', step='personal')

    if request.method == 'POST':
        if not participant and step != 'personal':
            return redirect('register', step='personal')

        if step == 'personal':
            form = ParticipantForm(request.POST, request.FILES, instance=participant)
            form.helper.form_action = reverse('register', kwargs={'step': step})
            formset = None
            if form.is_valid():
                participant = form.save(commit=False)
                participant.user = request.user
                participant.save()
                return redirect('register', step=step)
        elif step == 'appointments':
            form = AppointmentsForm(request.POST, instance=participant.appointments.first())
            form.helper.form_action = reverse('register', kwargs={'step': step})
            formset = None
            if form.is_valid():
                appointments = form.save(commit=False)
                appointments.participant = participant
                appointments.save()

                if appointments.federation.email:
                    title = 'Commissioner/Juror Registration'
                    message = 'Dear Mr President of the Federation,<br />This is the registration data we received from the appointed Commissioner or proposed Juror from your Federation. Please email us at <a class="text-dark" href="mailto:%s">%s</a> in case you find it inappropriate.' % (settings.EXHIBITION_EMAIL, settings.EXHIBITION_EMAIL)
                    sections = [{'title': 'Personal',
                                 'fields': participant.printout(),
                                 'subsections': []},
                                {'title': 'Appointments',
                                 'fields': appointments.printout(),
                                 'subsections': []}]
                    content = render_to_string('registrations/email.html', {'title': title,
                                                                            'message': message,
                                                                            'sections': sections})
                    send_mail('%s - %s' % (settings.EXHIBITION_NAME, title), '%s (in HTML format)' % title, settings.EMAIL_HOST_USER, ['chazapis@gmail.com', 'info@california.gr'], html_message=content)

                return redirect('register', step=step)
        elif step == 'exhibit':
            form = ExhibitForm(request.POST, request.FILES, instance=exhibit, prefix='main')
            if exhibit is None:
                form.helper.form_action = reverse('register', kwargs={'step': step})
            else:
                form.helper.form_action = reverse('edit_exhibit', kwargs={'exhibit_id': exhibit.id})
            if form.is_valid():
                exhibit = form.save(commit=False)
                exhibit.participant = participant
            ExhibitParticipationFormSet = inlineformset_factory(Exhibit, ExhibitParticipation, form=ExhibitParticipationForm, extra=1, max_num=6)
            formset = ExhibitParticipationFormSet(request.POST, instance=exhibit, prefix='nested')
            if exhibit and formset.is_valid():
                exhibit.save()
                formset.save()

                commissioner_appointments = Appointments.objects.filter(commissioner=True, federation__country_code=participant.country.code).first()
                email_to = commissioner_appointments.participant.email if commissioner_appointments else settings.NO_COMMISSIONER_EMAIL
                if email_to:
                    title = 'Exhibit Registration'
                    message = 'Dear Commissioner,<br />This is the entry form data we received from the prospective exhibitor of your country.<br />(a) In case there are errors, please get in contact with the exhibitor and advise him/her to correct the errors and re-submit.<br />(b) If, however, you disapprove of the application, please '
                    if settings.GENERAL_COMMISSIONER_EMAIL:
                        messasge += 'email the General Commissioner at <a class="text-dark" href="mailto:%s">%s</a>.' % (settings.GENERAL_COMMISSIONER_EMAIL, settings.GENERAL_COMMISSIONER_EMAIL)
                    else:
                        message += 'email us at <a class="text-dark" href="mailto:%s">%s</a>.' % (settings.EXHIBITION_EMAIL, settings.EXHIBITION_EMAIL)
                    sections = [{'title': 'Personal',
                                 'fields': participant.printout(),
                                 'subsections': []},
                                {'title': 'Entry',
                                 'fields': exhibit.printout(),
                                 'subsections': [{'title': 'Previous participation #%d' % (j + 1),
                                                  'fields': participation.printout()} for j, participation in enumerate(exhibit.participations.all())]}]
                    content = render_to_string('registrations/email.html', {'title': title,
                                                                            'message': message,
                                                                            'sections': sections})
                    send_mail('%s - %s' % (settings.EXHIBITION_NAME, title), '%s (in HTML format)' % title, settings.EMAIL_HOST_USER, ['chazapis@gmail.com', 'info@california.gr'], html_message=content)

                return redirect('edit_exhibit', exhibit_id=exhibit.id)
        elif step == 'travel':
            form = TravelDetailsForm(request.POST, instance=participant.travel_details.first())
            form.helper.form_action = reverse('register', kwargs={'step': step})
            formset = None
            if form.is_valid():
                travel_details = form.save(commit=False)
                travel_details.participant = participant
                travel_details.save()
                return redirect('register', step=step)
    else:
        if step == 'personal':
            form = ParticipantForm(instance=participant, initial={'surname': request.user.last_name,
                                                                  'name': request.user.first_name,
                                                                  'email': request.user.email})
            form.helper.form_action = reverse('register', kwargs={'step': step})
            formset = None
        elif step == 'appointments':
            appointments = participant.appointments.first() if participant else None
            form = AppointmentsForm(instance=appointments)
            form.helper.form_action = reverse('register', kwargs={'step': step})
            formset = None
        elif step == 'exhibit':
            form = ExhibitForm(instance=exhibit, prefix='main')
            if exhibit is None:
                form.helper.form_action = reverse('register', kwargs={'step': step})
            else:
                form.helper.form_action = reverse('edit_exhibit', kwargs={'exhibit_id': exhibit.id})
            ExhibitParticipationFormSet = inlineformset_factory(Exhibit, ExhibitParticipation, form=ExhibitParticipationForm, extra=1, max_num=6)
            formset = ExhibitParticipationFormSet(instance=exhibit, prefix='nested')
        elif step == 'travel':
            travel_details = participant.travel_details.first() if participant else None
            form = TravelDetailsForm(instance=travel_details)
            form.helper.form_action = reverse('register', kwargs={'step': step})
            formset = None

    local_account = (request.session[BACKEND_SESSION_KEY] == 'django.contrib.auth.backends.ModelBackend')

    exhibits = []
    if participant and step == 'exhibit' and exhibit_id is None:
        exhibits = [{'title': e.title,
                     'description': shorten(e.short_description, width=80, placeholder='...'),
                     'url': reverse('edit_exhibit', kwargs={'exhibit_id': e.id})} for e in participant.exhibits.all()]
    if local_account and step == 'personal':
        form.fields['email'].disabled = True
    required_done = True if participant else False
    steps = [{'title': 'Personal',
              'description': 'Name and contact details',
              'hidden': False,
              'done': True if participant else False,
              'current': step == 'personal',
              'url': reverse('register', kwargs={'step': 'personal'})},
             {'title': 'Appointments',
              'description': 'Commissioner/Jury data',
              'hidden': False,
              'done': participant and participant.appointments.count(),
              'current': step == 'appointments',
              'url': reverse('register', kwargs={'step': 'appointments'})},
             {'title': 'Entry forms',
              'description': 'Participating exhibits',
              'hidden': settings.ENTRY_FORMS_HIDDEN,
              'done': participant and participant.exhibits.count(),
              'current': step == 'exhibit',
              'url': reverse('register', kwargs={'step': 'exhibit'})},
             {'title': 'Travel details',
              'description': 'Flights, accommodation, etc.',
              'hidden': False,
              'done': participant and participant.travel_details.count(),
              'current': step == 'travel',
              'url': reverse('register', kwargs={'step': 'travel'})}]
    can_change_password = local_account

    return render(request, 'registrations/register.html', {'exhibits': exhibits,
                                                           'form_title': form_title,
                                                           'form': form,
                                                           'formset': formset,
                                                           'remove_url': remove_url,
                                                           'required_done': required_done,
                                                           'steps': steps,
                                                           'can_change_password': can_change_password})

@login_required
def remove_exhibit(request, exhibit_id=None):
    try:
        participant = Participant.objects.get(user=request.user)
        exhibit = participant.exhibits.get(id=exhibit_id)
        exhibit.delete()
    except Exhibit.DoesNotExist:
        pass

    return redirect('register', step='exhibit')

@login_required
def printout(request):
    try:
        participant = Participant.objects.get(user=request.user)
    except Participant.DoesNotExist:
        return redirect('register', step='personal')

    sections = []
    sections.append({'title': 'Personal',
                     'fields': participant.printout(),
                     'subsections': []})
    if participant.appointments.count():
        sections.append({'title': 'Appointments',
                         'fields': participant.appointments.first().printout(),
                         'subsections': []})
    for i, exhibit in enumerate(participant.exhibits.all()):
        sections.append({'title': 'Entry #%d' % (i + 1),
                         'fields': exhibit.printout(),
                         'subsections': [{'title': 'Previous participation #%d' % (j + 1),
                                          'fields': participation.printout()} for j, participation in enumerate(exhibit.participations.all())]})
    if participant.travel_details.count():
        sections.append({'title': 'Travel details',
                         'fields': participant.travel_details.first().printout(),
                         'subsections': []})
    return render(request, 'registrations/print.html', {'sections': sections})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            activation_url = '%s://%s/activate/%s/%s' % ('https' if request.is_secure else 'http',
                                                         request.get_host(),
                                                         urlsafe_base64_encode(force_bytes(user.pk)),
                                                         account_activation_token.make_token(user))
            title = 'Account activation'
            message = 'Dear %s,<br />Please activate your account by visiting the following link:<br /><a href="%s">%s</a>' % (user.username, activation_url, activation_url)
            content = render_to_string('registrations/email.html', {'title': title,
                                                                    'message': message,
                                                                    'sections': None})
            send_mail('%s - %s' % (settings.EXHIBITION_NAME, title), '%s (in HTML format)' % title, settings.EMAIL_HOST_USER, [user.email], html_message=content)

            message = 'Your account has been created, but in order to login you have to confirm your email address.<br />We have sent you an email with instructions on how to complete the sign up process.'
            return render(request, 'registrations/account.html', {'message': message,
                                                                  'next': settings.LOGIN_REDIRECT_URL})
    else:
        form = SignUpForm()
    return render(request, 'registrations/account.html', {'message': 'Sign up by creating an account with us.',
                                                          'form': form,
                                                          'next': settings.LOGIN_REDIRECT_URL})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('register', step='personal')

    return render(request, 'registrations/account.html', {'message': 'Invalid or expired activation link.',
                                                          'next': settings.LOGIN_REDIRECT_URL})

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            for user in User.objects.filter(email=email).all():
                if user.social_auth.exists():
                    continue
                if not user.email:
                    continue

                reset_url = '%s://%s/reset_password/%s/%s' % ('https' if request.is_secure else 'http',
                                                              request.get_host(),
                                                              urlsafe_base64_encode(force_bytes(user.pk)),
                                                              default_token_generator.make_token(user))
                title = 'Password reset'
                message = 'Dear %s,<br />Please reset the password to your account by visiting the following link:<br /><a href="%s">%s</a>' % (user.username, reset_url, reset_url)
                content = render_to_string('registrations/email.html', {'title': title,
                                                                        'message': message,
                                                                        'sections': None})
                send_mail('%s - %s' % (settings.EXHIBITION_NAME, title), '%s (in HTML format)' % title, settings.EMAIL_HOST_USER, [user.email], html_message=content)

            message = 'If the email belongs to a valid local account, we will send you instructions <br />on how to proceed with resetting the password.'
            return render(request, 'registrations/account.html', {'message': message,
                                                                  'next': settings.LOGIN_REDIRECT_URL})
    else:
        form = ForgotPasswordForm()
    return render(request, 'registrations/account.html', {'message': 'Enter your email address below to reset your password.',
                                                          'form': form,
                                                          'next': settings.LOGIN_REDIRECT_URL})

def reset_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Password successfully reset.')
                return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            form = ResetPasswordForm(user)
        return render(request, 'registrations/account.html', {'message': 'Reset your password.',
                                                              'form': form,
                                                              'next': settings.LOGIN_REDIRECT_URL})

    return render(request, 'registrations/account.html', {'message': 'Invalid or expired password reset link.',
                                                          'next': settings.LOGIN_REDIRECT_URL})

@login_required
def change_password(request):
    next = request.GET.get('next', settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully changed.')
            return redirect(next)
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'registrations/account.html', {'message': 'Change your password.',
                                                          'form': form,
                                                          'next': next})

@login_required
def logout(request, next):
    auth_logout(request)
    return redirect(next)
