from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.admin.views.decorators import staff_member_required


from edda.models import Vclans, Humen, HumenSostituzioni
from edda.views_support import HttpJSONResponse, make_pdf_response

import json

def can_update_stato_di_arrivo(user):
    return user.is_superuser or user.groups.filter(name__in=["tesorieri","segreteria"]).count()

def can_print_badge(user):
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

@csrf_exempt
@require_POST
@user_passes_test(can_update_stato_di_arrivo)
def vclan_do_set_null_arrived_campo(request, pk):

    vclan = get_object_or_404(Vclans, pk=pk)
    vclan.update_arrivo_al_campo(None)
    vclan.save()

    return HttpResponse("OK")

@csrf_exempt
@require_POST
@user_passes_test(can_update_stato_di_arrivo)
def vclan_do_set_null_arrived_quartiere(request, pk):

    vclan = get_object_or_404(Vclans, pk=pk)
    vclan.update_arrivo_al_quartiere(None)
    vclan.save()

    return HttpResponse("OK")

@csrf_exempt
@require_POST
@user_passes_test(can_update_stato_di_arrivo)
def humen_do_set_null_arrived_quartiere(request, pk):

    hu = get_object_or_404(Humen, pk=pk)
    hu.update_arrivo_al_quartiere(None)
    hu.save()

    return HttpResponse("OK")

@csrf_exempt
@user_passes_test(can_print_badge)
def humen_do_print_badge(request, pk):

    hu = get_object_or_404(Humen, pk=pk)

    return make_pdf_response({ 'qs' :[hu.get_new_badge()] }, 'badge_qs.html')


@csrf_exempt
@user_passes_test(can_print_badge)
def vclan_do_print_badge(request, pk):

    vclan = get_object_or_404(Vclans, pk=pk)

    badges = [member.get_new_badge() for member in vclan.humen_set.all() ]

    return make_pdf_response({ 'qs' :badges }, 'badge_qs.html')


# --------------------------------------------------------------

@staff_member_required
def check_in(request):
    return render_to_response('check-in.html')

@staff_member_required
def api_vclans_list(request):
    
    vclans = [clan.nome for clan in Vclans.objects.all()]
    
    return HttpResponse(json.dumps(vclans), content_type="application/json")

@staff_member_required
@csrf_exempt
def api_set_vclan_arrived(request):

    if not 'vclanid' in request.POST:
        return HttpResponse(
            json.dumps({'status': 'error', 'message': 'Devi inserire il clan arrivato'}),
            content_type="application/json"
        )

    clan = Vclans.objects.get(idvclan=request.POST['vclanid'])
    clan.update_arrivo_al_campo(True)
    clan.save()

    return HttpResponse(json.dumps({'status': 'OK'}), content_type="application/json")

@staff_member_required
@csrf_exempt
def api_search_vclan(request):

    if not 'vclan' in request.POST:
        return HttpResponse(
            json.dumps({'status': 'error', 'message': 'Devi inserire il clan da cercare'}),
            content_type="application/json"
        )

    response = []

    for clan in Vclans.objects.filter(nome=request.POST['vclan']):
        route = []
        for friend in  Vclans.objects.filter(route_num=clan.route_num):
            el = {
                'nome': friend.nome,
                'route': friend.route_num,
                'idvclan': friend.idvclan,
                'npersone': friend.humen_set.count(),
                'quartiere': friend.quartiere.name,
                'contrada': friend.contrada,
                'arrivato': friend.arrivato_al_campo,
            }
            route.append(el)
        response.append({'route': clan.route_num, 'clans': route})

    return HttpResponse(json.dumps(response), content_type="application/json")

