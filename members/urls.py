from django.urls import path

from . import views

app_name = 'members'
urlpatterns = [
    path('', views.MemberListView.as_view(), name='member_list'),
    path('profile/', views.UserProfileFormView.as_view(), name='profile_form'),
]
