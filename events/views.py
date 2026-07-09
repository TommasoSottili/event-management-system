from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, EventForm
from .models import Comment, Event, Registration


class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context["is_registered"] = self.object.registrations.filter(
                attendee=user
            ).exists()
        context["comment_form"] = CommentForm()
        return context


class OrganizerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_organizer

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated


class EventOwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.get_object().organizer == self.request.user

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated


class EventCreateView(OrganizerRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)


class EventUpdateView(EventOwnerRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"


class EventDeleteView(EventOwnerRequiredMixin, DeleteView):
    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("event-list")


@login_required
@require_POST
def register_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer == request.user:
        messages.warning(request, "Non puoi iscriverti a un evento che organizzi tu.")
    else:
        registration, created = Registration.objects.get_or_create(
            event=event, attendee=request.user
        )
        if created:
            messages.success(request, "Iscrizione confermata!")
        else:
            messages.info(request, "Eri gia iscritto a questo evento.")
    return redirect("event-detail", pk=pk)


@login_required
@require_POST
def unregister_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    Registration.objects.filter(event=event, attendee=request.user).delete()
    messages.success(request, "Iscrizione annullata.")
    return redirect("event-detail", pk=pk)


@login_required
@require_POST
def add_comment(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.event = event
        comment.author = request.user
        comment.save()
        messages.success(request, "Commento aggiunto.")
    else:
        messages.error(request, "Il commento non puo essere vuoto.")
    return redirect("event-detail", pk=pk)


@login_required
@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user or comment.event.organizer == request.user:
        event_pk = comment.event.pk
        comment.delete()
        messages.success(request, "Commento eliminato.")
        return redirect("event-detail", pk=event_pk)
    raise PermissionDenied


class EventParticipantsView(EventOwnerRequiredMixin, DetailView):
    model = Event
    template_name = "events/event_participants.html"
    context_object_name = "event"


class MyEventsView(LoginRequiredMixin, ListView):
    template_name = "events/my_events.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)


class MyRegistrationsView(LoginRequiredMixin, ListView):
    template_name = "events/my_registrations.html"
    context_object_name = "registrations"

    def get_queryset(self):
        return Registration.objects.filter(attendee=self.request.user)
