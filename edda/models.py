#-*- coding: utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Humen(models.Model):

    cu = models.CharField(max_length=255, blank=True,
        verbose_name='codice unico', help_text='', null=True
    )
    codice_censimento = models.IntegerField(blank=True, null=True,
        verbose_name='codice censimento', help_text=''
    )
    idgruppo = models.CharField(max_length=255, blank=True,
        verbose_name='id gruppo', help_text='', null=True
    )
    idunitagruppo = models.CharField(max_length=255, blank=True,
        verbose_name=u'id unità gruppo', help_text='', null=True
    )
    
    vclan = models.ForeignKey('Vclans', db_column='vclan_id',
        verbose_name='clan', help_text='', null=True
    )
    
    # Anagrafiche --------------------------------------

    nome = models.CharField(max_length=255, blank=True,
        verbose_name='nome', help_text='', null=True
    )
    cognome = models.CharField(max_length=255, blank=True,
        verbose_name='cognome', help_text='', null=True
    )
    sesso = models.CharField(max_length=255, blank=True,
        verbose_name='sesso', help_text='', null=True
    )
    data_nascita = models.DateField(blank=True, null=True,
        verbose_name='data di nascita', help_text=''
    )
    eta = models.IntegerField(blank=True, null=True,
        verbose_name=u'età', help_text=''
    )
    cellulare = models.CharField(max_length=255, blank=True,
        verbose_name='cellulare', help_text='', null=True
    )
    email = models.EmailField(max_length=255, blank=True,
        verbose_name='email', help_text='', null=True
    )
    abitazione = models.CharField(max_length=255, blank=True,
        verbose_name='abitazione', help_text='', null=True
    )
    indirizzo = models.CharField(max_length=255, blank=True,
        verbose_name='indirizzo', help_text='', null=True
    )
    provincia = models.CharField(max_length=255, blank=True,
        verbose_name='provincia', help_text='', null=True
    )
    cap = models.CharField(max_length=255, blank=True,
        verbose_name='CAP', help_text='', null=True
    )
    citta = models.CharField(max_length=255, blank=True,
        verbose_name='citta', help_text='', null=True
    )
   
    # Partecipazione -------------------------------
 
    ruolo = models.ForeignKey('Chiefroles', db_column='ruolo_id',
        verbose_name='ruolo', help_text='', null=True, blank=True
    )
    periodo_partecipazione = models.ForeignKey('Periodipartecipaziones', db_column='periodo_partecipazione_id',
        verbose_name='periodo di partecipazione', help_text='', null=True
    )
    pagato = models.NullBooleanField(default=False,
        verbose_name='pagato', help_text=''
    )
    mod_pagamento_id = models.IntegerField(blank=True, null=True,
        verbose_name='modalità di pagamento', help_text=''
    )
    
    # Ruoli  ----------------------------
    lab = models.NullBooleanField(default=False,
        verbose_name='lab.', help_text=''
    )
    novizio = models.NullBooleanField(default=False,
        verbose_name='novizio', help_text=''
    )
    scout = models.NullBooleanField(default=True,
        verbose_name='scout', help_text=''
    )
    agesci = models.NullBooleanField(default=True,
        verbose_name='AGESCI', help_text=''
    )
    rs = models.NullBooleanField(default=True,
        verbose_name='R/S', help_text=''
    )
    capo = models.NullBooleanField(default=True,
        verbose_name='capo', help_text=''
    )
    oneteam = models.NullBooleanField(default=False,
        verbose_name='OneTeam', help_text=''
    )
    extra = models.NullBooleanField(default=False,
        verbose_name='esterno', help_text=''
    )

    # Strade di coraggio -----------------------------------    

    stradadicoraggio1 = models.NullBooleanField(default=False,
        verbose_name='strada di coraggio 1', help_text=''
    )
    stradadicoraggio2 = models.NullBooleanField(default=False,
        verbose_name='strada di coraggio 2', help_text=''
    )
    stradadicoraggio3 = models.NullBooleanField(default=False,
        verbose_name='strada di coraggio 3', help_text=''
    )
    stradadicoraggio4 = models.NullBooleanField(default=False,
        verbose_name='strada di coraggio 4', help_text=''
    )
    stradadicoraggio5 = models.NullBooleanField(default=False,
        verbose_name='strada di coraggio 5', help_text=''
    )
    
    # Alimentazione --------------------------------------------

    colazione = models.ForeignKey('Colaziones', db_column='colazione',
        verbose_name='tipo di colazione', help_text='', null=True
    )
    dieta_alimentare = models.ForeignKey('Dietabases', db_column='dieta_alimentare_id',
        verbose_name='dieta alimentare', help_text='', null=True
    )
    intolleranze_alimentari = models.NullBooleanField(default=False,
        verbose_name='intolleranze alimentari', help_text=''
    )
    el_intolleranze_alimentari = models.TextField(max_length=255, blank=True,
        verbose_name='intolleranze alimentari', help_text='', null=True
    )
    allergie_alimentari = models.NullBooleanField(default=False,
        verbose_name='allergie alimentari', help_text=''
    )
    el_allergie_alimentari = models.TextField(max_length=255, blank=True,
        verbose_name='allergie alimentari', help_text='', null=True
    )
    allergie_farmaci = models.NullBooleanField(default=False,
        verbose_name='allergie farmaci', help_text=''
    )
    el_allergie_farmaci = models.TextField(max_length=255, blank=True,
        verbose_name='allergie farmaci', help_text='', null=True
    )

    # Diversamente abili ---------------------------------------

    fisiche = models.NullBooleanField(default=False,
        verbose_name=u'disabilità fisica', help_text=''
    )
    lis = models.NullBooleanField(default=False,
        verbose_name='LIS', help_text=''
    )
    psichiche = models.NullBooleanField(default=False,
        verbose_name=u'disabilità psichica', help_text=''
    )
    sensoriali = models.NullBooleanField(default=False,
        verbose_name=u'disabilità sensoriale', help_text=''
    )
    patologie = models.CharField(max_length=255, blank=True,
        verbose_name=u'patologie', help_text='', null=True
    )


    # Date di creazione ed aggiornamento

    created_at = models.DateTimeField(blank=True, null=True,
        verbose_name='data di creazione', help_text='', auto_now_add=True
    )
    updated_at = models.DateTimeField(blank=True, null=True,
        verbose_name='ultimo aggiornamento', help_text='', auto_now=True
    )

    class Meta:
        managed = False
        db_table = 'humen'
        verbose_name = 'persona'
        verbose_name_plural = 'persone'

    def __unicode__(self):
        return "%s - %s %s" % (self.cu, self.nome, self.cognome)

    def save(self, *args, **kw):

        self.intolleranze_alimentari = bool(self.el_intolleranze_alimentari)
        self.allergie_alimentari = bool(self.el_allergie_alimentari)
        self.allergie_farmaci = bool(self.el_allergie_farmaci)
        super(Humen, self).save(*args, **kw)

class Vclans(models.Model):
    idvclan = models.CharField(max_length=255, blank=True)
    idgruppo = models.CharField(max_length=255, blank=True)
    idunitagruppo = models.CharField(max_length=255, blank=True)
    ordinale = models.CharField(max_length=255, blank=True)
    nome = models.CharField(max_length=255, blank=True)
    regione = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vclans'
        verbose_name = 'clan'
        verbose_name_plural = 'clan'

    def __unicode__(self):
        return self.nome

class Chiefroles(models.Model):
    kkey = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, verbose_name='ruolo')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chiefroles'
        verbose_name = 'ruolo'
        verbose_name_plural = 'ruoli'

    def __unicode__(self):
        return self.description

class Colaziones(models.Model):
    kkey = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colaziones'
        verbose_name = 'tipo di colazione'
        verbose_name_plural = 'tipi di colazione'

    def __unicode__(self):
        return self.name

class Contradas(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    district_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    routes_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    vincolo_tende = models.IntegerField(blank=True, null=True)
    vincolo_persone = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contradas'
        verbose_name = 'contrada'
        verbose_name_plural = 'contrade'

    def __unicode__(self):
        return self.name

class Dietabases(models.Model):
    kkey = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dietabases'
        verbose_name = 'dieta alimentare'
        verbose_name_plural = 'diete alimentari'

    def __unicode__(self):
        return self.name

class Districts(models.Model):
    name = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    vincolo_tende = models.IntegerField(blank=True, null=True)
    vincolo_persone = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'districts'
        verbose_name = 'quartiere'
        verbose_name_plural = 'quartieri'

    def __unicode__(self):
        return self.name

class Gemellaggios(models.Model):
    route = models.ForeignKey('RoutesTest', db_column='route_id')
    vclan = models.ForeignKey('Vclans', db_column='vclan_id')
    ospitante = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gemellaggios'
        verbose_name = 'gemellaggio'
        verbose_name_plural = 'gemellaggi'

class Periodipartecipaziones(models.Model):
    kkey = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    from_day = models.IntegerField(blank=True, null=True)
    to_day = models.IntegerField(blank=True, null=True)
    from_meal = models.IntegerField(blank=True, null=True)
    to_meal = models.IntegerField(blank=True, null=True)
    ruolo = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'periodipartecipaziones'
        verbose_name = 'periodo di partecipazione'
        verbose_name_plural = 'periodi di partecipazione'
    
    def __unicode__(self):
        return u"%s - %s" % (self.ruolo, self.description)

class RoutesOrig(models.Model):
    name = models.CharField(max_length=255, blank=True)
    numero = models.IntegerField(blank=True, null=True)
    area = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    quartiere = models.IntegerField(blank=True, null=True)
    quartiere_lock = models.IntegerField(blank=True, null=True)
    contrada_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'routes_orig'

class RoutesTest(models.Model):
    name = models.CharField(max_length=255, blank=True)
    numero = models.IntegerField(blank=True, null=True)
    area = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    quartiere = models.IntegerField(blank=True, null=True)
    quartiere_lock = models.IntegerField(blank=True, null=True)
    contrada_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'routes_test'
        verbose_name = 'Route'
        verbose_name_plural = 'Route'

    def __unicode__(self):
        return self.name

class Topics(models.Model):
    kkey = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'topics'

# ----------------------------------

class SchemaMigrations(models.Model):
    version = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'schema_migrations'



class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

#--------------------------------------------------------------------------------

class ChiefManager(models.Manager):
    def get_queryset(self):
        return super(ChiefManager, self).get_queryset().filter(capo=True)

class RSManager(models.Manager):
    def get_queryset(self):
        return super(RSManager, self).get_queryset().filter(rs=True)


class ChiefHumen(Humen):

    objects = ChiefManager()

    class Meta:
        proxy = True
        verbose_name = 'capo'
        verbose_name_plural = 'capi'

class RSHumen(Humen):

    objects = RSManager()

    class Meta:
        proxy = True
        verbose_name = 'RS'
        verbose_name_plural = 'RS'
