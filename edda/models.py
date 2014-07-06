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


class Chiefroles(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    kkey = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chiefroles'


class Colaziones(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    kkey = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'colaziones'


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


class Dietabases(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    kkey = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dietabases'


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


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


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


class Humen(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    cu = models.CharField(max_length=255, blank=True)
    codice_censimento = models.IntegerField(blank=True, null=True)
    idgruppo = models.CharField(max_length=255, blank=True)
    idunitagruppo = models.CharField(max_length=255, blank=True)
    vclan_id = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True)
    cognome = models.CharField(max_length=255, blank=True)
    sesso = models.CharField(max_length=255, blank=True)
    data_nascita = models.DateField(blank=True, null=True)
    eta = models.IntegerField(blank=True, null=True)
    periodo_partecipazione_id = models.IntegerField(blank=True, null=True)
    ruolo_id = models.IntegerField(blank=True, null=True)
    novizio = models.IntegerField(blank=True, null=True)
    scout = models.IntegerField(blank=True, null=True)
    agesci = models.IntegerField(blank=True, null=True)
    rs = models.IntegerField(blank=True, null=True)
    capo = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True)
    abitazione = models.CharField(max_length=255, blank=True)
    indirizzo = models.CharField(max_length=255, blank=True)
    provincia = models.CharField(max_length=255, blank=True)
    cap = models.CharField(max_length=255, blank=True)
    citta = models.CharField(max_length=255, blank=True)
    pagato = models.IntegerField(blank=True, null=True)
    mod_pagamento_id = models.IntegerField(blank=True, null=True)
    colazione = models.IntegerField(blank=True, null=True)
    dieta_alimentare_id = models.IntegerField(blank=True, null=True)
    intolleranze_alimentari = models.IntegerField(blank=True, null=True)
    el_intolleranze_alimentari = models.CharField(max_length=255, blank=True)
    allergie_alimentari = models.IntegerField(blank=True, null=True)
    el_allergie_alimentari = models.CharField(max_length=255, blank=True)
    allergie_farmaci = models.IntegerField(blank=True, null=True)
    el_allergie_farmaci = models.CharField(max_length=255, blank=True)
    fisiche = models.IntegerField(blank=True, null=True)
    lis = models.IntegerField(blank=True, null=True)
    psichiche = models.IntegerField(blank=True, null=True)
    sensoriali = models.IntegerField(blank=True, null=True)
    patologie = models.CharField(max_length=255, blank=True)
    stradadicoraggio1 = models.IntegerField(blank=True, null=True)
    stradadicoraggio2 = models.IntegerField(blank=True, null=True)
    stradadicoraggio3 = models.IntegerField(blank=True, null=True)
    stradadicoraggio4 = models.IntegerField(blank=True, null=True)
    stradadicoraggio5 = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    cellulare = models.CharField(max_length=255, blank=True)
    oneteam = models.IntegerField(blank=True, null=True)
    extra = models.IntegerField(blank=True, null=True)
    lab = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'humen'


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


class SchemaMigrations(models.Model):
    version = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'schema_migrations'


class Topics(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    kkey = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'topics'


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
