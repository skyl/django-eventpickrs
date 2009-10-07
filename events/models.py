import datetime

from django.db import models
from django.template.defaultfilters import slugify

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class FutureEventsManager(models.Manager):
    ''' Return all of the events, next one first
    '''
    def get_query_set(self):
        return super(FutureEventsManager, self).get_query_set().filter(
                start__gte=datetime.datetime.now()-datetime.timedelta(hours=1)
        ).order_by('start')

class PastEventsManager(models.Manager):
    ''' Return all events in the past, starting with most recent
    '''
    def get_query_set(self):
        return super(PastEventsManager, self).get_query_set().filter(
                start__lte=datetime.datetime.now()-datetime.timedelta(hours=1)
        ).order_by('-start')

class Event(models.Model):
    ''' Simple event-tag with owner and content_object + meta_data '''
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, editable=False)

    start = models.DateTimeField(verbose_name="Date and Time",
            help_text="Checkit")

    owner = models.ForeignKey('auth.User')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    objects = models.Manager()
    futures = FutureEventsManager()
    pasts = PastEventsManager()

    def watchers(self):
        e = EventGroup.objects.get(event=self)
        return e.watchers

    def is_future(self):
        return self.start >= datetime.datetime.now()

    def __unicode__(self):
        return "%s, %s" % (self.slug, self.start.date())

    @models.permalink
    def get_absolute_url(self):
        ''' should be /events/<id>/slug/'''
        return ('events.views.detail', (), {
                'id':str(self.id),
                'slug':self.slug
            }
        )

    def save(self, force_insert=False, force_update=False):
        ''' Automatically generate the slug from the title '''
        self.slug = slugify(self.title)
        super(Event, self).save(force_insert, force_update)

    class Meta:
        ordering=( 'start', )
        unique_together = (('start', 'slug'),)

class EventRelation(models.Model):
    ''' Relate an event to a user.

    '''
    user = models.ForeignKey('auth.User')
    event = models.ForeignKey(Event)

    def __unicode__(self):
        return "%s-%s" % (self.user, self.event)

    class Meta:
        unique_together = (('user', 'event'),)

