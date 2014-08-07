#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from django.template.loader import get_template
from django.template import Context

from edda.models import *

from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
import sys

class Command(BaseCommand):
    args = ''
    help = 'print info PDF for all events, listing people'

    def handle(self, *args, **options):

        clans = Vclans.objects.filter(quartiere__id=1, arrivato_al_quartiere=True)

        n_clans = clans.count()
        done = 0

        con = {}
        con['clans'] = []

        for c in clans:

            npersone = Humen.objects.filter(vclan=c, arrivato_al_quartiere=True).count()

            con['clans'].append({'nome': c.nome, 'idvclan': c.idvclan, 'npersone': npersone})

        write_pdf('panic_export.html', con, 'panic_export/sottocampo1-clan.pdf')
        
def write_pdf(template_src, context_dict, filename):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = open(filename, 'wb') # Changed from file to filename
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result)
    result.close()

