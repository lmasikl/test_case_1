from django.conf.urls import include, url
from django.contrib import admin

from case.views import AccountsView, AccountView

urlpatterns = [
    url(r'account/$', AccountView.as_view(), name='account'),
    url(r'account/(?P<pk>\d+)/$', AccountView.as_view(), name='account'),
    url(r'accounts/$', AccountsView.as_view(), name='accounts'),

    url(r'^admin/', include(admin.site.urls)),
]
