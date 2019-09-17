from django.contrib import admin

from .models import Participant, Exhibit, ExhibitParticipation


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'country', 'telephone', 'mobile', 'language')

class ExhibitParticipationAdmin(admin.TabularInline):
    model = ExhibitParticipation

@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    list_display = ('title', 'exhibit_class', 'frames')
    inlines = [ExhibitParticipationAdmin]
