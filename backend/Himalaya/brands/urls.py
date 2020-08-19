from brands import views
from django.urls import path

urlpatterns = [
    path('',views.BrandView.as_view()),
    path('get_brands/<int:pk>/',views.get_brands),
    path('<int:pk>/',views.BrandView.as_view())
]