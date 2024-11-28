from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from portfolio import settings

urlpatterns = [
    path("", include("dems.urls")),
    path("dems/", admin.site.urls),
    path("accounts/", include("myauth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:  # Assurez-vous que c'est en mode DEBUG
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
