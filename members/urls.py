from django.urls import path

from . import views

app_name = 'members'
urlpatterns = [
    path('', views.MemberListView.as_view(), name='member-list'),
    path('add/', views.UserCreateView.as_view(), name='user-create'),
    path('profile/', views.MemberCreateView.as_view(), name='member-create'),
    path('<int:pk>/edit/', views.MemberUpdateView.as_view(), name='member-update'),
]
