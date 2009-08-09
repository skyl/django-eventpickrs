from django import forms
from events.models import Event

class EventForm(forms.ModelForm):

    start = forms.DateTimeField(('%m/%d/%Y %H:%M',),
            widget=forms.SplitDateTimeWidget(
                date_format='%m/%d/%Y',
                time_format='%H:%M',
            )
    )
    end = forms.DateTimeField(('%m/%d/%Y %H:%M',),
            widget=forms.SplitDateTimeWidget(
                date_format='%m/%d/%Y',
                time_format='%H:%M',
            ),
            required=False
    )

    class Meta:
        model = Event
        exclude = ('object_id', 'content_type', 'owner')

'''
class EventAddForm(EventForm):
    class Meta(EventForm.Meta):
        exclude = ('object_id', 'content_type', 'owner')

class EventFormWithMedia(EventForm):

    class Media:
        css = {'all':('events_form.css',), }
        js = ('events_form.js',)

'''
