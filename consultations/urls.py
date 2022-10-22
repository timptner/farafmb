from django.urls import path

from . import views

app_name = 'consultations'
urlpatterns = [
    path('', views.OfficeHoursView.as_view(), name='office-hours'),
    path('consultation/add/', views.ConsultationCreateView.as_view(), name='consultation-create'),
    path('consultation/list/', views.ConsultationListView.as_view(), name='consultation-list'),
    path('consultation/<int:pk>/update/', views.ConsultationUpdateView.as_view(), name='consultation-update'),
    path('consultation/<int:pk>/delete/', views.ConsultationDeleteView.as_view(), name='consultation-delete'),
]