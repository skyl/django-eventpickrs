from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

urlpatterns = patterns('',
    url(r'^$', view='events.views.all',
        name="events_all"),

    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', view='events.views.detail',
        name="events_detail"),

    url(r'^create/$', view='events.views.create',
        name="events_create"),

    url(r'^delete/(?P<id>\d+)/', view='events.views.delete',
        name='events_delete'),

    url(r'add/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<id>\d+)/$',\
            view='events.views.add', name='events_add'),

    url(r'change/(?P<id>\d+)/', view='events.views.change',
        name='events_change'),

    url(r'for_day/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',\
            view='events.views.for_day', name='events_for_day'),

    url(r'foo/(?P<username>[-\w]+)/$',\
            view='events.views.for_user', name='events_for_user'),

    url(r'for/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<id>\d+)/$',\
            view='events.views.for_instance', name='events_for_instance'),
)
