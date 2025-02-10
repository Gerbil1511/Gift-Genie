from django import forms
from .models import Planner

class EventForm(forms.ModelForm):
    class Meta:
        model = Planner
        fields = ['event_name', 'description', 'event_date', 'event_time']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
        }