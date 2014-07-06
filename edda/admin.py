from django.contrib import admin
from edda.models import Humen

class HumenAdmin(admin.ModelAdmin):
    list_display = [
        '__unicode__',
        'cu',
        'nome',
        'cognome',
        'vclan_id',
        'ruolo_id',
        'rs',
        'capo',
    ]

    search_fields = [
        'cu',
        'nome',
        'cognome',
        'vclan_id__nome',
        'ruolo_id__description',
    ]

    list_filter = [
        'rs',
        'capo',
        'ruolo_id__description',
        'vclan_id__nome',
    ]

    fieldsets = (
        (None, {
            'fields': (
                'cu', 'codice_censimento', 'idgruppo', 'idunitagruppo', 'vclan_id' 
            )
        }),
        ('Anagrafica', {
            'fields': (
                'nome', 'cognome', 'sesso', 'data_nascita', 'eta', 'cellulare', 
                'email', 'abitazione', 'indirizzo', 'provincia', 'cap', 'citta',
            )
        }),
        ('Partecipazione', {
            'fields': (
                'ruolo_id', 'periodo_partecipazione_id', 'pagato', 'mod_pagamento_id', 
            )
        }),
        ('Ruoli', {
            'fields': (
                'novizio', 'scout', 'agesci', 'rs', 'capo', 'oneteam', 'extra',  
            )
        }),
        ('Strade di coraggio', {
            'fields': (
                'stradadicoraggio1', 'stradadicoraggio2', 'stradadicoraggio3', 'stradadicoraggio4', 'stradadicoraggio5',
            )
        }),
        ('Alimentazione', {
            'fields': (
                'colazione', 'dieta_alimentare_id', 'intolleranze_alimentari', 'el_intolleranze_alimentari',
                'allergie_alimentari', 'el_allergie_alimentari', 'allergie_farmaci', 'el_allergie_farmaci',
            )
        }),
        ('Diversamente abili', {
            'fields': (
                'fisiche', 'lis', 'psichiche', 'sensoriali', 'patologie', 
            )
        }),
        ('Aggiornamento', {
            'fields': (
                'created_at', 'updated_at', 
            )
        }),
    )

admin.site.register(Humen, HumenAdmin)
