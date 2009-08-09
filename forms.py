from django import forms
from events.models import Event

class EventForm(forms.ModelForm):
    ''' Simple Event with SplitDateTime for jq-ui widgets '''


    start = forms.SplitDateTimeField()

    class Meta:
        model = Event
        exclude = ('object_id', 'content_type', 'owner')

