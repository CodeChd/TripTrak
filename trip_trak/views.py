from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy


from .models import Trip, Note

# Create your views here.
class HomeView(TemplateView):
    template_name = 'trip_trak/index.html' 


def trip_list(request):
    trips = Trip.objects.filter(owner=request.user.id)
    context = {
        'trips': trips
    }
    return render(request, 'trip_trak/trip_list.html', context)


class TripCreateView(CreateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ['city', 'country', 'start_date', 'end_date']


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TripDetailView(DetailView):
    model = Trip 

    # data stored on trip
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = context['object']
        notes = trip.notes.all()
        context['notes'] = notes

        return context


class TripUpdateView(UpdateView):
    model = Trip
    success_url = reverse_lazy("trip-list")
    fields = ['city', 'country', 'start_date', 'end_date']

class TripDeleteView(DeleteView):
    model = Trip
    success_url = reverse_lazy("trip-list")






class NoteDetailView(DetailView):
    model = Note


class NoteListView(ListView):
    model = Note

    # fetch only notes of the active user
    def get_queryset(self):
        queryset = Note.objects.filter(trip__owner=self.request.user) 
        return queryset
    

class NoteCreateView(CreateView):
    model = Note
    success_url = reverse_lazy("note-list")
    fields = "__all__"


    def get_form(self):
         form = super(NoteCreateView, self).get_form()
         trips = Trip.objects.filter(owner=self.request.user)
         form.fields['trip'].queryset = trips
         return form



class NoteUpdateView(UpdateView):
    model = Note
    success_url = reverse_lazy("note-list")
    fields = "__all__"


    def get_form(self):
         form = super(NoteUpdateView, self).get_form()
         trips = Trip.objects.filter(owner=self.request.user)
         form.fields['trip'].queryset = trips
         return form

class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy("note-list")
    
