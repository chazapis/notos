from django.contrib import admin

from .models import Participant, Federation, Exhibit, ExhibitParticipation, TravelDetails


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'country', 'telephone', 'mobile', 'language')

@admin.register(Federation)
class FederationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'country_code')

class ExhibitParticipationAdmin(admin.TabularInline):
    model = ExhibitParticipation

@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    list_display = ('title', 'exhibit_class', 'frames')
    inlines = [ExhibitParticipationAdmin]
    fieldsets = ((None, {'fields': ('participant',
                                    'title',
                                    'short_description',
                                    'exhibit_class',
                                    'date_of_birth',
                                    'frames',
                                    'remarks')}),
                 ('PHILATELIC LITERATURE APPENDIX', {'fields': ('author',
                                                                'publisher',
                                                                'year_of_publication',
                                                                'pages',
                                                                'format',
                                                                'frequency',
                                                                'availability',
                                                                'price')}))

@admin.register(TravelDetails)
class TravelDetailsAdmin(admin.ModelAdmin):
    list_display = ('participant', 'arrival', 'arrival_flight_number', 'departure', 'departure_flight_number')
