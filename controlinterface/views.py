from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist

from go_http.metrics import MetricsApiClient
from django.conf import settings

from .models import Dashboard, UserDashboard
from .forms import MessageFindForm, SubscriptionFindForm


def get_user_dashboards(request):
    if (request.user.has_perm('controlinterface.view_dashboard_private') or
            request.user.has_perm('controlinterface.view_dashboard_summary')):
        user_dashboards = UserDashboard.objects.get(user=request.user)
        dashboards = {}
        for dash in user_dashboards.dashboards.all():
            dashboards[dash.id] = dash.name
        return {"dashboards": dashboards}
    else:
        return {"dashboards": {}}


@login_required(login_url='/controlinterface/login/')
def index(request):
    if (request.user.has_perm('controlinterface.view_dashboard_private') or
            request.user.has_perm('controlinterface.view_dashboard_summary')):

        user_dashboards = UserDashboard.objects.get(user=request.user)
        return redirect('dashboard',
                        dashboard_id=user_dashboards.default_dashboard.id)
    else:
        return render(request,
                      'controlinterface/index_nodash.html')


@login_required(login_url='/controlinterface/login/')
def dashboard(request, dashboard_id):
    context = get_user_dashboards(request)
    if (request.user.has_perm('controlinterface.view_dashboard_private') or
            request.user.has_perm('controlinterface.view_dashboard_summary')):

        try:
            access = Dashboard.objects.get(
                id=dashboard_id).dashboards.filter(
                user=request.user).count()

            if access == 1:
                dashboard = Dashboard.objects.get(id=dashboard_id)
                dashboard_widgets = dashboard.widgets.all()
                widgets = {}
                for widget in dashboard_widgets:
                    widgets[widget.id] = {
                        "config": widget,
                        "data": widget.data.all()
                    }
                context.update({
                    "widgets": widgets,
                    "dashboard_api_key": settings.DASHBOARD_API_KEY
                })
                return render(request,
                              'controlinterface/index.html',
                              context)
            else:
                return render(request,
                              'controlinterface/index_notdashallowed.html')
        except ObjectDoesNotExist:
            # User tried to access a dashboard they're not allowed to
            return render(request,
                          'controlinterface/index_notdashallowed.html')
    else:
        return render(request,
                      'controlinterface/index_nodash.html')


@login_required(login_url='/controlinterface/login/')
def message_edit(request):
    if (request.user.has_perm('controlinterface.view_dashboard_private') or
            request.user.has_perm('controlinterface.view_dashboard_summary')):

        context = get_user_dashboards(request)
        form = MessageFindForm()
        context.update({"form": form})
        context.update(csrf(request))

        return render_to_response("controlinterface/messages.html",
                                  context,
                                  context_instance=RequestContext(request))
    else:
        return render(request,
                      'controlinterface/index_nodash.html')


@login_required(login_url='/controlinterface/login/')
def subscription_edit(request):
    if (request.user.has_perm('controlinterface.view_dashboard_private') or
            request.user.has_perm('controlinterface.view_dashboard_summary')):

        context = get_user_dashboards(request)
        form = SubscriptionFindForm()
        context.update({"form": form})
        context.update(csrf(request))

        return render_to_response("controlinterface/subscription.html",
                                  context,
                                  context_instance=RequestContext(request))
    else:
        return render(request,
                      'controlinterface/index_nodash.html')


@login_required(login_url='/controlinterface/login/')
def servicerating(request):
    if (request.user.has_perm('controlinterface.view_dashboard_private') or
            request.user.has_perm('controlinterface.view_dashboard_summary')):

        context = get_user_dashboards(request)
        context.update(csrf(request))

        return render_to_response("controlinterface/serviceratings.html",
                                  context,
                                  context_instance=RequestContext(request))
    else:
        return render(request,
                      'controlinterface/index_nodash.html')


@login_required(login_url='/controlinterface/login/')
def metric(request):
    # load json fixture for demo

    client = MetricsApiClient(settings.VUMI_GO_API_TOKEN,
                              settings.VUMI_GO_API_URL)

    filters = {
        "m": [],
        "start": "",
        "interval": "",
        "nulls": ""
    }

    for k, v in request.GET.lists():
        filters[k] = v

    results = []
    for metric in filters['m']:
        start = filters['start'][0]
        interval = filters['interval'][0]
        nulls = filters['nulls'][0]
        response = client.get_metric(metric, start, interval, nulls)
        div = 0.7
        if metric in response:
            detail = []
            for res in response[metric]:
                detail.append({"x": res["x"], "y": int(res["y"] * div)})
            values = detail
        else:
            values = []
        results.append({"key": metric, "values": values})

    fakeapi = {
        "meta": {
            "limit": 20, "next": None, "offset": 0, "previous": None,
            "total_count": 1
        },
        "objects": results
    }
    return JsonResponse(fakeapi)
