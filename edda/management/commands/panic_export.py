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

        for quartiere_id in range(1, 6):

            clans = Vclans.objects.filter(quartiere__id=quartiere_id, arrivato_al_quartiere=True)

            n_clans = clans.count()
            done = 0

            con = {}
            con['quartiere_id'] = quartiere_id
            con['clans'] = []

            # genera una pagina riassuntiva per ogni clan
            for c in clans:

                npersone = Humen.objects.filter(vclan=c, arrivato_al_quartiere=True).count()

                con['clans'].append({'nome': c.nome, 'idvclan': c.idvclan, 'npersone': npersone})

            write_pdf('panic_overview.html', con, 'panic_export/sottocampo%s_riassunto_clan.pdf' % (quartiere_id))

            # genera una pagina dettagliata per ogni clan
            for c in clans:

                con = {}
                con['quartiere_id'] = quartiere_id
                con['clan'] = {'nome': c.nome, 'idvclan': c.idvclan}
                con['hs'] = []

                hs = Humen.objects.filter(vclan=c, arrivato_al_quartiere=True)

                for h in hs:
                    con['hs'].append(h)

                write_pdf('panic_details.html', con, 'panic_tmp/sottocampo%s_dettagli_clan_%s.pdf' % (quartiere_id, c.idvclan))

            print('Quartiere %s OK!' % (quartiere_id))

        print('>>> Mission Complete!! <<<')


def write_pdf(template_src, context_dict, filename):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = open(filename, 'wb') # Changed from file to filename
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result)
    result.close()

