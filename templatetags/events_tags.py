from django import template

register = template.Library()

from django.contrib.contenttypes.models import ContentType
from events.models import Event, EventRelation

@register.inclusion_tag('events/tags/add.html')
def add_event_to(model_instance, css_id):
    ''' Tag instance with an event with dialog widget

    {% add_event_to myModel 'css_id' %}
    This is a javascript bit that requires jQuery.
    On pinax you may put it in extra_body.
    '''

    ContentType.objects.get_for_model(model_instance)
    obj_id = model_instance.id

    app_label = model_instance._meta.app_label
    model_name = model_instance._meta.module_name

    return locals()

@register.inclusion_tag('events/tags/add_link.html')
def event_link_add_to(model_instance, css_id):
    ''' Produce the link for add_event_to javascript

    {% event_link_add_to myModel 'css_id' %}
    '''

    app_label = model_instance._meta.app_label
    model_name = model_instance._meta.module_name

    return locals()

@register.inclusion_tag('events/tags/link_to_events_for.html')
def link_to_events_for(model_instance, css_class):
    ''' Produce the link to the events detail page

    {% link_to_events_for myModel 'css_class' %}
    '''

    app_label = model_instance._meta.app_label
    model_name = model_instance._meta.module_name

    return locals()

@register.inclusion_tag('events/tags/add_url.html')
def events_add_url(model_instance):
    ''' Produce the url to add events to a model

    {% events_add_url myModel %} might return something like:
    /events/add/auth/user/1/
    '''

    app_label = model_instance._meta.app_label
    model_name = model_instance._meta.module_name

    return locals()

@register.inclusion_tag('events/tags/show_event.html', takes_context=True)
def show_event(context, event, user, truncate):
    ''' Show the event summary, suitable for a list display

    {% show_event event_instance user 50 %} to truncate at 50
    {% show_event event_instance user 0 %} to not truncate the description
    Add an extra argument
    '''

    if event.owner == user:
        is_owner = True

    else:
        is_owner = False

    try:
        er = EventRelation.objects.get(
                event=event,
                user=user
        )
    except:
        er = None

    MEDIA_URL = context['MEDIA_URL']
    request = context['request']

    return locals()

@register.inclusion_tag('events/tags/add_event_relation.html', takes_context=True)
def add_remove_event_relation(context, event, user):
    '''render a form to post to url adding the event to one's calendar

    '''

    try:
        EventRelation.objects.get(event=event, user=user)
        exists = True
    except:
        exists = False

    request = context['request']

    return locals()
