from django.urls import path
from crosschain_swap_sign.views import sign_view

urlpatterns = [
    path('sign/', sign_view)
]
