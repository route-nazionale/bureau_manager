#-*- coding: utf-8 -*-

from django.db import models

import datetime

class District(models.Model):
    """
    District entity
    """

    code = models.CharField(max_length=8, primary_key=True, 
        verbose_name=u'codice quartiere', help_text=u'codice quartiere'
    )
    name = models.CharField(max_length=128, unique=True, 
        verbose_name=u'nome quartiere', help_text=u'nome quartiere'
    )

    class Meta:

        db_table = "camp_districts"
        verbose_name = "quartiere"
        verbose_name_plural = "quartieri"

    def __unicode__(self):
        return self.name

#--------------------------------------------------------------------------------

class ScoutUnit(models.Model):

    name = models.CharField(
        max_length=128, 
        primary_key=True, 
        verbose_name=u'nome', 
        help_text=u'Il nome del gruppo scout'
    )
    
    city = models.CharField(
        max_length=128, 
        verbose_name=u'città', 
        help_text=u'La città del gruppo scout'
    )

    date_arrive = models.DateField(
        default=None, 
        verbose_name="data di arrivo", 
        help_text=u'Data di arrivo'
    )

    district = models.ForeignKey(District, default=None,
        verbose_name=u'quartiere', help_text=u'quartiere'
    )  

    class Meta:

        db_table = "scout_units"
        verbose_name = "gruppo scout"
        verbose_name_plural = "gruppi scout"

    def __unicode__(self):
        return self.name

#--------------------------------------------------------------------------------

class Scout(models.Model):

    code = models.CharField(max_length=128, unique=True,
        verbose_name="codice censimento", help_text=u'codice censimento'
    )
    scout_unit = models.ForeignKey(ScoutUnit)

    name = models.CharField(max_length=32, 
        verbose_name="nome", help_text=u'nome'
    )
    surname = models.CharField(max_length=32, 
        verbose_name="cognome", help_text=u'cognome'
    )
    birthday = models.DateField(verbose_name="data di nascita", help_text=u'data di nascita')
    is_chief = models.BooleanField(default=False, 
        verbose_name=u"è un capo", help_text=u"questo è un capo scout"
    )

    class Meta:

        db_table = "scout_chiefs"
        verbose_name = "capo scout"
        verbose_name_plural = "capi scout"

    def __unicode__(self):
        return u"%s - %s %s" % (self.scout_unit, self.name, self.surname)

    @property
    def age(self):
        return datetime.date.today().year - self.birthday.year

#--------------------------------------------------------------------------------

class HeartBeat(models.Model):

    name = models.CharField(max_length=128, unique=True,
        verbose_name=u'nome', help_text=u'nome strada di coraggio'
    )
    code = models.IntegerField(blank=True,
        verbose_name=u'codice', help_text=u'codice della strada di coraggio'
    )

    def __unicode__(self):
        return self.name
