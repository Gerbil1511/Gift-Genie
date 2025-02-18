from django import forms
from django.core.exceptions import ValidationError
from .models import Planner
import datetime
from django.utils import timezone

class EventForm(forms.ModelForm):
    class Meta:
        model = Planner
        fields = ['title', 'description', 'start', 'end']

    # def clean_start(self):
    #     start = self.cleaned_data.get('start')
    #     if start and start < timezone.now():
    #         raise ValidationError("The event start date/time cannot be in the past.")
    #     return start

    # def clean_end(self):
    #     end = self.cleaned_data.get('end')
    #     start = self.cleaned_data.get('start')
    #     if end and start and end < start:
    #         raise ValidationError("The event end date/time cannot be before the start date/time.")
    #     return end

    # def clean(self):
    #     cleaned_data = super().clean()
    #     start = cleaned_data.get('start')
    #     end = cleaned_data.get('end')
    #     if start and end and end < start:
    #         raise ValidationError("The event end date/time cannot be before the start date/time.")
    #     return cleaned_data