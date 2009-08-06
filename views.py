from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseNotFound

from events.models import Event
from events.forms import EventForm

def all(request):
    qs = Event.objects.all()
    context = {}
    return object_list(request,
            queryset=Event.objects.all(),
            template_name="events/event_list.html",
            extra_context=context,
    )

def detail(request, id, slug):

    return object_detail(request,
        queryset=Event.objects.all(),
        object_id=id,
    )

@login_required
def delete(request, id):
    e = get_object_or_404(Event, pk=id)

    if e.owner == request.user:

        return delete_object(request,
                model=Event,
                object_id = id,
                post_delete_redirect=reverse('events_all'),
        )

    else:
        return HttpResponseRedirect(reverse('acct_login'))

@login_required
def create(request):

    return create_object(request,
        form_class=EventForm,
    )

def add(request, app_label, model_name, id):
    ''' Tag an event to another model object '''

    try:
        ct = ContentType.objects.get(\
                app_label = app_label,
                model = model_name)
        obj = ct.get_object_for_this_type( id=id )

    except:
        return HttpResponseNotFound()

