from django.urls import path

from . import views

app_name = 'mentoring'
urlpatterns = [
    path('register/', views.MentorCreateView.as_view(), name='create-mentor'),
    path('register/done/', views.MentorCreateDoneView.as_view(), name='create-mentor-done'),
    path('mentors/', views.MentorListView.as_view(), name='mentor-list'),
]
