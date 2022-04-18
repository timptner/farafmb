from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.EventsView.as_view(), name='events'),
    path('<int:pk>/', views.InfoView.as_view(), name='info'),
    path('<int:pk>/register/', views.RegistrationView.as_view(), name='registration'),
    path('<int:pk>/register/done/', views.RegistrationDoneView.as_view(), name='registration_done'),
    path('<int:pk>/participants/', views.ParticipantView.as_view(), name='participants'),
    path('<int:pk>/participants/contact/', views.ParticipantsContactView.as_view(), name='participants_contact'),
    path('<int:pk>/participants/contact/done/', views.ParticipantsContactDoneView.as_view(),
         name='participants_contact_done'),
]
