from items import views
from django.urls import path

urlpatterns = [
    path('',views.ItemView.as_view()),
    path('<int:pk>/',views.ItemView.as_view()),
    path('itemsBrand/',views.get_items_and_brands)
]