from django.urls import path
from .views import token_balance, historical_data, transfer_token

urlpatterns = [
    path('token_balance/', token_balance),
    path('historical_data/', historical_data),
    path('transfer_token/', transfer_token),
]
