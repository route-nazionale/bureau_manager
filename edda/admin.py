#-*- coding: utf-8 -*-

from django.contrib import admin
from edda.models import Humen, Chiefroles, Periodipartecipaziones
from edda.models import RSHumen, ChiefHumen, RoutesTest

from django.http import HttpResponseRedirect
from django import forms

import copy

class BaseHumenForm(forms.ModelForm):

    patologie = forms.CharField(widget=forms.Textarea(attrs={'class':'vLargeTextField'}), required=False)

    def clean(self):

        cleaned_data = super(BaseHumenForm, self).clean()
        cleaned_data['el_allergie_farmaci'] = cleaned_data['el_allergie_farmaci'].strip()
        return cleaned_data


    class Meta:
        model = Humen
    

class BaseHumenAdmin(admin.ModelAdmin):

    form = BaseHumenForm

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
        'vclan',
    ]

    list_per_page = 10

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
                'el_allergie_farmaci',
            )
        }),
        ('Diversamente abili', {
            'fields': (
                ('fisiche', 'lis', 'psichiche', 'sensoriali'),
                'patologie', 
            ),
            #'classes' : ('wide',),
        }),
    )

    actions = ['add_humen']
    change_list_template = "admin/change_list_person.html"

    def add_humen(self, request, queryset):
        return HttpResponseRedirect("/admin/edda/humen/add/")
    add_humen.short_description = 'Aggiungi Persona'

    class Media:
        css = {
            "all": ("my_styles.css",)
        }
        js = ("some_admin_code.js",)

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
#admin.site.register(RSHumen, RSAdmin)
#admin.site.register(ChiefHumen, ChiefAdmin)
admin.site.register(Chiefroles, ChiefrolesAdmin)
admin.site.register(Periodipartecipaziones, PeriodipartecipazionesAdmin)
admin.site.register(RoutesTest, RoutesTestAdmin)
