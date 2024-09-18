
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from portfolio import settings

urlpatterns = [
    path('', include('dems.urls')),
    path('dems/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)