from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from users.views import index


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path('api/v1/', include('api.urls')),
    path("", index, name="index"),
] + i18n_patterns(
    path('admin/', admin.site.urls),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)