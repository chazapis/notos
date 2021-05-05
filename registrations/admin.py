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

from django.contrib import admin
from django.shortcuts import redirect, reverse
from django.utils.http import urlencode
from admin_views.admin import AdminViews

from .models import Participant, Federation, Appointments, Exhibit, ExhibitParticipation, TravelDetails


@admin.register(Participant)
class ParticipantAdmin(AdminViews):
    list_display = ('full_name', 'country', 'telephone', 'mobile', 'language', 'changed_at')
    admin_views = (('Export to CSV', 'export_to_csv'),
                   ('Export to XLSX', 'export_to_xlsx'),
                   ('Download XLSX report', 'report_to_xlsx'),
                   ('Download exhibits in HTML (per class)', 'exhibits_in_html_per_class'),
                   ('Download exhibits in HTML (per country)', 'exhibits_in_html_per_country'))
    readonly_fields = ('created_at', 'changed_at')

    def export_to_csv(self, *args, **kwargs):
        return redirect('{}?{}'.format(reverse('export_raw'), urlencode({'type': 'csv'})))

    def export_to_xlsx(self, *args, **kwargs):
        return redirect('{}?{}'.format(reverse('export_raw'), urlencode({'type': 'xlsx'})))

    def report_to_xlsx(self, *args, **kwargs):
        return redirect('export_report')

    def exhibits_in_html_per_class(self, *args, **kwargs):
        return redirect('{}?{}'.format(reverse('export_exhibits'), urlencode({'sort': 'class'})))

    def exhibits_in_html_per_country(self, *args, **kwargs):
        return redirect('{}?{}'.format(reverse('export_exhibits'), urlencode({'sort': 'country'})))

@admin.register(Federation)
class FederationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'country_code')

@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ('participant', 'federation', 'commissioner', 'jury', 'changed_at')
    readonly_fields = ('created_at', 'changed_at')

class ExhibitParticipationAdmin(admin.TabularInline):
    model = ExhibitParticipation
    readonly_fields = ('created_at', 'changed_at')

@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    list_display = ('title', 'exhibit_class', 'frames', 'changed_at')
    readonly_fields = ('created_at', 'changed_at')
    inlines = [ExhibitParticipationAdmin]
    fieldsets = ((None, {'fields': ('participant',
                                    'title',
                                    'short_description',
                                    'exhibit_class',
                                    'date_of_birth',
                                    'frames',
                                    'introductory_page',
                                    'synopsis',
                                    'remarks',
                                    'created_at',
                                    'changed_at')}),
                 ('PHILATELIC LITERATURE APPENDIX', {'fields': ('author',
                                                                'publisher',
                                                                'year_of_publication',
                                                                'language',
                                                                'isbn',
                                                                'pages',
                                                                'format',
                                                                'frequency',
                                                                'availability',
                                                                'price')}))

@admin.register(TravelDetails)
class TravelDetailsAdmin(admin.ModelAdmin):
    list_display = ('participant', 'arrival', 'arrival_flight_number', 'departure', 'departure_flight_number', 'changed_at')
    readonly_fields = ('created_at', 'changed_at')
