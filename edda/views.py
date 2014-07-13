from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from edda.models import Vclans

def vclans_do_check_in_campo(request, pk):

    vc = get_object_or_404(Vclans, pk=pk)
    vc.update_arrivo_al_campo(True)
    vc.save()

    return HttpResponse("OK")

def vclans_do_check_in_quartiere(request, pk):

    vc = get_object_or_404(Vclans, pk=pk)
    if not vc.arrivati_al_campo:
        vc.update_arrivo_al_campo(True)
    vc.update_arrivo_al_quartiere(True)
    vc.save()

    return HttpResponse("OK")

    
