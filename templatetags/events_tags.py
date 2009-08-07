from django import template

register = template.Library()

from django.contrib.contenttypes.models import ContentType

@register.inclusion_tag('events/tags/add_widget.html')
def add_event_to(model_instance, css_id):
    ''' Tag instance with an event with dialog widget

    {% add_event_to myModel 'css_id %}
    '''

    ContentType.objects.get_for_model(model_instance)
    obj_id = model_instance.id

    app_label = model_instance._meta.app_label
    model_name = model_instance._meta.module_name

    return locals()
