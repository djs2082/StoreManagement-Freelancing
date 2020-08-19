from rest_framework import routers
from .views import PaymentView
from django.urls import path
from .views import PaymentMethods

urlpatterns = [
    path('',PaymentView.as_view()),
    path('<int:pk>/',PaymentView.as_view()),
    path('payments_today/',PaymentMethods.as_view()),
]