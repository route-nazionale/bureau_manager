from django.contrib import admin

from base.models import *

class DistrictAdmin(admin.ModelAdmin):

    list_display = (
        'code',
        'name',
    )

class ScoutUnitAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'city',
        'date_arrive',
        'district',
    )

class ScoutAdmin(admin.ModelAdmin):

    list_display = (
        'code',
        'scout_unit',
        'name',
        'surname',
        'birthday',
        'is_chief',
    )

class HeartBeatAdmin(admin.ModelAdmin):

    list_display = (
        'code',
        'name',
    )

admin.site.register(District,   DistrictAdmin)
admin.site.register(ScoutUnit,  ScoutUnitAdmin)
admin.site.register(Scout,      ScoutAdmin)
admin.site.register(HeartBeat,  HeartBeatAdmin)
