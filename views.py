from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.template import RequestContext

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

    if request.method == 'POST':
        request.POST.update( { 'owner':request.user.id, 'object_id':id,
                'content_type':ct.id, 'content_obj': obj, } )
        form = EventForm(request.POST)

        if form.is_valid():
            form.save()

        try:
            return HttpResponseRedirect(obj.get_absolute_url())

        except:
            return HttpResponseRedirect(reverse('events_all'))

    else:
        form = EventForm()

    context = { 'form':form, 'object':obj, 'content_type':ct, }
    context.update(locals())

    return render_to_response('events/event_form.html', context,\
            context_instance = RequestContext(request))

