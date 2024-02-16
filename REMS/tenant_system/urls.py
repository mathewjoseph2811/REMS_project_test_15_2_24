from django.urls import path
from .views import *

app_name = 'tenant_system'

urlpatterns = [
    path('tenant_list', TenantList.as_view(), name='tenant_list'),
    path('add_tenant', AddTenant.as_view(), name='tenant'),
    path('view_tenant/<int:id>', ViewTenant.as_view(), name='view_tenant'),
    path('search_list', SearchList.as_view(), name='search_list'),
]