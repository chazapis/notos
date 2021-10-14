# Copyright (C) 2019 Antony Chazapis
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import io
import zipfile
import xlsxwriter

from django.shortcuts import render, redirect, reverse, HttpResponse
from django.conf import settings
from django.forms import inlineformset_factory
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import login, logout as auth_logout, BACKEND_SESSION_KEY, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django_countries import countries
from textwrap import shorten
from datetime import datetime
from collections import OrderedDict

from .models import Participant, Federation, Appointments, Exhibit, ExhibitParticipation, TravelDetails
from .forms import ParticipantForm, AppointmentsForm, ExhibitForm, ExhibitParticipationForm, TravelDetailsForm, SignUpForm, ChangePasswordForm, ForgotPasswordForm, ResetPasswordForm
from .tokens import account_activation_token


@login_required
def register(request, step=None, exhibit_id=None):
    if step == 'exhibit' and request.method == 'POST' and settings.ENTRY_FORMS_DISABLED_MESSAGE:
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
                    recipients = ([] if settings.EMAIL_ONLY_ADDITIONAL_RECIPIENTS else appointments.federation.email_list()) + settings.EMAIL_ADDITIONAL_RECIPIENTS
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
                    send_mail('%s - %s' % (settings.EXHIBITION_NAME, title), '%s (in HTML format)' % title, settings.EMAIL_HOST_USER, recipients, html_message=content)

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

                email_to = None
                commissioner_appointments = Appointments.objects.filter(commissioner=True, federation__country_code=participant.country.code).first()
                if commissioner_appointments:
                    email_to = [commissioner_appointments.participant.email]
                else:
                    federation = Federation.objects.filter(country_code=participant.country.code).first()
                    if federation:
                        if federation.commissioner_email:
                            email_to = [federation.commissioner_email]
                        else:
                            email_to = federation.email_list()
                if not email_to and settings.NO_COMMISSIONER_EMAIL:
                    email_to = [settings.NO_COMMISSIONER_EMAIL]

                if email_to:
                    title = 'Exhibit Registration'
                    recipients = ([] if settings.EMAIL_ONLY_ADDITIONAL_RECIPIENTS else email_to) + settings.EMAIL_ADDITIONAL_RECIPIENTS
                    message = 'Dear Commissioner,<br />This is the entry form data we received from the prospective exhibitor of your country.<br />(a) In case there are errors, please get in contact with the exhibitor and advise him/her to correct the errors and re-submit.<br />(b) If, however, you disapprove of the application, please '
                    if settings.GENERAL_COMMISSIONER_EMAIL:
                        message += 'email the General Commissioner at <a class="text-dark" href="mailto:%s">%s</a>.' % (settings.GENERAL_COMMISSIONER_EMAIL, settings.GENERAL_COMMISSIONER_EMAIL)
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
                    send_mail('%s - %s' % (settings.EXHIBITION_NAME, title), '%s (in HTML format)' % title, settings.EMAIL_HOST_USER, recipients, html_message=content)

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
            initial_surname = participant.surname if (participant and participant.surname) else request.user.last_name
            initial_name = participant.name if (participant and participant.name) else request.user.first_name
            initial_email = participant.email if (participant and participant.email) else request.user.email
            form = ParticipantForm(instance=participant, initial={'surname': initial_surname,
                                                                  'name': initial_name,
                                                                  'email': initial_email})
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
    if local_account and step == 'personal' and request.user.email:
        form.fields['email'].widget.attrs['readonly'] = True
    required_done = True if participant else False
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
              'description': 'Participating exhibits',
              'done': participant and participant.exhibits.count(),
              'current': step == 'exhibit',
              'url': reverse('register', kwargs={'step': 'exhibit'})},
             {'title': 'Travel details',
              'description': 'Flights, accommodation, etc.',
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
                                                           'can_change_password': can_change_password,
                                                           'privacy_policy_message': settings.PRIVACY_POLICY_MESSAGE})

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

@staff_member_required
def export_raw(request):
    export_type = request.GET.get('type', 'csv')
    export_name = '%s-export-%s' % (settings.EXHIBITION_NAME.replace(' ', '-'), datetime.now().strftime('%Y%m%d%H%M%S'))

    if export_type == 'csv':
        zip_stream = io.BytesIO()
        with zipfile.ZipFile(zip_stream, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr('%s/registrants.csv' % export_name, Participant.export_to_csv())
            zip_file.writestr('%s/exhibits.csv' % export_name, Exhibit.export_to_csv())
            zip_file.writestr('%s/exhibit_participations.csv' % export_name, ExhibitParticipation.export_to_csv())
            zip_file.writestr('%s/federations.csv' % export_name, Federation.export_to_csv())
            zip_file.writestr('%s/countries.csv' % export_name, Participant.export_countries_to_csv())
            zip_file.writestr('%s/titles.csv' % export_name, Participant.export_choices_to_csv(Participant.TITLE_CHOICES))
            zip_file.writestr('%s/languages.csv' % export_name, Participant.export_choices_to_csv(Participant.LANGUAGE_CHOICES))
            zip_file.writestr('%s/accredited_jurors.csv' % export_name, Appointments.export_choices_to_csv(Appointments.ACCREDITED_JUROR_CHOICES))
            zip_file.writestr('%s/exhibit_classes.csv' % export_name, Exhibit.export_choices_to_csv(Exhibit.EXHIBIT_CLASS_CHOICES))
            zip_file.writestr('%s/exhibition_levels.csv' % export_name, ExhibitParticipation.export_choices_to_csv(ExhibitParticipation.EXHIBITION_LEVEL_CHOICES))
            zip_file.writestr('%s/medals.csv' % export_name, ExhibitParticipation.export_choices_to_csv(ExhibitParticipation.MEDAL_CHOICES))

        response = HttpResponse(zip_stream.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="%s.zip"' % export_name
        return response
    else:
        xlsx_stream = io.BytesIO()
        xlsx_options = {'strings_to_numbers': False,
                        'strings_to_formulas': False,
                        'strings_to_urls': False}
        with xlsxwriter.Workbook(xlsx_stream, xlsx_options) as workbook:
            Participant.export_to_xlsx(workbook, 'registrants')
            Exhibit.export_to_xlsx(workbook, 'exhibits')
            ExhibitParticipation.export_to_xlsx(workbook, 'exhibit_participations')
            Federation.export_to_xlsx(workbook, 'federations')
            Participant.export_countries_to_xlsx(workbook, 'countries')
            Participant.export_choices_to_xlsx(workbook, 'titles', Participant.TITLE_CHOICES)
            Participant.export_choices_to_xlsx(workbook, 'languages', Participant.LANGUAGE_CHOICES)
            Appointments.export_choices_to_xlsx(workbook, 'accredited_jurors', Appointments.ACCREDITED_JUROR_CHOICES)
            Exhibit.export_choices_to_xlsx(workbook, 'exhibit_classes', Exhibit.EXHIBIT_CLASS_CHOICES)
            ExhibitParticipation.export_choices_to_xlsx(workbook, 'exhibition_levels', ExhibitParticipation.EXHIBITION_LEVEL_CHOICES)
            ExhibitParticipation.export_choices_to_xlsx(workbook, 'medals', ExhibitParticipation.MEDAL_CHOICES)

        response = HttpResponse(xlsx_stream.getvalue(), content_type='application/xlsx')
        response['Content-Disposition'] = 'attachment; filename="%s.xlsx"' % export_name
        return response

@staff_member_required
def export_report(request):
    report_name = '%s-report-%s' % (settings.EXHIBITION_NAME.replace(' ', '-'), datetime.now().strftime('%Y%m%d%H%M%S'))

    def write_entries(worksheet, entries):
        next_column = 0
        for section in entries[0].keys():
            row = 0
            column = next_column
            next_column = 0
            titles_written = False
            for entry in [e[section] for e in entries]:
                row += 1
                if not entry:
                    continue
                if not titles_written:
                    worksheet.write_row(0, column, entry.keys())
                    next_column = column + len(entry)
                    titles_written = True
                worksheet.write_row(row, column, ['\n'.join(str(v).splitlines()) for v in entry.values()])

    xlsx_stream = io.BytesIO()
    xlsx_options = {'strings_to_numbers': False,
                    'strings_to_formulas': False,
                    'strings_to_urls': False}
    with xlsxwriter.Workbook(xlsx_stream, xlsx_options) as workbook:
        worksheet = workbook.add_worksheet('Registrants')
        entries = []
        for participant in Participant.objects.all():
            entries.append({'id': {'ID': participant.id},
                            'participant': participant.printout(all_fields=True),
                            'appointments': participant.appointments.first().printout(all_fields=True) if participant.appointments.count() else None,
                            'travel_details': participant.travel_details.first().printout(all_fields=True) if participant.travel_details.count() else None})
        write_entries(worksheet, entries)

        worksheet = workbook.add_worksheet('Exhibits')
        entries = []
        for exhibit in Exhibit.objects.all():
            entries.append({'id': {'ID': exhibit.id},
                            'exhibit': exhibit.printout(all_fields=True),
                            'participant': exhibit.participant.printout(all_fields=True)})
        write_entries(worksheet, entries)

    response = HttpResponse(xlsx_stream.getvalue(), content_type='application/xlsx')
    response['Content-Disposition'] = 'attachment; filename="%s.xlsx"' % report_name
    return response

@staff_member_required
def export_exhibits(request):
    export_sort = request.GET.get('sort', 'class')
    extras = request.GET.get('extras', '')
    extras = int(extras) if extras.isdigit() else 0

    if export_sort == 'class':
        exhibit_sections = OrderedDict({'non-competitive': {'title': 'Non-Competitive Classes',
                                                            'classes': []},
                                        'competitive': {'title': 'Competitive Classes',
                                                        'classes': []}})
        for exhibit_class, exhibit_class_title in Exhibit.EXHIBIT_CLASS_CHOICES:
            section = 'non-competitive' if exhibit_class_title.startswith('A') else 'competitive'
            exhibits = Exhibit.objects.filter(exhibit_class=exhibit_class, rejected=False).order_by('participant__surname')
            if len(exhibits) == 0:
                continue
            if extras:
                jury_groups = set([exhibit.jury_group for exhibit in exhibits])
                if len(jury_groups) > 1:
                    for jury_group in sorted([(j if j else 0) for j in jury_groups]):
                        if jury_group:
                            jury_group_title_suffix = ' (jury group %d)' % jury_group
                        else:
                            jury_group_title_suffix = ' (empty jury group)'
                        exhibit_sections[section]['classes'].append({'title': exhibit_class_title + jury_group_title_suffix,
                                                                     'exhibits': exhibits.filter(jury_group=jury_group if jury_group else None)})
                    continue
            exhibit_sections[section]['classes'].append({'title': exhibit_class_title,
                                                         'exhibits': exhibits})
    else:
        exhibit_countries = set()
        for exhibit in Exhibit.objects.all():
            exhibit_countries.add(exhibit.participant.country.name)
        exhibit_countries = sorted(list(exhibit_countries))

        exhibit_sections = OrderedDict()
        for country in exhibit_countries:
            exhibit_classes = []
            for exhibit_class, exhibit_class_title in Exhibit.EXHIBIT_CLASS_CHOICES:
                exhibits = Exhibit.objects.filter(exhibit_class=exhibit_class, participant__country=countries.by_name(country), rejected=False).order_by('participant__surname')
                if len(exhibits) == 0:
                    continue
                exhibit_classes.append({'title': exhibit_class_title,
                                        'exhibits': exhibits})
            exhibit_sections[country] = {'title': country,
                                         'classes': exhibit_classes}

    return render(request, 'registrations/exhibits.html', {'exhibit_sections': exhibit_sections,
                                                           'extras': extras})

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
                                                          'next': settings.LOGIN_REDIRECT_URL,
                                                          'show_privacy_policy': True,
                                                          'privacy_policy_message': settings.PRIVACY_POLICY_MESSAGE})

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
