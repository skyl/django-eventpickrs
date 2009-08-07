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

    * jQuery

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


