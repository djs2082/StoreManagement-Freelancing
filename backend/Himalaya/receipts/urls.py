from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import Receipt,SalesForGraph

app_name="receipts"

urlpatterns = [
	path('',Receipt.as_view()),
	path('sales_for_graph/',SalesForGraph.as_view()),
# 	path('sendsms/',sendsms),
]