from django.conf import settings
from django.db import models
from django.urls import reverse


class Event(models.Model):
    title = models.CharField("titolo", max_length=200)
    description = models.TextField("descrizione")
    date = models.DateTimeField("data e ora")
    location = models.CharField("luogo", max_length=200)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events_organized",
        verbose_name="organizzatore",
    )

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event-detail", kwargs={"pk": self.pk})


class Registration(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations",
        verbose_name="evento",
    )
    attendee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="registrations",
        verbose_name="partecipante",
    )
    registered_at = models.DateTimeField("iscritto il", auto_now_add=True)

    class Meta:
        ordering = ["-registered_at"]
        unique_together = ("event", "attendee")

    def __str__(self):
        return f"{self.attendee} → {self.event}"
