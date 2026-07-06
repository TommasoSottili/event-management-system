from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField(
        "biografia",
        blank=True,
        help_text="Breve descrizione facoltativa dell'utente.",
    )

    def __str__(self):
        return self.username

    @property
    def is_organizer(self):
        return self.groups.filter(name="Organizer").exists()

    @property
    def is_attendee(self):
        return self.groups.filter(name="Attendee").exists()
