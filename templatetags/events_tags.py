from django import template

register = template.Library()

from django.contrib.contenttypes.models import ContentType

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

