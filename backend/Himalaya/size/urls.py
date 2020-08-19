from size import views
from django.urls import path

urlpatterns = [
    path('',views.SizeView.as_view()),
    path('<int:pk>/',views.SizeView.as_view())
]