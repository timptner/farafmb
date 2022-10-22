from django.urls import path

from . import views

app_name = 'consultations'
urlpatterns = [
    path('', views.ConsultationListView.as_view(), name='consultation-list'),
    path('add/', views.ConsultationCreateView.as_view(), name='consultation-create'),
    path('<int:pk>/update/', views.ConsultationUpdateView.as_view(), name='consultation-update'),
    path('<int:pk>/delete/', views.ConsultationDeleteView.as_view(), name='consultation-delete'),
]