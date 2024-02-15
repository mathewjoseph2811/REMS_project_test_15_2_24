from django.urls import path
from .views import *

app_name = 'property'

urlpatterns = [
    path('property_list', PropertyList.as_view(), name='property_list'),
    path('add_property', AddProperty.as_view(), name='add_property'),
    path('view_property/<int:id>', ViewProperty.as_view(), name='view_property'),
]