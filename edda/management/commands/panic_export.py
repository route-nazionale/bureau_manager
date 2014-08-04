#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from django.template.loader import get_template
from django.template import Context

from edda.models import *

from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
import sys
import datetime
import csv

class Command(BaseCommand):
    args = ''
    help = 'print info PDF for all events, listing people'

    def handle(self, *args, **options):

        hs = Humen.objects.filter(arrivato_al_quartiere=True)
        n_hs = hs.count()
        done = 0

        con = {}
        con['hs'] = []

        for h in hs:

            done = done + 1

            sys.stdout.write("\r%s/%s %s %s%%" % (done, n_hs, h.cu, int(100 * float(done)/float(n_hs))))
            sys.stdout.flush()

            con['hs'].append(h)
        
        a = datetime.datetime.now()

        con['data'] = a
        con['n_hs'] = n_hs
        

        filename = '/tmp/panic_export_humen_%s%s%s-%s%s.csv' % (
            a.year,
            a.month,
            a.day,
            a.hour,
            a.minute,
        )

        print ''
        print 'Esportazione file csv...'
        write_to_text_file(hs, filename)
        print 'esportati %s utenti in %s' % (done, filename) 


def write_to_text_file(humen, filename):
    f = open(filename, 'wb')
    f.write(",".join(
            [
                "Nome", 
                "Cognome", 
                "Data nascita", 
                "Nome Vclan", 
                "ID Vclan",
                "Codice Unico",
                "Quartiere",
                "Contrada",
            ]
        )
    )
    f.write("\n")
    for h in humen:
        f.write(",".join(
                [
                    h.nome.encode('utf-8'), 
                    h.cognome.encode('utf-8'), 
                    str(h.data_nascita).encode('utf-8'), 
                    h.vclan.nome.encode('utf-8'), 
                    h.vclan.idvclan.encode('utf-8'),
                    h.cu.encode('utf-8'),
                    h.vclan.quartiere.name.encode('utf-8'),
                    str(h.vclan.contrada).encode('utf-8')
                ]
            )
        )
        f.write("\n")
    f.close()

def write_pdf(template_src, context_dict, filename):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = open(filename, 'wb') # Changed from file to filename
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result)
    result.close()


          
