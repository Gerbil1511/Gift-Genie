from django import forms
from .models import Planner

class EventForm(forms.ModelForm):
    class Meta:
        model = Planner
        fields = ['event_name', 'description', 'event_date', 'event_time']


    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date < datetime.today().date():
            raise ValidationError("The event date cannot be in the past.")
        return event_date

    def clean_event_time(self):
        event_time = self.cleaned_data.get('event_time')
        if event_time < datetime.now().time() and self.cleaned_data.get('event_date') == datetime.today().date():
            raise ValidationError("The event time cannot be in the past.")
        return event_time

    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get('event_date')
        event_time = cleaned_data.get('event_time')
        if event_date and event_time:
            if event_date == datetime.today().date() and event_time < datetime.now().time():
                raise ValidationError("The event time cannot be in the past.")
        return cleaned_data