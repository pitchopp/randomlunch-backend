from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from backend import views
from randomlunch import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/persons', views.persons),
    path('api/sessions', views.sessions),
    path('api/sessions/random', views.random_session),
    path('api/sessions/<int:session_id>/validate', views.validate_session),
    path('api/sessions', views.sessions),
    path('api/updateSessions', views.update_sessions)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
