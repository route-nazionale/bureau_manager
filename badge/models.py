from django.db import models

from base.models import Scout

class Badge(models.Model):
    
    created_on = models.DateField(
        verbose_name=u'data creazione', help_text=u'data di creazione'
    )

    created_on = models.DateField(
        verbose_name=u'data disabilitazione', help_text=u'data di disabilitazione'
    )

    scout = models.ForeignKey(Scout,
        verbose_name=u'scout', help_text=u'scout'
    )

