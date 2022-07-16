from django.urls import path

from . import views

app_name = 'mentoring'
urlpatterns = [
    path('registration/', views.RegistrationListView.as_view(), name='registration-list'),
    path('registration/add/', views.RegistrationCreateView.as_view(), name='registration-create'),
    path('registration/<int:pk>/delete/', views.RegistrationDeleteView.as_view(), name='registration-delete'),
    path('program/', views.ProgramListView.as_view(), name='program-list'),
    path('program/add/', views.ProgramCreateView.as_view(), name='program-create'),
    path('program/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program-delete'),
    path('mentor/', views.MentorListView.as_view(), name='mentor-list'),
    path('mentor/export/', views.export_mentors_as_csv, name='mentor-list-export'),
    path('mentor/add/', views.MentorCreateView.as_view(), name='mentor-create'),
    path('mentor/add/done/', views.MentorCreateDoneView.as_view(), name='mentor-create-done'),
    path('mentor/<int:pk>/', views.MentorDetailView.as_view(), name='mentor-detail'),
    path('helper/', views.HelperListView.as_view(), name='helper-list'),
    path('helper/export/', views.export_helpers_as_csv, name='helper-list-export'),
    path('helper/add/', views.HelperCreateView.as_view(), name='helper-create'),
    path('helper/add/done/', views.HelperCreateDoneView.as_view(), name='helper-create-done'),
    path('helper/<int:pk>/', views.HelperDetailView.as_view(), name='helper-detail'),
]
