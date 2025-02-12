from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Planner
from friendslist.models import Friendship 
from .forms import EventForm
from django.contrib.auth.models import User
from django.contrib import messages
import json

@login_required
def planner_view(request):
    user_events = Planner.objects.filter(user=request.user)
    friends = Friendship.objects.filter(user=request.user, confirmed=True).values_list('friend_id', flat=True)
    friends_events = Planner.objects.filter(user__in=friends)
    return render(request, 'planner/planner.html', {'user_events': user_events, 'friends_events': friends_events})

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return JsonResponse({'success': True, 'event_id': event.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Planner, id=event_id, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Planner, id=event_id, user=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('planner:planner_view')
    return render(request, 'planner/delete_event.html', {'event': event})