from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report_incident, name='report_incident'),
    path('thanks/<str:token>/', views.thanks, name='thanks'),
    path('track/', views.track, name='track'),
    path('track/<str:token>/', views.track_detail, name='track_detail'),
    path('authority/', views.authority_dashboard, name='authority_dashboard'),
    path('authority/incident/<int:pk>/', views.manage_incident, name='manage_incident'),
    path('api/incidents/', views.incidents_api, name='incidents_api'),
]
