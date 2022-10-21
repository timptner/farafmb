from django.urls import path

from . import views

app_name = 'consultations'
urlpatterns = [
    path('', views.ConsultationsView.as_view(), name='main'),
    path('add/', views.ConsultationCreateView.as_view(), name='consultation-create'),
    path('list/', views.ConsultationListView.as_view(), name='consultation-list'),
    path('<int:pk>/', views.ConsultationUpdateView.as_view(), name='consultation-update'),
]