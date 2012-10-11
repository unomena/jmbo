import datetime

from django.conf import settings
from django.db import models

class PermittedManager(models.Manager):
    def get_query_set(self):
        
        now = datetime.datetime.now()
        
        # Get base queryset and exclude based on state.
        queryset = super(PermittedManager, self).get_query_set().exclude(
            state='unpublished',
            publish_on__gt=now,
            retract_on__lt=now
        )

        # Exclude objects in staging state if not in
        # staging mode (settings.STAGING = False).
        if not getattr(settings, 'STAGING', False):
            queryset = queryset.exclude(state='staging')

        # Filter objects for current site.
        queryset = queryset.filter(sites__id__exact=settings.SITE_ID)
        return queryset