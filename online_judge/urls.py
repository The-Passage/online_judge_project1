from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('problems.urls')),
    path('contest/',include('contest.urls')),
    path('clearification/',include('clearification.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
