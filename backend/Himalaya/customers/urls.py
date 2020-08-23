from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from customers import views

app_name="customers"

urlpatterns = [
	path("",views.CustomerView.as_view(),name="Customer"),
	path("bday/",views.get_bday,name="bdays")
]