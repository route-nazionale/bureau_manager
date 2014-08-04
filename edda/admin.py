#-*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib import messages
from edda.models import Humen, Periodipartecipaziones, HumenSostituzioni
from edda.models import HumenBadge, PosixGroup, ALL_POSIX_GROUPS
from edda.models import RSHumen, ChiefHumen, Routes, Vclans
from edda.models import HumenServices
from edda.views_support import make_pdf_response

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
        'arrivato_al_campo_display',
        'arrivato_al_quartiere_display',
        'ruolo',
        'service',
        'vclan',
        'cu',
        'nome',
        'cognome',
        'quartiere',
        'contrada',
        'my_class',
        'scout',
        'agesci',
    ]

    search_fields = [
        'cu',
        'nome',
        'cognome',
        'vclan__nome',
        'ruolo__value',
    ]

    list_filter = [
        'ruolo',
        'vclan',
        'vclan__arrivato_al_campo',
        'arrivato_al_quartiere',
        'vclan__quartiere',
        'vclan__contrada',
        'service',
    ]

    base_readonly_fields = ['codice_censimento', 'cu',
        'periodo_partecipazione', 'quartiere', 'contrada'
    ]

    hyperdynamic_fields = [
        'arrivato_al_campo_display', 'arrivato_al_quartiere_display',
        'sostituito_da',
        'quartiere',
        'contrada',
    ]

    #DEBUG list_per_page = 10

    fieldsets = (
        (None, {
            'fields': [
                ('vclan', 'codice_censimento'),
                ('scout'),
                ('agesci'),
                ('classe_presenza'),
                ('cu',),
                ('service',),
            ],
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
                ('stradadicoraggio1'),
                ('stradadicoraggio2'),
                ('stradadicoraggio3'),
                ('stradadicoraggio4'),
                ('stradadicoraggio5'),
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
        ('Note', {'fields': ('note',)}),
    )
    actions = [
        'arrivati_al_quartiere',
        'non_arrivati_al_quartiere',
        'stampa_badge',
        'stampa_servizi',
    ]

    change_list_template = "admin/change_list_pagination_on_top.html"
    actions_on_bottom = True
    actions_on_top = True

    def quartiere(self, obj):
        return obj.vclan.quartiere

    def contrada(self, obj):
        return obj.vclan.contrada

    # Wrap readonly permissions
    def get_actions(self, request):

        if request.user.is_readonly():
            actions = []
        else:
            actions = super(BaseHumenAdmin, self).get_actions(request)
            del actions['delete_selected']

            # ACTIONS TO MANAGE POSIX GROUPS
            for pgroup in ALL_POSIX_GROUPS:
                for kind in ["add", "remove"]:
                    k = "action_posix_group_%s_%s" % (kind, pgroup.name.replace('.','__'))
                    k_fun = getattr(self, k)
                    actions[k] = (k_fun, k, k_fun.short_description)
        return actions

    def has_add_permission(self, request):
        rv = super(BaseHumenAdmin, self).has_add_permission(request)
        return not request.user.is_readonly() or rv

    def has_delete_permission(self, request, obj=None):
        return False

    # End wrap readonly permissions

    # POSIX GROUP ACTIONS

    def _do_action_posix_group(self, request, queryset, kind, group_name):
        if kind == "add":
            add = [group_name]
            remove = []
        elif kind == "remove":
            add = []
            remove = [group_name]

        for hu in queryset:
            hu.update_posix_groups(add=add, remove=remove)


    def __getattr__(self, attr_name, default=None):
        if attr_name.startswith('action_posix_group_'):
            # recall __getattr__ to get the real method
            # WARNING: do not call this method action_posix_group_xxxxx pay with an infinite recursion otherwise
            fun = self._do_action_posix_group
            kind, group_name = attr_name[len('action_posix_group_'):].split('_',1)
            group_name = group_name.replace('__','.')
            if kind == "add":
                verb_kind = "Aggiungi"
            elif kind == "remove":
                verb_kind = "Rimuovi"

            new_fun = lambda self, request, queryset: fun(request, queryset, kind, group_name)
            new_fun.short_description = "*** autorizzazione: %s %s" % (verb_kind, ALL_POSIX_GROUPS.get(name=group_name))
            new_fun.short_description = new_fun.short_description.upper()
            return new_fun

        else:
            return super(BaseHumenAdmin, self).__getattr__(attr_name, default)

    # END POSIX GROUP ACTIONS

    def get_form(self, request, obj=None):
        """
        Vedi issue https://github.com/route-nazionale/bureau_manager/issues/4

        * Se sei superuser -> puoi cambiare tutti i vclan
        * Altrimenti se ruolo == 8 puoi cambiare vclan tra quelli con lo stesso idgruppo

        """
        self._obj = obj #Hack to filter formfield_for_foreignkey
        if obj:
            if request.user.is_superuser or obj.ruolo.pk == 8:
                # vclan can be modified
                if 'vclan' in self.base_readonly_fields:
                    self.base_readonly_fields.remove('vclan')
            else:
                self.base_readonly_fields.append('vclan')

        form = super(BaseHumenAdmin, self).get_form(request, obj)
        if form.base_fields.get('vclan'):
            form.base_fields['vclan'].widget.can_add_related = False
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # if we are changing a person and we are not a superuser
        if not request.user.is_superuser and self._obj and db_field.name == "vclan":
            kwargs["queryset"] = Vclans.objects.filter(
                idgruppo=self._obj.vclan.idgruppo
            )
        return super(BaseHumenAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #def add_humen(self, request, queryset):
    #    return HttpResponseRedirect("/admin/edda/humen/add/")
    #add_humen.short_description = 'Aggiungi Persona'

    def change_view(self, request, *args, **kw):
        if request.user.is_readonly():
            self.message_user(request, "[NOTA] questo utente non può modificare", level=messages.WARNING)

        for f in self.hyperdynamic_fields:
            if f not in self.base_readonly_fields:
                self.base_readonly_fields.append(f)
                if f not in self.fieldsets[0][1]['fields']:
                    self.fieldsets[0][1]['fields'].append(f)

        if request.user.is_readonly():
            self.readonly_fields = self.base_readonly_fields + [
                'vclan',
                'scout', 'agesci',
                'cu',
                'fisiche', 'lis', 'psichiche', 'sensoriali',
                'patologie',
                'colazione', 'dieta_alimentare',
                'el_intolleranze_alimentari',
                'el_allergie_alimentari',
                'el_allergie_farmaci',
                'stradadicoraggio1', 'stradadicoraggio2',
                'stradadicoraggio3', 'stradadicoraggio4',
                'stradadicoraggio5',
                'ruolo', 'periodo_partecipazione', 'pagato',
                'nome', 'cognome', 'sesso', 'data_nascita',
                'cellulare', 'email',
                'abitazione', 'indirizzo',
                'provincia', 'cap', 'citta'
            ]
        else:
            self.readonly_fields = self.base_readonly_fields
        return super(BaseHumenAdmin, self).change_view(request, *args, **kw)

    def add_view(self, request, *args, **kw):

        if request.user.is_readonly():
            self.message_user(request, "[NOTA] questo utente non può modificare", level=messages.WARNING)

        # Clean an "add form"
        for f in self.hyperdynamic_fields:
            if f in self.base_readonly_fields:
                self.base_readonly_fields.remove(f)
                if f in self.fieldsets[0][1]['fields']:
                    self.fieldsets[0][1]['fields'].remove(f)

        return super(BaseHumenAdmin, self).add_view(request, *args, **kw)

    def sostituito_da(self, obj):
        humen = obj.sostituito_da
        return humen or "Nessuno"

    def arrivati_al_quartiere(self, request, queryset):
        self.message_user(request, 'Benvenuti: %s' % " ".join(map(unicode, queryset)))
        for el in queryset:
            el.update_arrivo_al_quartiere(is_arrived=True)
            el.save()
    arrivati_al_quartiere.short_description = "CONFERMA L'ARRIVO DELLE PERSONE SELEZIONATE"

    def non_arrivati_al_quartiere(self, request, queryset):
        for el in queryset:
            el.update_arrivo_al_quartiere(is_arrived=False)
            el.save()
    non_arrivati_al_quartiere.short_description = "REGISTRA CHE LE PERSONE SELEZIONATE NON VENGONO"

    def stampa_badge(self, request, queryset):

        badge_qs = []
        for hu in queryset:
            badge_qs.append(hu.get_new_badge())
        return make_pdf_response({ 'qs' : badge_qs }, 'badge_qs.html')
    stampa_badge.short_description = 'STAMPA BADGE DELLE PERSONE SELEZIONATE'
    
    def stampa_servizi(self, request, queryset):

        servizi = []
        for hu in queryset:
            servizi.append(hu)
        return make_pdf_response({ 'qs' : servizi }, 'servizi.html')
    stampa_servizi.short_description = 'STAMPA I SERVIZI ASSEGNATI ALLE PERSONE SELEZIONATE'

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
        'nowrap__unicode__', 'arrivato_al_quartiere_display', 'ruolo', 'handicaps',
        'periodo_partecipazione',
    )
    readonly_fields = ('nowrap__unicode__', 'arrivato_al_quartiere_display', 'handicaps', 'ruolo', 'periodo_partecipazione')
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

    def has_delete_permission(self, request, obj=None):
        return False

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
        'arrivato_al_campo',
        'arrivato_al_quartiere',
        'quartiere',
        'contrada',
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
        '__unicode__', 'arrivato_al_campo_display', 'arrivato_al_quartiere_display',  'quartiere', 'contrada', 'idgruppo', 'idunitagruppo'
    )

    fieldsets = (
        (None, {
            'fields': (
                ('nome', 'quartiere', 'contrada', 'route_num', 'idgruppo', 'idunitagruppo',
                'regione', 'arrivato_al_campo_display', 'arrivato_al_quartiere_display')
            )
        }),
    )

    readonly_fields = ('nome', 'idunitagruppo', 'idgruppo', 'regione', 'arrivato_al_campo_display', 'arrivato_al_quartiere_display')

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

    # Wrap readonly permissions
    def get_actions(self, request):

        if request.user.is_readonly():
            actions = []
        else:
            actions = super(VclansAdmin, self).get_actions(request)
        return actions

    def has_add_permission(self, request):
        return not request.user.is_readonly()

    def has_delete_permission(self, request, obj=None):
        return False

    # End wrap readonly permissions

class HumenSostituzioniAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'vclan', 'humen', 'humen_sostituito_da', 'updated_at')
    list_filter = ('humen__vclan',)

    fields = ('humen', 'humen_sostituito_da', 'updated_at')
    readonly_fields = ('humen', 'updated_at')

    actions_on_top = True

    # Wrap readonly permissions
    def get_actions(self, request):

        if request.user.is_readonly():
            actions = []
        else:
            actions = super(HumenSostituzioniAdmin, self).get_actions(request)
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_readonly()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or bool(
            request.user.groups.filter(name__in=['segreteria','tesorieri']).count()
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "humen_sostituito_da":
            kwargs["queryset"] = Humen.objects.filter(vclan=self._obj.humen.vclan).exclude(cu=self._obj.humen.cu)
        return super(HumenSostituzioniAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        self._obj = obj
        form_class = super(HumenSostituzioniAdmin, self).get_form(request, obj, **kwargs)
        return form_class

class HumenBadgeAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'humen', 'code', 'is_valid', 'updated_at')

class HumenServicesAdmin(admin.ModelAdmin):

    list_display = ('name', 'n_humen',)

    inlines = [ HumenInline ] 
    
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Humen, BaseHumenAdmin)
admin.site.register(HumenSostituzioni, HumenSostituzioniAdmin)
admin.site.register(HumenBadge, HumenBadgeAdmin)
admin.site.register(HumenServices, HumenServicesAdmin)
#admin.site.register(RSHumen, RSAdmin)
#admin.site.register(ChiefHumen, ChiefAdmin)
admin.site.register(Periodipartecipaziones, PeriodipartecipazionesAdmin)
admin.site.register(Routes, RoutesAdmin)

admin.site.register(Vclans, VclansAdmin)
