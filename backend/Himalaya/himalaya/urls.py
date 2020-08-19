"""himalaya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.views.static import serve
from django.contrib.auth.models import Group, User

admin.autodiscover()
admin.site.unregister(Token)
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = "Denim Factory Admin"
admin.site.site_title = "Denim Factory Admin Portal"
admin.site.index_title = "Welcome to Denim Factory Admin Portal"
admin.site.site_url="https://shield-1712.firebaseapp.com/"
admin.empty_value_display="Nothing to Display, Add by clicking on right side"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('owner/', include("owner.urls","owner")),
    path('customers/', include("customers.urls","customers")),
    path('payments/',include('payment.urls')),
    path('items/',include('items.urls')),
    path('brands/',include('brands.urls')),
    path('sizes/',include('size.urls')),
    path('receipts/',include('receipts.urls'))
]

@api_view(['GET'])
@permission_classes([])
def protected_serve(request, path, document_root=None, show_indexes=False):
    path=path.split("?Token=")
    if(len(path)>1):
        try:
            token=Token.objects.get(key=path[1])
            return serve(request, path[0], document_root, show_indexes)
        except Token.DoesNotExist:
            return Response({'authentication':'Authentication Credentials not provided/ Wrong Credentials'})
    else:
        return Response({'authentication':'Token should be provided with URL'})

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
