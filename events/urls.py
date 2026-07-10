from django.urls import path

from . import views

urlpatterns = [
    path("", views.EventListView.as_view(), name="event-list"),
    path("event/new/", views.EventCreateView.as_view(), name="event-create"),
    path("event/<int:pk>/", views.EventDetailView.as_view(), name="event-detail"),
    path("event/<int:pk>/edit/", views.EventUpdateView.as_view(), name="event-update"),
    path("event/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event-delete"),
    path("event/<int:pk>/register/", views.register_event, name="event-register"),
    path("event/<int:pk>/unregister/", views.unregister_event, name="event-unregister"),
    path("event/<int:pk>/participants/", views.EventParticipantsView.as_view(), name="event-participants"),
    path("event/<int:pk>/comment/", views.add_comment, name="add-comment"),
    path("comment/<int:pk>/delete/", views.delete_comment, name="delete-comment"),
    path("organizer/<int:pk>/", views.OrganizerProfileView.as_view(), name="organizer-profile"),
    path("organizer/<int:pk>/rate/", views.rate_organizer, name="rate-organizer"),
    path("my/events/", views.MyEventsView.as_view(), name="my-events"),
    path("my/registrations/", views.MyRegistrationsView.as_view(), name="my-registrations"),
]
