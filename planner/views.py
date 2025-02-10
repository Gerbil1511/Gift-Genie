# planner/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Planner
from .forms import EventForm
from friendslist.models import Friendship
from django.contrib.auth.models import User
from django.contrib import messages


@login_required
def planner_view(request):
    user_events = Planner.objects.filter(user=request.user)
    friends_events = Planner.objects.filter(user__in=request.user.friends.all())
    return render(request, 'planner/planner.html', {'events': events, 'friends_events': friends_events})

# @login_required
# def get_events(request):
#     events = Planner.objects.filter(user=request.user)
#     events_list = []
#     for event in events:
#         events_list.append({
#             'title': event.event_name,
#             'start': event.event_date.isoformat(),  # Start date
#             'end': (event.event_date + timedelta(days=1)).isoformat(),  # End date (next day)
#             'description': event.description,
#         })
#     return JsonResponse(events_list, safe=False)


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, 'Event added successfully!')
            return redirect('planner:planner_view')
    else:
        form = EventForm()
    return render(request, 'planner/add_event.html', {'form': form})



@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Planner, id=event_id, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('planner:planner_view')
    else:
        form = EventForm(instance=event)
    return render(request, 'planner/edit_event.html', {'form': form})



@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Planner, id=event_id, user=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('planner:planner_view')
    return render(request, 'planner/delete_event.html', {'event': event})