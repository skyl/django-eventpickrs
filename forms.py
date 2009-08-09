from django import forms
from events.models import Event

class EventForm(forms.ModelForm):

    start = end = forms.DateTimeField(('%m/%d/%Y %H:%M',),
            widget=forms.SplitDateTimeWidget(
                date_format='%m/%d/%Y',
                time_format='%H:%M',
            )
    )

    owner = forms.CharField( widget=forms.HiddenInput )

    class Meta:
        model = Event

class EventFormWithMedia(EventForm):

    class Media:
        css = {'all':('events_form.css',), }
        js = ('events_form.js',)


