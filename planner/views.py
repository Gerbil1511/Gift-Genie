from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from .models import Planner
from friendslist.models import Friendship 
from .forms import EventForm
from django.contrib.auth.models import User
# from django.contrib import messages
import json



@login_required
def planner_view(request):
    # Render the main calendar template
    return render(request, 'planner/planner.html')

@login_required
def add_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = EventForm(data)
            if form.is_valid():
                event = form.save(commit=False)
                event.user = request.user
                event.save()
                return JsonResponse({
                    'success': True,
                    'event': {
                        'id': event.id,
                        'title': event.title,
                        'start': event.start.isoformat(),
                        'end': event.end.isoformat() if event.end else None
                    }
                })
            else:
                print("Form errors:", form.errors)  # Debug form issues
                return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            print("Error in add_event:", e)  # Catch unexpected errors
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid method'})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Planner, id=event_id, user=request.user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Debug incoming data

            form = EventForm(data, instance=event)
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'success': True,
                    'event': {
                        'id': event.id,
                        'title': event.title,
                        'start': event.start.isoformat(),
                        'end': event.end.isoformat() if event.end else None
                    }
                })
            else:
                print("Form errors:", form.errors)  # Debug form issues
                return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            print("Error in edit_event:", e)  # Catch unexpected errors
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid method'})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Planner, id=event_id, user=request.user)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid method'})

@login_required
def get_events(request):
    try:
        # Get events for the current user and their friends
        user_events = Planner.objects.filter(user=request.user)
        friends = Friendship.objects.filter(user=request.user, confirmed=True).values_list('friend_id', flat=True)
        friends_events = Planner.objects.filter(user__in=friends)
    
        # Serialize events
        events = []
        for event in user_events.union(friends_events):
            events.append({
                'id': event.id,
                'title': event.title,  # Match model
                'start': event.start.isoformat(),
                'end': event.end.isoformat() if event.end else None,
                'color': '#3788d8' if event.user == request.user else '#6c757d',
                'is_friend': event.user != request.user,  # Send friend status
                'owner': event.user.username,  # Send event owner's name
                'profile_image': event.user.profile.image.url if hasattr(event.user, 'profile') else None,  # Send profile pic
        })
        return JsonResponse({'events': events})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)