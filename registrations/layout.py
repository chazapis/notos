# Based on: https://dev.to/zxenia/django-inline-formsets-with-class-based-views-and-crispy-forms-14o6

from crispy_forms.layout import LayoutObject, TEMPLATE_PACK
from django.template.loader import render_to_string

class Formset(LayoutObject):
    template = 'registrations/formset.html'

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {'formset': formset})
