from django.urls import path

from meetings import views

app_name = 'meetings'
urlpatterns = [
    path('invite/', views.SendInvite.as_view(), name='invite'),
    path('invite/success/', views.SendInviteSuccess.as_view(), name='invite-success'),
]
