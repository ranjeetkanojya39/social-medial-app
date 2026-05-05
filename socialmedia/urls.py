from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userauth.urls')),
]

# ✅ MEDIA files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ⭐ STATIC files (IMPORTANT FIX)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)