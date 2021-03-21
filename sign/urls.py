from django.urls import path
from sign.views import sign_view

urlpatterns = [
    path('sign/', sign_view)
]
