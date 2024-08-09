from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('HCODajHGIRNJFkKmjTQJpAsQ/', admin.site.urls),
    path('', include('app.urls')),
]

# Serving media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serving static files during development
urlpatterns += staticfiles_urlpatterns()
