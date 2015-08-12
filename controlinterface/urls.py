from django.conf.urls import patterns, url
from controlinterface import views
from controlinterface.forms import AuthLoginForm

urlpatterns = patterns(
    '',
    # Setting the urlpatterns to hook into the api urls
    url(r'^api/v1/controlinterface/metric/', views.metric, name='metric'),
    url(r'^controlinterface/$', views.index, name='index'),
    url(r'^controlinterface/message/$', views.message_edit,
        name='message_edit'),
    url(r'^controlinterface/dashboard/(?P<dashboard_id>\d+)/', views.dashboard,
        name='dashboard'),
    # url(r'^controlinterface/subscription/$', views.subscription_edit,
    #     name='subscription_edit'),
    # url(r'^controlinterface/servicerating/download/',
    #     views.servicerating_report, name='servicerating_report'),
    # url(r'^controlinterface/servicerating/',
    #     views.servicerating, name='servicerating'),
    url(r'^controlinterface/login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'controlinterface/login.html',
            'authentication_form': AuthLoginForm,
        }, name='login'),
)
