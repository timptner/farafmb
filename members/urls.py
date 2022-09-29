from django.urls import path

from . import views

app_name = 'members'
urlpatterns = [
    path('update/', views.UserProfileFormView.as_view(), name='profile_form'),
    path('', views.MemberListView.as_view(), name='member-list'),
    path('add/', views.MemberCreateView.as_view(), name='member-create'),
    path('profile/', views.get_profile, name='profile'),
]
