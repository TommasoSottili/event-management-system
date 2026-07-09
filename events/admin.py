from django.contrib import admin

from .models import Comment, Event, Registration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location", "organizer")
    list_filter = ("date",)
    search_fields = ("title", "location")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "attendee", "registered_at")
    list_filter = ("event",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("event", "author", "created_at")
    list_filter = ("event",)
