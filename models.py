from django.db import models
from django.template.defaultfilters import slugify

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Event(models.Model):
    ''' Simple event-tag with owner and content_object + meta_data '''
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, editable=False)

    start = models.DateTimeField(verbose_name="Date and Time")

    owner = models.ForeignKey('auth.User')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

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
        ordering=( '-start', )
        unique_together = (('start', 'slug'),)

