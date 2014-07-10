#-*- coding: utf-8 -*-

from django.contrib import admin
from edda.models import Humen, Chiefroles, Periodipartecipaziones
from edda.models import RSHumen, ChiefHumen, RoutesTest

from django.http import HttpResponseRedirect


import copy

class BaseHumenAdmin(admin.ModelAdmin):
    list_display = [
        '__unicode__',
        'ruolo',
        'vclan',
        'cu',
        'nome',
        'cognome',
        'oneteam',
        'lab',
        'novizio',
        'scout',
        'agesci',
        'extra',
    ]

    search_fields = [
        'cu',
        'nome',
        'cognome',
        'vclan__nome',
        'ruolo__description',
    ]

    list_filter = [
        'ruolo__description',
        'vclan__nome',
    ]

    list_per_page = 100

    fieldsets = (
        (None, {
            'fields': (
                ('vclan', 'codice_censimento'),
                ('cu', 'idgruppo', 'idunitagruppo',),  
            )
        }),
        ('Anagrafica', {
            'fields': (
                ('nome', 'cognome'), ('sesso', 'data_nascita', 'eta'),  
                ('cellulare', 'email'), 
                ('abitazione', 'indirizzo', 'provincia', 'cap', 'citta'),
            )
        }),
        ('Partecipazione', {
            'fields': (
                'ruolo', 'periodo_partecipazione', ('pagato', 'mod_pagamento_id'), 
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
                ('colazione', 'dieta_alimentare'), 
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

    actions = ['add_humen']

    def add_humen(self, request, queryset):
        return HttpResponseRedirect("/admin/edda/humen/add/")
    add_humen.short_description = 'Aggiungi Persona'

class HumenAdmin(BaseHumenAdmin):
    list_display = copy.copy(BaseHumenAdmin.list_display) + ['rs', 'capo']
    list_filter = copy.copy(BaseHumenAdmin.list_filter) + ['rs', 'capo']

class RSAdmin(BaseHumenAdmin):

    list_filter = ( 'agesci', 'vclan')

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
    
class RoutesTestAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'numero', 'area', 'quartiere',
    )

admin.site.register(Humen, BaseHumenAdmin)
admin.site.register(RSHumen, RSAdmin)
admin.site.register(ChiefHumen, ChiefAdmin)
admin.site.register(Chiefroles, ChiefrolesAdmin)
admin.site.register(Periodipartecipaziones, PeriodipartecipazionesAdmin)
admin.site.register(RoutesTest, RoutesTestAdmin)
