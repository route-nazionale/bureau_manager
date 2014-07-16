#-*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib import messages
from edda.models import Humen, Periodipartecipaziones
from edda.models import RSHumen, ChiefHumen, Routes, Vclans

from django.http import HttpResponseRedirect
from django import forms
from django.core.urlresolvers import reverse

import copy

#--------------------------------------------------------------------------------
# helper functions and decorators

def disable_field(field):
    field.widget.attrs.update({'disabled' : 'true'})


def only_one_element_allowed(func):

    def my_fun(modeladmin, request, queryset):

        if queryset.count() > 1:
            modeladmin.message_user(request, "Puoi impostare l'arrivo di un solo clan per volta")
            return
        else:
            return func(modeladmin, request, queryset)

    return my_fun

class ReadOnlyForm(forms.ModelForm):

    def __init__(self, *args, **kw):

        super(ReadOnlyForm, self).__init__(*args, **kw)
        for v in self.fields.values():
            disable_field(v)
        
    def clean(self):

        cleaned_data = super(ReadOnlyForm, self).clean()
        if self.instance:
            for k,v in self.fields.items():
                cleaned_data[k] = getattr(self.instance, k)
        return cleaned_data
    
#--------------------------------------------------------------------------------


class BaseHumenForm(forms.ModelForm):

    patologie = forms.CharField(widget=forms.Textarea(attrs={'class':'vLargeTextField'}), required=False, label='Patologie')
    codice_censimento = forms.CharField(widget=forms.TextInput(attrs={'size':20}), required=False, label='Cod. censimento')
    cu = forms.CharField(widget=forms.TextInput(attrs={'size': 14}), required=False, label='Codice univoco')

    CLASSI = (('RS','RS'), ('CA','Capo'), ('OT', 'Oneteam'), ('EX','Quadro'), ('LA','Laboratori'))
    classe_presenza = forms.ChoiceField(widget=forms.Select, choices=CLASSI, label="Tipo")

    scout = forms.BooleanField(required=False, label='Scout')
    agesci = forms.BooleanField(required=False,label="AGESCI")

    stradadicoraggio1 = forms.BooleanField(required=False, label="Il coraggio di amare (1)")
    stradadicoraggio2 = forms.BooleanField(required=False, label="Il coraggio di farsi ultimi (2)")
    stradadicoraggio3 = forms.BooleanField(required=False, label="Il coraggio di essere chiesa (3)")
    stradadicoraggio4 = forms.BooleanField(required=False, label="Il coraggio di essere cittadini (4)")
    stradadicoraggio5 = forms.BooleanField(required=False, label="Il coraggio di liberare il futuro (5)")

    def __init__(self, *args, **kw):

        super(BaseHumenForm, self).__init__(*args, **kw)

        disable_field(self.fields['cu'])
        if kw.get('instance'):
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
        cleaned_data['el_allergie_alimentari'] = cleaned_data['el_allergie_alimentari'].strip()
        cleaned_data['el_intolleranze_alimentari'] = cleaned_data['el_intolleranze_alimentari'].strip()
        cleaned_data['patologie'] = cleaned_data['patologie'].strip()
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
        'scout',
        'agesci',
    ]

    search_fields = [
        'cu',
        'nome',
        'cognome',
        'vclan__nome',
        'ruolo',
    ]

    list_filter = [
        'ruolo',
        'vclan',
    ]

    #DEBUG list_per_page = 10

    fieldsets = (
        (None, {
            'fields': (
                ('vclan', 'codice_censimento'),
                ('scout', 'agesci', 'classe_presenza'),  
                ('cu',),  
            ),
            'classes' : ('wide',)
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

    actions = [
        'arrivati_al_quartiere', 
        'non_arrivati_al_quartiere',
        #'imposta_ritirati',
    ]

    change_list_template = "admin/change_list_pagination_on_top.html"
    actions_on_bottom = True
    actions_on_top = True

    #def add_humen(self, request, queryset):
    #    return HttpResponseRedirect("/admin/edda/humen/add/")
    #add_humen.short_description = 'Aggiungi Persona'

    def change_view(self, request, *args, **kw):
        self.message_user(request, "[NOTA] potremmo modificare (x migliorare) la posizione e la presentazione dei campi", level=messages.WARNING)
        
        return super(BaseHumenAdmin, self).change_view(request, *args, **kw)

    def add_view(self, request, *args, **kw):
        self.message_user(request, "[NOTA] potremmo modificare (x migliorare) la posizione e la presentazione dei campi", level=messages.WARNING)
        
        return super(BaseHumenAdmin, self).add_view(request, *args, **kw)

    def arrivati_al_quartiere(self, request, queryset):
        self.message_user(request, 'Benvenuti: %s' % " ".join(map(unicode, queryset)))
        for el in queryset:
            el.update_arrivo_al_quartiere(is_arrived=True)
            el.save()
    arrivati_al_quartiere.short_description = "CONFERMA L'ARRIVO DI QUESTA PERSONA"

    def non_arrivati_al_quartiere(self, request, queryset):
        for el in queryset:
            el.update_arrivo_al_quartiere(is_arrived=False)
            el.save()
    non_arrivati_al_quartiere.short_description = "REGISTRA CHE QUESTA PERSONA NON VIENE"

    #def imposta_ritirati(self, request, queryset):
    #    for el in queryset:
    #        el.ritirato = True
    #        el.update_arrivo_al_quartiere(is_arrived=False)
    #        el.save()
    #imposta_ritirati.short_description = 'Imposta RITIRO'

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
    
class RoutesAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'numero', 'area', 'quartiere',
    )

class InlineHumenAdminForm(forms.ModelForm):

    handicap = forms.CharField(widget=forms.TextInput(attrs={'size' : '30'}), required=False)

class HumenInline(admin.TabularInline):

    model = Humen
    #template = "admin/vclans/inline_person.html"
    fields = (
        'nowrap__unicode__', 'ruolo', 'handicaps',
        'periodo_partecipazione',
    )
    readonly_fields = ('nowrap__unicode__', 'handicaps', 'ruolo', 'periodo_partecipazione')
    extra = 0

    def handicaps(self, obj):

        rv = []
        if obj.handicaps:
            rv = map(lambda x : '<span class="btn btn-success" style="margin:0.1em">%s</span>' % x, obj.handicaps)

        if not rv:
            rv = "(Nessuna)"
        else:
            rv = "".join(rv)
        return rv
    handicaps.short_description = u"Diversabilità"
    handicaps.allow_tags = True

    def nowrap__unicode__(self, obj):
        return u'<div style="white-space: nowrap;"><a href="%s">%s</a></div>' % (
            reverse('admin:edda_humen_change', args=(obj.pk,)) , unicode(obj).strip()
        )
    nowrap__unicode__.short_description = u"Persona"
    nowrap__unicode__.allow_tags = True

class VclansAdmin(admin.ModelAdmin):

    inlines = [
        HumenInline,
    ]
    form = ReadOnlyForm

    search_fields = [
        'nome',
    ]

    list_filter = [
        'nome',
    ]

    actions = [
        'arrivati_al_campo', 
        'non_arrivati_al_campo',
        'arrivati_al_quartiere',
        'non_arrivati_al_quartiere',
    ]

    change_list_template = "admin/change_list_pagination_on_top.html"
    actions_on_bottom = True
    actions_on_top = True
    save_on_top = True

    list_display = (
        '__unicode__', 'nome', 'idunitagruppo', 'idgruppo'
    )

    fieldsets = (
        (None, {
            'fields': (
                ('nome', 'idunitagruppo', 'idgruppo',
                'regione',)
            )
        }),
    )

    readonly_fields = ('nome', 'idunitagruppo', 'idgruppo', 'regione')

    @only_one_element_allowed
    def arrivati_al_campo(self, request, queryset):
        el = queryset[0]
        el.update_arrivo_al_campo(is_arrived=True)
        el.save()
    arrivati_al_campo.short_description = 'Imposta arrivo al CAMPO'
    

    @only_one_element_allowed
    def non_arrivati_al_campo(self, request, queryset):
        el = queryset[0]
        el.update_arrivo_al_campo(is_arrived=True)
        el.save()
    non_arrivati_al_campo.short_description = 'Imposta il MANCATO ARRIVO al CAMPO'

    @only_one_element_allowed
    def arrivati_al_quartiere(self, request, queryset):
        for el in queryset[0].humen_set.all():
            el.update_arrivo_al_quartiere(is_arrived=True)
            el.save()
    arrivati_al_quartiere.short_description = 'Imposta arrivo al QUARTIERE'

    @only_one_element_allowed
    def non_arrivati_al_quartiere(self, request, queryset):
        for el in queryset[0].humen_set.all():
            el.update_arrivo_al_quartiere(is_arrived=False)
            el.save()
    non_arrivati_al_quartiere.short_description = 'Imposta il MANCATO ARRIVO al QUARTIERE'


admin.site.register(Humen, BaseHumenAdmin)
#admin.site.register(RSHumen, RSAdmin)
#admin.site.register(ChiefHumen, ChiefAdmin)
admin.site.register(Periodipartecipaziones, PeriodipartecipazionesAdmin)
admin.site.register(Routes, RoutesAdmin)

admin.site.register(Vclans, VclansAdmin)
