from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test, login_required

from edda.models import Vclans, Humen, HumenSostituzioni
from edda.views_support import HttpJSONResponse

def can_update_stato_di_arrivo(user):

    return user.is_superuser or user.groups.filter(name__in=["tesorieri","segreteria"]).count()

@csrf_exempt
@require_POST
@user_passes_test(can_update_stato_di_arrivo)
def vclans_do_check_in_campo(request, pk):

    vc = get_object_or_404(Vclans, pk=pk)
    vc.update_arrivo_al_campo(True)
    vc.save()

    return HttpResponse("OK")

@csrf_exempt
@require_POST
@user_passes_test(can_update_stato_di_arrivo)
def vclans_do_check_in_quartiere(request, pk):

    vc = get_object_or_404(Vclans, pk=pk)
    if not vc.arrivato_al_campo:
        vc.update_arrivo_al_campo(True)
    vc.update_arrivo_al_quartiere(True)
    vc.save()

    return HttpResponse("OK")

@csrf_exempt
@require_POST
@user_passes_test(can_update_stato_di_arrivo)
def vclans_do_set_retired_campo(request, pk):

    vc = get_object_or_404(Vclans, pk=pk)
    vc.update_arrivo_al_campo(False)
    vc.update_arrivo_al_quartiere(False)
    vc.save()

    return HttpResponse("OK")

@csrf_exempt
@require_POST
@user_passes_test(can_update_stato_di_arrivo)
def humen_do_check_in_quartiere(request, pk):

    hu = get_object_or_404(Humen, pk=pk)
    hu.update_arrivo_al_quartiere(True)
    hu.save()

    return HttpResponse("OK")

@csrf_exempt
@require_POST
@user_passes_test(can_update_stato_di_arrivo)
def humen_do_set_retired_quartiere(request, pk):

    hu = get_object_or_404(Humen, pk=pk)
    hu.update_arrivo_al_quartiere(False)
    hu.save()

    return HttpResponse("OK")

@csrf_exempt
#@require_POST
@user_passes_test(can_update_stato_di_arrivo)
def humen_do_prepare_substitution(request, pk):

    hu = get_object_or_404(Humen, pk=pk)
    x, created = HumenSostituzioni.objects.get_or_create(humen=hu)

    return HttpJSONResponse(
        { 'url' : reverse('admin:edda_humensostituzioni_change', args=(x.pk,))}
    )

