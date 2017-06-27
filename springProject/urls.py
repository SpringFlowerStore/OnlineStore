from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^login/', include('apps.bestLogin.urls', namespace='users')),
    url(r'^', include('apps.imageApp.urls', namespace='spring')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
