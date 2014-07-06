from django.contrib import admin
from edda.models import Humen

class HumenAdmin(admin.ModelAdmin):
    list_display = [
        'cu',
        'nome',
        'cognome',
        'rs',
        'capo',
    ]

admin.site.register(Humen, HumenAdmin)
