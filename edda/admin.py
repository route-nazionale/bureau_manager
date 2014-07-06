#-*- coding: utf-8 -*-

from django.contrib import admin
from edda.models import Humen, Chiefroles, Periodipartecipaziones
from edda.models import RSHumen, ChiefHumen

import copy

class BaseHumenAdmin(admin.ModelAdmin):
    list_display = [
        '__unicode__',
        'cu',
        'nome',
        'cognome',
        'vclan_id',
        'ruolo_id',
    ]

    search_fields = [
        'cu',
        'nome',
        'cognome',
        'vclan_id__nome',
        'ruolo_id__description',
    ]

    list_filter = [
        'ruolo_id__description',
        'vclan_id__nome',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('vclan_id', 'codice_censimento'),
                ('cu', 'idgruppo', 'idunitagruppo',),  
            )
        }),
        ('Anagrafica', {
            'fields': (
                ('nome', 'cognome'), ('sesso', 'data_nascita'), #età non visualizzata 
                ('cellulare', 'email'), 
                ('abitazione', 'indirizzo', 'provincia', 'cap', 'citta'),
            )
        }),
        ('Partecipazione', {
            'fields': (
                'ruolo_id', 'periodo_partecipazione_id', ('pagato', 'mod_pagamento_id'), 
            )
        }),
        ('Ruoli', {
            'fields': (
                ('lab', 'novizio', 'scout', 'agesci', 'rs', 'capo', 'oneteam', 'extra'),  
            )
        }),
        ('Strade di coraggio', {
            'fields': (
                ('stradadicoraggio1', 'stradadicoraggio2', 'stradadicoraggio3', 'stradadicoraggio4', 'stradadicoraggio5'),
            )
        }),
        ('Alimentazione', {
            'fields': (
                ('colazione', 'dieta_alimentare_id'), 
                'intolleranze_alimentari', 'el_intolleranze_alimentari',
                'allergie_alimentari', 'el_allergie_alimentari', 
                'allergie_farmaci', 'el_allergie_farmaci',
            )
        }),
        ('Diversamente abili', {
            'fields': (
                ('fisiche', 'lis', 'psichiche', 'sensoriali'),
                'patologie', 
            )
        }),
        ('Aggiornamento', {
            'fields': (
                'created_at', 'updated_at', 
            )
        }),
    )

class HumenAdmin(BaseHumenAdmin):
    list_display = copy.copy(BaseHumenAdmin.list_display) + ['rs', 'capo']
    list_filter = copy.copy(BaseHumenAdmin.list_filter) + ['rs', 'capo']

class RSAdmin(BaseHumenAdmin):
    pass

class ChiefAdmin(BaseHumenAdmin):
    pass

class ChiefrolesAdmin(admin.ModelAdmin):
    
    list_display = (
        'description',
    )

class PeriodipartecipazionesAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
    )
    

admin.site.register(Humen, HumenAdmin)
admin.site.register(RSHumen, RSAdmin)
admin.site.register(ChiefHumen, ChiefAdmin)
admin.site.register(Chiefroles, ChiefrolesAdmin)
admin.site.register(Periodipartecipaziones, PeriodipartecipazionesAdmin)
