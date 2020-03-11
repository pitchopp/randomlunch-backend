from django.contrib import admin
from django.urls import path
from backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/persons', views.persons),
    path('api/sessions', views.sessions),
    path('api/sessions/random', views.random_session),
    path('api/sessions/<int:session_id>/validate', views.validate_session),
    path('api/sessions', views.sessions)
]
