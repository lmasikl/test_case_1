from django.conf.urls import include, url
from django.contrib import admin

from case.views import (AccountsListView, AccountView, DepartmentsListView,
                        DepartmentView, FactPaymentsListView, PaymentView,
                        PlanedPaymentsListView, ProjectsListView, ProjectView)

urlpatterns = [
    url(r'account/$', AccountView.as_view(), name='account'),
    url(r'account/(?P<pk>\d+)/$', AccountView.as_view(), name='account'),
    url(r'accounts/$', AccountsListView.as_view(), name='accounts'),

    url(r'department/$', DepartmentView.as_view(), name='department'),
    url(r'department/(?P<pk>\d+)/$', DepartmentView.as_view(), name='department'),
    url(r'departments/$', DepartmentsListView.as_view(), name='departments'),

    url(r'project/$', ProjectView.as_view(), name='project'),
    url(r'project/(?P<pk>\d+)/$', ProjectView.as_view(), name='project'),
    url(r'projects/$', ProjectsListView.as_view(), name='projects'),

    url(r'payment/$', PaymentView.as_view(), name='payment'),
    url(r'payment/(?P<pk>\d+)/$', PaymentView.as_view(), name='payment'),
    url(r'payments/planed/$', PlanedPaymentsListView.as_view(), name='planed-payments'),
    url(r'payments/fact/$', FactPaymentsListView.as_view(), name='fact-payments'),
]
