from django.urls import path

from . import views

app_name = 'mentoring'
urlpatterns = [
    path('register/', views.MentorCreateView.as_view(), name='create-mentor'),
    path('register/done/', views.MentorCreateDoneView.as_view(), name='create-mentor-done'),
    path('mentors/', views.MentorListView.as_view(), name='mentor-list'),
    path('program/all/', views.ProgramListView.as_view(), name='program-list'),
    path('program/create/', views.ProgramCreateView.as_view(), name='program-create'),
    path('program/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program-delete'),
]