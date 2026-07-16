from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    path('api/', include('tracker.api_urls')),
]
