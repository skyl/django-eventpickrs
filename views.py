from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object,\
        update_object
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.db.models import Q
from django.template import RequestContext

from events.models import Event
from events.forms import EventForm, SearchForm


from django.contrib.auth.models import User

def all(request):
    ''' Shows all of the events in the system

    working on search, filtering, etc
    '''
    if request.method == 'POST':
        action = request.POST.get('action', None)
        if action == 'search':
            search_form = SearchForm(request.POST)
            terms = request.POST.get('terms', None)
            q=Q()

        for t in terms.split(" "):
            q = q|Q(title__icontains=t)|Q(description__icontains=t)

        qs = Event.objects.filter(q)

    else:
        qs = Event.objects.all()
        search_form = SearchForm()

    context = { 'search_form':search_form, }
    return object_list(request,
            queryset=qs,
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

@login_required
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
        #request.POST.update( { 'owner':request.user.id, 'object_id':id,
        #        'content_type':ct.id, 'content_obj': obj, } )
        form = EventForm(request.POST)

        if form.is_valid():
            ev = form.save(commit=False)
            ev.owner = request.user
            ev.object_id = obj.id
            ev.content_type = ct
            ev.save()

            try:
                return HttpResponseRedirect(obj.get_absolute_url())

            except:
                return HttpResponseRedirect(reverse('events_all'))

    else:
        form = EventForm()

    context = { 'form':form, 'object':obj, 'content_type':ct, }
    context.update(locals())

    return render_to_response('events/events_add.html', context,\
            context_instance = RequestContext(request))

@login_required
def change(request, id):
    return update_object(request,
        form_class=EventForm,
        object_id = id,
        extra_context = locals()
    )

def for_day(request, year, month, day):
    events = Event.objects.filter(start__year=year, start__month=month,
            start__day=day)

    return object_list(request,
            queryset = events,
            template_name = "events/events_for_day.html",
            extra_context = locals(),
    )

def for_user(request, username):
    ''' Returns response with all the events owned by or associated with a user

    '''

    user = get_object_or_404(User, username=username)

    events = Event.objects.filter(
            (Q(object_id=user.id)
                &
                Q(content_type=ContentType.objects.get_for_model(user))
            )|
            Q(owner=user)
    )

    return object_list(request,
            queryset = events
    )

def for_instance(request, app_label, model_name, id):
    ''' Returns the events associated with the model instance

    '''

    try:
        ct = ContentType.objects.get(\
                app_label = app_label,
                model = model_name)
        obj = ct.get_object_for_this_type( id=id )

    except:
        return HttpResponseNotFound()

    events = Event.objects.filter(content_type = ct, object_id = id)

    return object_list(request,
            queryset = events
    )

