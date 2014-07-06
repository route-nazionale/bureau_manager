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
    #id = models.IntegerField(primary_key=True)  # AutoField?

    cu = models.CharField(max_length=255, blank=True,
        verbose_name='codice unico', help_text=''
    )
    codice_censimento = models.IntegerField(blank=True, null=True,
        verbose_name='codice censimento', help_text=''
    )
    idgruppo = models.CharField(max_length=255, blank=True,
        verbose_name='id gruppo', help_text=''
    )
    idunitagruppo = models.CharField(max_length=255, blank=True,
        verbose_name=u'id unità gruppo', help_text=''
    )
    
    vclan_id = models.ForeignKey('Vclans', db_column='vclan_id',
        verbose_name='clan', help_text=''
    )
    
    # Anagrafiche --------------------------------------

    nome = models.CharField(max_length=255, blank=True,
        verbose_name='nome', help_text=''
    )
    cognome = models.CharField(max_length=255, blank=True,
        verbose_name='cognome', help_text=''
    )
    sesso = models.CharField(max_length=255, blank=True,
        verbose_name='sesso', help_text=''
    )
    data_nascita = models.DateField(blank=True, null=True,
        verbose_name='data di nascita', help_text=''
    )
    eta = models.IntegerField(blank=True, null=True,
        verbose_name=u'età', help_text=''
    )
    cellulare = models.CharField(max_length=255, blank=True,
        verbose_name='cellulare', help_text=''
    )
    email = models.EmailField(max_length=255, blank=True,
        verbose_name='email', help_text=''
    )
    abitazione = models.CharField(max_length=255, blank=True,
        verbose_name='abitazione', help_text=''
    )
    indirizzo = models.CharField(max_length=255, blank=True,
        verbose_name='indirizzo', help_text=''
    )
    provincia = models.CharField(max_length=255, blank=True,
        verbose_name='provincia', help_text=''
    )
    cap = models.CharField(max_length=255, blank=True,
        verbose_name='CAP', help_text=''
    )
    citta = models.CharField(max_length=255, blank=True,
        verbose_name='citta', help_text=''
    )
   
    # Partecipazione -------------------------------
 
    ruolo_id = models.ForeignKey('Chiefroles', db_column='ruolo_id',
        verbose_name='ruolo', help_text=''
    )
    periodo_partecipazione_id = models.ForeignKey('Periodipartecipaziones', db_column='periodo_partecipazione_id',
        verbose_name='periodo di partecipazione', help_text=''
    )
    pagato = models.BooleanField(default=False,
        verbose_name='pagato', help_text=''
    )
    mod_pagamento_id = models.IntegerField(blank=True, null=True,
        verbose_name='modalità di pagamento', help_text=''
    )
    
    # Ruoli  ----------------------------
    lab = models.BooleanField(default=False,
        verbose_name='tiene un laboratorio', help_text=''
    )
    novizio = models.BooleanField(default=False,
        verbose_name='novizio', help_text=''
    )
    scout = models.BooleanField(default=True,
        verbose_name='scout', help_text=''
    )
    agesci = models.BooleanField(default=True,
        verbose_name='AGESCI', help_text=''
    )
    rs = models.BooleanField(default=True,
        verbose_name='R/S', help_text=''
    )
    capo = models.BooleanField(default=True,
        verbose_name='capo', help_text=''
    )
    oneteam = models.BooleanField(default=False,
        verbose_name='membro OneTeam', help_text=''
    )
    extra = models.BooleanField(default=False,
        verbose_name='esterno', help_text=''
    )

    # Strade di coraggio -----------------------------------    

    stradadicoraggio1 = models.BooleanField(default=False,
        verbose_name='strada di coraggio 1', help_text=''
    )
    stradadicoraggio2 = models.BooleanField(default=False,
        verbose_name='strada di coraggio 2', help_text=''
    )
    stradadicoraggio3 = models.BooleanField(default=False,
        verbose_name='strada di coraggio 3', help_text=''
    )
    stradadicoraggio4 = models.BooleanField(default=False,
        verbose_name='strada di coraggio 4', help_text=''
    )
    stradadicoraggio5 = models.BooleanField(default=False,
        verbose_name='strada di coraggio 5', help_text=''
    )
    
    # Alimentazione --------------------------------------------

    colazione = models.ForeignKey('Colaziones', db_column='colazione',
        verbose_name='tipo di colazione', help_text=''
    )
    dieta_alimentare_id = models.ForeignKey('Dietabases', db_column='dieta_alimentare_id',
        verbose_name='dieta alimentare', help_text=''
    )
    intolleranze_alimentari = models.BooleanField(default=False,
        verbose_name='intolleranze alimentari', help_text=''
    )
    el_intolleranze_alimentari = models.TextField(max_length=255, blank=True,
        verbose_name='intolleranze alimentari', help_text=''
    )
    allergie_alimentari = models.BooleanField(default=False,
        verbose_name='allergie alimentari', help_text=''
    )
    el_allergie_alimentari = models.TextField(max_length=255, blank=True,
        verbose_name='allergie alimentari', help_text=''
    )
    allergie_farmaci = models.BooleanField(default=False,
        verbose_name='allergie farmaci', help_text=''
    )
    el_allergie_farmaci = models.TextField(max_length=255, blank=True,
        verbose_name='allergie farmaci', help_text=''
    )

    # Diversamente abili ---------------------------------------

    fisiche = models.BooleanField(default=False,
        verbose_name=u'disabilità fisica', help_text=''
    )
    lis = models.BooleanField(default=False,
        verbose_name='LIS', help_text=''
    )
    psichiche = models.BooleanField(default=False,
        verbose_name=u'disabilità psichica', help_text=''
    )
    sensoriali = models.BooleanField(default=False,
        verbose_name=u'disabilità sensoriale', help_text=''
    )
    patologie = models.CharField(max_length=255, blank=True,
        verbose_name=u'patologie', help_text=''
    )


    # Date di creazione ed aggiornamento

    created_at = models.DateTimeField(blank=True, null=True,
        verbose_name='data di creazione', help_text=''
    )
    updated_at = models.DateTimeField(blank=True, null=True,
        verbose_name='ultimo aggiornamento', help_text=''
    )

    class Meta:
        managed = False
        db_table = 'humen'
        verbose_name = 'persona'
        verbose_name_plural = 'persone'

    def __unicode__(self):
        return "%s - %s %s" % (self.cu, self.nome, self.cognome)

class Vclans(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
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
    id = models.IntegerField(primary_key=True)  # AutoField?
    kkey = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
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
    id = models.IntegerField(primary_key=True)  # AutoField?
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
    id = models.IntegerField(primary_key=True)  # AutoField?
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
    id = models.IntegerField(primary_key=True)  # AutoField?
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
    id = models.IntegerField(primary_key=True)  # AutoField?
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
    id = models.IntegerField(primary_key=True)  # AutoField?
    route_id = models.IntegerField(blank=True, null=True)
    vclan_id = models.IntegerField(blank=True, null=True)
    ospitante = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gemellaggios'
        verbose_name = 'gemellaggio'
        verbose_name_plural = 'gemellaggi'

class Periodipartecipaziones(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
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
        return self.description

class RoutesOrig(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
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
    id = models.IntegerField(primary_key=True)  # AutoField?
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

class Topics(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
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
