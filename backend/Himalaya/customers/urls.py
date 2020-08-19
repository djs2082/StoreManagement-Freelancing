from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import Customer

app_name="customers"

urlpatterns = [
	path("",Customer.as_view(),name="Customer"),
]