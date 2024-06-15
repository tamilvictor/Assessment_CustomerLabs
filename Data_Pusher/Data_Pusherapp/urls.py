from django.urls import path
from .views import AccountListCreate, AccountRetrieveUpdateDestroy, DestinationListCreate, DestinationRetrieveUpdateDestroy, IncomingData

urlpatterns = [
    path('accounts/', AccountListCreate.as_view(), name='account-list-create'),
    path('accounts/<uuid:pk>/', AccountRetrieveUpdateDestroy.as_view(), name='account-detail'),
    path('accounts/<uuid:account_id>/destinations/', DestinationListCreate.as_view(), name='destination-list-create'),
    path('destinations/<int:pk>/', DestinationRetrieveUpdateDestroy.as_view(), name='destination-detail'),
    path('server/incoming_data/', IncomingData.as_view(), name='incoming-data'),
]
