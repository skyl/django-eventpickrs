--------------
django-events
--------------

An app for tagging arbitrary models with "events".
An event is a simple model with a DateTime start and (optional) end.
A small amount of metadata is also contained, title, slug, description.

The idea is to have templatetags for tagging objects with 
datepicker and timepickr jQuery-UI widgets inside a dialog.

Likewise, an overview calendar for model_instances will be obtainable.


Requirements
============

    * Django 1.1+

    * jQuery 1.3+

This app is being built for pinax-0.7+.
Your mileage may vary out of the box in other environments.
For quick integration you will need a current copy django-uni_form, for instance.

Install
=======

    * Check out the code onto your path as events::

        git clone git://github.com/skyl/django-events.git events

    * Add 'events' to INSTALLED_APPS

    * add (r'^events/', include('events.urls')), to your urlpatterns

    * syncdb

For Pinax you can take the additional steps, 
add to the right_tabs block in site_base.html::

    <li id="tab_events"><a href="{% url events_all %}">{% trans "Events" %}</a></li>

In site_tabs.css you can add rules for
``body.events #tab_events a`` and ``body.events #tab_events``. 

Pinax Usage
===========

In the template with the object(s) you want to tag add::

    {% load events_tags %}

Where you would like the link to add an event to a model instance::

    {% event_link_add_to myModelInstance 'css_id' %}

To make this link a jQuery dialog widget, in extra_body::

    <script type="text/javascript" src="{{MEDIA_URL}}events/js/jquery-ui.js"></script>
    <script type="text/javascript" src="{{MEDIA_URL}}events/js/ui.datepicker.js"></script>
    <script type="text/javascript" src="{{MEDIA_URL}}events/js/jquery.utils.js"></script>
    <script type="text/javascript" src="{{MEDIA_URL}}events/js/jquery.strings.js"></script>
    <script type="text/javascript" src="{{MEDIA_URL}}events/js/ui.dropslide.js"></script>
    <script type="text/javascript" src="{{MEDIA_URL}}events/js/ui.timepickr.js"></script>

    <style>
        div.ui-datepicker {z-index:10000000;}
    </style>

    {% add_event_to myModelinstance 'css_id' %}
 
Note that you can choose 'css_id' for these tags but they must match.

Add css for the widget to extra_head::

    {% include 'events/widgetCSS.html' %}
  
To add a link to all of the events for a model instance::
    
    {% link_to_events_for myModelInstance 'css_class' %}


