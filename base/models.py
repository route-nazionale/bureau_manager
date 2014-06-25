#-*- coding: utf-8 -*-

from django.db import models

import datetime

class ScoutUnit(models.Model):

    name = models.CharField(max_length=128, primary_key=True)

    class Meta:

        db_table = "scout_units"
        verbose_name = "gruppo scout"
        verbose_name_plural = "gruppi scout"

    def __unicode__(self):
        return self.name

#--------------------------------------------------------------------------------

class ScoutChief(models.Model):

    code = models.CharField(max_length=128, unique=True,
        verbose_name="codice censimento"
    )
    scout_unit = models.ForeignKey(Unit)

    name = models.CharField(max_length=32, verbose_name="nome")
    surname = models.CharField(max_length=32, verbose_name="cognome")
    birthday = models.DateField(verbose_name="data di nascita");
    is_spalla = models.BooleanField(default=False, verbose_name=u"è un capo spalla",
        help_text=u"questo capo verrà iscritto dalla 'pattuglia eventi' con criteri supersonici"
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

class District(models.Model):
    """
    District entity
    """

    code = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=128, unique=True)

    class Meta:

        db_table = "camp_districts"
        verbose_name = "quartiere"
        verbose_name_plural = "quartieri"

    def __unicode__(self):
        return self.name

#--------------------------------------------------------------------------------

class HeartBeat(models.Model):

    name = models.CharField(max_length=128, unique=True)
    code = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.name
