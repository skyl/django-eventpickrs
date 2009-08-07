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
)
