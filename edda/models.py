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

from django.db import models, transaction
from django.db.models import F
from django.conf import settings

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core import serializers
import logging
from django.utils.timezone import now
from django.utils.html import format_html

import logging, datetime

import qrcode
import base64
import StringIO

from utils import send_to_rabbitmq

import json, urllib2

logger = logging.getLogger('pippo')

class Ruolipartecipante(models.Model):

    code = models.IntegerField(primary_key=True, db_column="id")
    value = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'ruolipartecipante'

    def __unicode__(self):
        return self.value

#--------------------------------------------------------------------------------

class PosixGroup(models.Model):

    name = models.CharField(max_length=32, primary_key=True, db_column="group")
    description = models.CharField(max_length=512, blank=True, db_column="label")

    class Meta:
        verbose_name = "permesso applicazioni"
        verbose_name_plural = "permessi applicazioni"
        db_table = "posix"

    def __unicode__(self):
        rv = self.name
        if self.description:
            rv += u" (=%s)" % self.description
        return rv

ALL_POSIX_GROUPS = PosixGroup.objects.all()

#PER ORA NO: class HumenPosixGroupMap(models.Model):
#
#    posix_group = models.ForeignKey(PosixGroup)
#    humen = models.ForeignKey("Humen")
#
#    class Meta:
#        verbose_name = "corrispondenza persona -> permesso"
#        verbose_name_plural = "corrispondenze persone -> permessi"
#

#--------------------------------------------------------------------------------

class HumenServices(models.Model):

    name = models.CharField(primary_key=True, max_length=127)

    class Meta:
        db_table = 'humen_services'
        ordering = ('name',)
        verbose_name = 'servizio'
        verbose_name_plural = 'servizi'

    def __unicode__(self):
        return self.name

    @property
    def n_humen(self):
        return self.humen_set.count() 

#--------------------------------------------------------------------------------

class Humen(models.Model):

    SESSO_CHOICES = (
        ('M', 'Maschio'),
        ('F', 'Femmina'),
    )
    cu = models.CharField(max_length=255, blank=True,
        verbose_name='codice unico', help_text='', null=True, unique=True
    )
    codice_censimento = models.IntegerField(blank=True, null=True,
        verbose_name='codice censimento', help_text=''
    )
    idgruppo = models.CharField(max_length=255, blank=True,
        verbose_name='ID gruppo', help_text='', null=True
    )
    idunitagruppo = models.CharField(max_length=255, blank=True,
        verbose_name=u'ID unità gruppo', help_text='', null=True
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
        verbose_name='sesso', help_text='', null=True,
        choices=SESSO_CHOICES
    )
    data_nascita = models.DateField(null=True,
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
    note = models.TextField(blank=True,
        verbose_name='note', help_text='', null=True)

    # Partecipazione -------------------------------

    ruolo = models.ForeignKey(Ruolipartecipante,
        verbose_name='ruolo', help_text='', db_column="ruolo"
    )
    periodo_partecipazione = models.ForeignKey('Periodipartecipaziones', db_column='periodo_partecipazione_id',
        verbose_name='periodo di partecipazione', help_text='', null=True
    )
    pagato = models.NullBooleanField(default=False,
        verbose_name='pagato', help_text=''
    )
    #mod_pagamento_id = models.IntegerField(blank=True, null=True,
    #    verbose_name='modalità di pagamento', help_text=''
    #)

    # Ruoli  ----------------------------
    lab = models.NullBooleanField(default=False,
        verbose_name='lab.', help_text=''
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
        verbose_name='Extra', help_text=''
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

    colazione = models.CharField(max_length=14, db_column='colazione',
        verbose_name='tipo di colazione', help_text='', blank=True,
        choices = (('LATTE', 'LATTE'), ('THE','THE'), ('ALTRO','ALTRO'))
    )
    dieta_alimentare = models.CharField(max_length=14, db_column='dieta_alimentare',
        verbose_name='dieta alimentare', help_text='', blank=True,
        choices = (('STANDARD','STANDARD'),('VEGETARIANO','VEGETARIANO'),('VEGANO','VEGANO'))
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

    arrivato_al_quartiere = models.NullBooleanField(default=None)
    dt_verifica_di_arrivo = models.DateTimeField(blank=True, null=True, default=None)

    #posix_group_set = models.ManyToManyField(PosixGroup,
    #    null=True, blank=True, related_name="humen_set",
    #    #through=HumenPosixGroupMap
    #)


    # Servizi -----------------------------------------

    service = models.ForeignKey(HumenServices, blank=True, null=True, 
        verbose_name='servizio'
    )


    class Meta:
        #managed = False
        db_table = 'humen'
        verbose_name = 'persona'
        verbose_name_plural = 'persone'

    def __unicode__(self):
        return u"%s - %s %s" % (self.cu, self.nome, self.cognome)

    def save(self, *args, **kw):

        # Set boolean fields
        self.intolleranze_alimentari = bool(self.el_intolleranze_alimentari)
        self.allergie_alimentari = bool(self.el_allergie_alimentari)
        self.allergie_farmaci = bool(self.el_allergie_farmaci)

        self.eta = self.compute_age()
        self.nuovo_cu = False

        if self.pk: #we are updating an instance

            old_me = Humen.objects.get(pk=self.pk)
            # check to update idgruppo and idunitagruppo
            if self.vclan != old_me.vclan:
                if self.vclan:
                    self.idunitagruppo = self.vclan.idunitagruppo
                    self.idgruppo = self.vclan.idgruppo
                else:
                    self.idunitagruppo = ''
                    self.idgruppo = ''

                #WARNING: non cambiamo il codice univoco...

            created = False
        else:
            created = True

            # Check for codice_censimento. Se non esiste -> crealo automaticamente!
            if not self.codice_censimento:
                self.assign_codice_censimento()
            self.cu = ''
            if self.vclan:
                self.idunitagruppo = self.vclan.idunitagruppo
                self.idgruppo = self.vclan.idgruppo
            else:
                self.idunitagruppo = ''
                self.idgruppo = ''

        super(Humen, self).save(*args, **kw)

        if created:
            # compute codice unico (cu)
            self.cu = self.compute_cu()
            kw.pop('force_insert', None)
            self.nuovo_cu = True
            super(Humen, self).save(*args, **kw)

    def assign_codice_censimento(self):
        """
        Assegna il primo codice censimento valido < 3000
        """

        if self.codice_censimento:
            raise ValueError(
                u"Questo umano ha già un codice censimento assegnato (=%s)" % self.codice_censimento
        )

        taken_codes = Humen.objects.filter(
            codice_censimento__lte=settings.MAX_USABLE_CODICE_CENSIMENTO
        ).values_list('codice_censimento').order_by('codice_censimento')
        last_taken_code = 0
        for taken_code in taken_codes:
            taken_code = taken_code[0] # taken_code is a tuple
            if taken_code != None: # avoid NULLs
                if taken_code == last_taken_code + 1:
                    last_taken_code = taken_code
                else:
                    self.codice_censimento = last_taken_code + 1

    def compute_cu(self):

        if self.rs:
            base_cu = 'AG'
        elif self.capo:
            base_cu = 'AA'
        elif self.oneteam:
            base_cu = 'OT'
        elif self.extra:
            base_cu = 'OT'
        elif self.lab:
            base_cu = 'AL'
        else:
            raise ValueError("Codice univoco non computabile")

        return "%s-%04d-%06d" % (base_cu, self.vclan_id, self.pk )

    def compute_age(self):
        if self.data_nascita:
            return datetime.date.today().year - self.data_nascita.year
        else:
            return None

    def is_young(self):

        return self.compute_age() < settings.YOUNG_AGE

    def update_arrivo_al_quartiere(self, is_arrived):
        if is_arrived and self.vclan and not self.vclan.arrivato_al_campo:
            raise ValueError("Una persona non può essere arrivata se non è arrivato il suo clan")
        self.arrivato_al_quartiere = is_arrived
        self.dt_verifica_di_arrivo = now()

    @property
    def handicaps(self):
        rv = []
        for k in 'fisiche', 'lis', 'psichiche', 'sensoriali':
            if getattr(self, k):
                rv.append(k.upper()[:3])

        return rv

    @property
    def sostituito_da(self):
        if self.sostituito_da_set.count():
            return self.sostituito_da_set.first().humen_sostituito_da
        else:
            return None

    def arrivato_al_campo_display(self):
        if self.vclan.arrivato_al_campo == True:
            css, button, color = 'success', 'S', '#51a351'
        elif self.vclan.arrivato_al_campo == False:
            css, button, color = 'danger', 'N', 'red'
        else:
            css, button, color = 'warning', '?', '#f89406'
        return format_html('<span class="label label-%s" style="background-color: %s; font-size: 18px; padding: 5px;">%s</span>' % (css, color, button))
    arrivato_al_campo_display.short_description = 'VARCO0'
    arrivato_al_campo_display.allow_tags = True

    def arrivato_al_quartiere_display(self):
        if self.arrivato_al_quartiere == True:
            css, button, color = 'success', 'S', '#51a351'
        elif self.arrivato_al_quartiere == False:
            css, button, color = 'danger', 'N', 'red'
        else:
            css, button, color = 'warning', '?', '#f89406'
        return format_html('<span class="label label-%s" style="background-color: %s; font-size: 18px; padding: 5px;">%s</span>' % (css, color, button))
    arrivato_al_quartiere_display.short_description = 'VARCO1'
    arrivato_al_quartiere_display.allow_tags = True

    def get_new_badge(self):
      badge_qs = self.badge_set.all()
      if badge_qs.count():
          badge_qs.update(is_valid=False)
          nums = []
          for badge in badge_qs:
              nums.append(badge.code[15])
          max_num = max(nums)
          if max_num == '9':
              new_num = 'A'
          elif max_num == 'Z':
              raise Exception('NumeroMassimoBadge', 'Questa persona ha stampato troppi badge, contatta lo staff IT')
          else:
              new_num = chr(ord(max_num) + 1)
      else:
          new_num = '0'
      return HumenBadge.objects.create(humen=self, code=self.cu+'-'+new_num, is_valid=True)

    def update_posix_groups(self, add=[], remove=[]):
        """
        Update or (add or remove) posix groups
        """

        final_add = []
        final_remove = []

        pgroup_names = [] # map(lambda x: x[0], self.posix_group_set.values('name'))

        for gadd in add:
            # update or add groups
            if gadd not in pgroup_names:
                final_add.append(gadd)

        for gdel in remove:
            # update or remove groups
            if gdel in pgroup_names:
                final_remove.append(gdel)

        #self.posix_group_set.remove(*final_remove)
        #self.posix_group_set.add(*final_add)

        routing_key = "humen.groups"
        data = json.dumps({
            "username" : self.cu,
            "add" : add, #original groups sent -> RABBIT is more up-to-date than me
            "remove" : remove, #original groups sent -> RABBIT is more up-to-date than me
        })

        # SEND TO RABBITMQ
        if settings.RABBITMQ_ENABLE:

            send_to_rabbitmq(routing_key, data)

        logger.info("[UPDATE %s] %s" % (routing_key, data))

    def get_posix_groups(self):
        """
        Query the REST API for groups belonging to this humen
        and save it in cache
        """

        headers = { "Content-Type" : "application/json" }
        url = settings.REST_URL_GET_CU_GROUPS % {'cu' : self.cu }
        req = urllib2.Request(url, headers=headers)

        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError as error:
            contents = error.read()

            rv = [u"Errore HTTP nel recupero dei gruppi per %s (%s)" % (self.cu, contents)]
        else:
            contents = response.read()
            d = json.loads(contents)
            rv = d["groups"]

        return rv


#---------------------------------------------------------------------------------

class Vclans(models.Model):

    idvclan = models.CharField(max_length=255, blank=True)
    idgruppo = models.CharField(verbose_name="ID gruppo", max_length=255, blank=True)
    idunitagruppo = models.CharField(verbose_name="ID unità gruppo", max_length=255, blank=True)
    # ordinale = models.CharField(max_length=255, blank=True)
    nome = models.CharField(max_length=255, blank=True)
    regione = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    arrivato_al_campo = models.NullBooleanField(default=None)
    dt_verifica_di_arrivo = models.DateTimeField(blank=True, null=True, default=None)

    arrivato_al_quartiere = models.NullBooleanField(default=None)
    dt_arrivo_quartiere = models.DateTimeField(blank=True, null=True, default=None)

    route_num = models.IntegerField(db_column='route', null=True)
    #is_ospitante = models.NullBooleanField(default=None)

    #quartiere = models.IntegerField(blank=True, null=True)
    quartiere = models.ForeignKey('Districts', to_field="id", db_column='quartiere',
        related_name='in_quartiere', verbose_name='quartiere'
    )
    contrada = models.IntegerField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'vclans'
        verbose_name = 'clan'
        verbose_name_plural = 'clan'

    def __unicode__(self):
        return u"%s (%s)" % (self.nome, self.idunitagruppo)

    def update_arrivo_al_campo(self, is_arrived):
        self.arrivato_al_campo = is_arrived
        self.dt_verifica_di_arrivo = now()

    def update_arrivo_al_quartiere(self, is_arrived):
        """
        Setta lo stato `is_arrived` (True o False) per tutti
        i membri del clan che non sono già stati segnalati come
        ritirati.
        """

        for h in self.humen_set.exclude(arrivato_al_quartiere=False):
            h.update_arrivo_al_quartiere(is_arrived)
            h.save()

    def arrivato_al_campo_display(self):
        if self.arrivato_al_campo == True:
            css, button, color = 'success', 'S', '#51a351'
        elif self.arrivato_al_campo == False:
            css, button, color = 'danger', 'N', 'red'
        else:
            css, button, color = 'warning', '?', '#f89406'
        return format_html('<span class="label label-%s" style="background-color: %s; font-size: 18px; padding: 5px;">%s</span>' % (css, color, button))
    arrivato_al_campo_display.short_description = 'VARCO0'
    arrivato_al_campo_display.allow_tags = True

    def arrivato_al_quartiere_display(self):
        if self.arrivato_al_quartiere == True:
            css, button, color = 'success', 'S', '#51a351'
        elif self.arrivato_al_quartiere == False:
            css, button, color = 'danger', 'N', 'red'
        else:
            css, button, color = 'warning', '?', '#f89406'
        return format_html('<span class="label label-%s" style="background-color: %s; font-size: 18px; padding: 5px;">%s</span>' % (css, color, button))
    arrivato_al_quartiere_display.short_description = 'VARCO1'
    arrivato_al_quartiere_display.allow_tags = True

class HumenSostituzioni(models.Model):

    humen = models.ForeignKey(Humen, to_field="cu",
        primary_key=True, db_column="cu", related_name="sostituito_da_set",
        verbose_name="persona"
    )
    humen_sostituito_da = models.ForeignKey(Humen, to_field="cu",
        db_column="cu_sostituito_da", related_name="sostituisce_da_set",
        verbose_name="sostituito da",
        null=True

    )
    updated_at = models.DateTimeField(
        verbose_name='ultimo aggiornamento', help_text='', auto_now=True
    )

    class Meta:
        managed = False
        db_table = 'humen_sostituzioni'
        verbose_name = 'sostituzione'
        verbose_name_plural = 'sostituzioni'

    def __unicode__(self):
        return u"%s sostituito da %s" % (self.humen, self.humen_sostituito_da)

    @property
    def vclan(self):
        return self.humen.vclan

    @transaction.atomic
    def save(self, *args, **kw):
        super(HumenSostituzioni, self).save(*args, **kw)
        if self.humen.arrivato_al_quartiere is not False: # in [None, True]
            self.humen.arrivato_al_quartiere = False
            self.humen.save()

class HumenBadge(models.Model):

    humen = models.ForeignKey(Humen, to_field="cu",
        db_column="cu", related_name="badge_set",
        verbose_name="persona"
    )

    code = models.CharField(max_length=16, unique=True)

    is_valid = models.BooleanField(default=True, verbose_name='valido')

    updated_at = models.DateTimeField(
        verbose_name='ultimo aggiornamento', help_text='', auto_now=True
    )

    class Meta:
        managed = True
        db_table = 'humen_badge'
        verbose_name = 'badge'
        verbose_name_plural = 'badge'

    def __unicode__(self):
        return u"%s - %s" % (self.humen, self.code[15:])

    @property
    def qrcode(self):
        qr_code = qrcode.make(self.code)
        qr_code_output = StringIO.StringIO()
        qr_code.save(qr_code_output)
        image = qr_code_output.getvalue()
        data = base64.b64encode(image)
        data = "data:image/png;base64," + data
        return data

    @property
    def humen_nome(self):
        return self.humen.nome

    @property
    def humen_cognome(self):
        return self.humen.cognome

    @property
    def humen_vclan(self):
        return self.humen.vclan.nome

#--------------------------------------------------------------------------------

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

class Districts(models.Model):
    name = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=255, blank=True)
    #created_at = models.DateTimeField(blank=True, null=True)
    #updated_at = models.DateTimeField(blank=True, null=True)
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

class Routes(models.Model):
    name = models.CharField(max_length=255, blank=True)
    numero = models.IntegerField(blank=True, null=True)
    area = models.CharField(max_length=255, blank=True)
    #created_at = models.DateTimeField(blank=True, null=True)
    #updated_at = models.DateTimeField(blank=True, null=True)
    quartiere = models.IntegerField(blank=True, null=True)
    quartiere_lock = models.IntegerField(blank=True, null=True)
    contrada = models.IntegerField(blank=True, null=True)

    class Meta:
        #managed = False
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

#--------------------------------------------------------------------------------
# Extending a bit the User model
from django.contrib.auth.models import User

def user_is_readonly(self):
    return bool(self.groups.filter(name='readonly').count())

User.add_to_class('is_readonly', user_is_readonly)

#---------------------------------------------------------------------------------
# RABBITMQ part

if settings.RABBITMQ_ENABLE:

    MODEL_RABBITMQ_MAP = {
        Humen : ('humen', lambda x: x.cu not in ['', None])
    }

    def get_rabbitmq_routing_key(sender, instance, created):

        basename, condition = MODEL_RABBITMQ_MAP.get(sender, (None, None))
        if basename and condition(instance):
            action = ['update','insert'][int(created) or getattr(instance,'nuovo_cu',None)]
            return u"%s.%s" % (basename, action)
        else:
            return None

    import pika
    @receiver(post_save)
    def my_log_queue(sender, instance, created, **kwargs):

        data = serializers.serialize("json", [instance], indent=2)

        # Publish changes to RabbitMQ server
        routing_key = get_rabbitmq_routing_key(sender, instance, created)

        if routing_key:

            send_to_rabbitmq(routing_key, data)

            logger.debug("[DB WRITE %s] %s" % (routing_key, data))
        else:
            logger.debug("[NO RABBIT DB WRITE] %s" % data)
