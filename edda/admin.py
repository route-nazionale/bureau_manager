#-*- coding: utf-8 -*-

from django.contrib import admin
from edda.models import Humen, Chiefroles, Periodipartecipaziones
from edda.models import RSHumen, ChiefHumen, RoutesTest

from django.http import HttpResponseRedirect
from django import forms

import copy

def disable_field(field):
    field.widget.attrs.update({'disabled' : 'true'})

class BaseHumenForm(forms.ModelForm):

    patologie = forms.CharField(widget=forms.Textarea(attrs={'class':'vLargeTextField'}), required=False)
    codice_censimento = forms.CharField(widget=forms.TextInput(attrs={'size':20}), required=False)
    cu = forms.CharField(widget=forms.TextInput(attrs={'size': 14}), required=False)

    CLASSI = (('RS','RS'), ('CA','Capo'), ('OT', 'Oneteam'), ('EX','Quadro'), ('LA','Laboratori'))
    classe_presenza = forms.MultipleChoiceField(widget=forms.Select, choices=CLASSI)

    novizio = forms.BooleanField(required=False)
    scout = forms.BooleanField(required=False)
    agesci = forms.BooleanField(required=False,label="AGESCI")

    stradadicoraggio1 = forms.BooleanField(required=False, label="Il coraggio di amare (1)")
    stradadicoraggio2 = forms.BooleanField(required=False, label="Il coraggio di farsi ultimi (2)")
    stradadicoraggio3 = forms.BooleanField(required=False, label="Il coraggio di essere chiesa (3)")
    stradadicoraggio4 = forms.BooleanField(required=False, label="Il coraggio di essere cittadini (4)")
    stradadicoraggio5 = forms.BooleanField(required=False, label="Il coraggio di liberare il futuro (5)")

    def __init__(self, *args, **kw):

        super(BaseHumenForm, self).__init__(*args, **kw)

        disable_field(self.fields['cu'])
        if kw.has_key('instance'):
            disable_field(self.fields['codice_censimento'])
            instance = kw['instance']

            if instance.rs:
                classe = 'RS'
            elif instance.capo:
                classe = 'CA'
            elif instance.lab:
                classe = 'LA'
            elif instance.extra:
                classe = 'EX'
            elif instance.oneteam:
                classe = 'OT'
            else: #default
                classe = 'OT'

            self.fields['classe_presenza'].initial = classe

    def clean(self):

        cleaned_data = super(BaseHumenForm, self).clean()
        cleaned_data['el_allergie_farmaci'] = cleaned_data['el_allergie_farmaci'].strip()
        if self.instance:
            cleaned_data['codice_censimento'] = self.instance.codice_censimento
            cleaned_data['cu'] = self.instance.cu
        return cleaned_data


    #class Meta:
    #    model = Humen
    

class BaseHumenAdmin(admin.ModelAdmin):

    form = BaseHumenForm
    save_on_top = True

    list_display = [
        '__unicode__',
        'ruolo',
        'vclan',
        'cu',
        'nome',
        'cognome',
        'my_class',
        'novizio',
        'scout',
        'agesci',
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
                ('scout', 'agesci', 'classe_presenza', 'novizio'),  
                ('cu',),  
            )
        }),
        ('Anagrafica', {
            'fields': (
                ('nome', 'cognome'), ('sesso', 'data_nascita'),  
                ('cellulare', 'email'), 
                ('abitazione', 'indirizzo', 'provincia', 'cap', 'citta'),
            )
        }),
        ('Partecipazione', {
            'fields': (
                'ruolo', 'periodo_partecipazione', ('pagato'), 
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
                'el_intolleranze_alimentari',
                'el_allergie_alimentari', 
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

    #actions = ['add_humen']
    change_list_template = "admin/change_list_person.html"
    actions_on_bottom = True
    actions_on_top = True

    def add_humen(self, request, queryset):
        return HttpResponseRedirect("/admin/edda/humen/add/")
    add_humen.short_description = 'Aggiungi Persona'

    def my_class(self, obj):

        if obj.rs:
            classe = 'RS'
        elif obj.capo:
            classe = 'Capo'
        elif obj.lab:
            classe = 'Oneteam'
        elif obj.extra:
            classe = 'Quadro'
        elif obj.oneteam:
            classe = 'Laboratori'
        else: #default
            classe = '(Nessuna)'

        return classe
    my_class.short_description = 'classe'

    def save_model(self, request, obj, form, changed):
        
        obj.rs = form.cleaned_data['classe_presenza'] == 'RS'
        obj.capo = form.cleaned_data['classe_presenza'] == 'CA'
        obj.extra = form.cleaned_data['classe_presenza'] == 'EX'
        obj.lab = form.cleaned_data['classe_presenza'] == 'LA'
        obj.oneteam = form.cleaned_data['classe_presenza'] == 'OT'

        obj.save()

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
