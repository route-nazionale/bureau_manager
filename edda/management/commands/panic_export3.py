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

        for c in clans:
            
            con = {}
            con['clan'] = {'nome': c.nome, 'idvclan': c.idvclan}
            con['hs'] = []

            hs = Humen.objects.filter(vclan=c, arrivato_al_quartiere=True)

            for h in hs:
                con['hs'].append(h)

            write_pdf('panic_export3.html', con, 'panic_export_2/clan-%s.pdf' % (c.idvclan))
        
        print 'fatto :)'

def write_pdf(template_src, context_dict, filename):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = open(filename, 'wb') # Changed from file to filename
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result)
    result.close()

