from django.urls import path

from . import views

app_name = 'mentoring'
urlpatterns = [
    path('program/', views.ProgramListView.as_view(), name='program-list'),
    path('program/add/', views.ProgramCreateView.as_view(), name='program-create'),
    path('program/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program-delete'),
    path('mentor/', views.MentorListView.as_view(), name='mentor-list'),
    path('mentor/add/', views.MentorCreateView.as_view(), name='mentor-create'),
    path('mentor/add/done/', views.MentorCreateDoneView.as_view(), name='mentor-create-done'),
    path('mentor/<int:pk>/', views.MentorDetailView.as_view(), name='mentor-detail'),
]
