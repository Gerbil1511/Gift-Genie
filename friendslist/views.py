from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Friendship
from .forms import AddFriendForm
from planner.models import Planner
from wishlist.models import WishlistItem

def search_usernames(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('term', '')
        users = User.objects.filter(username__icontains=query)
        results = [
            {
                'username': user.username,
                'profile_image': user.myaccount.profile_image.url if user.myaccount.profile_image else ''
            }
            for user in users
        ]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)  # If it's not an AJAX request, return an empty list

@login_required
def friendship_list(request):
    friendships = Friendship.objects.filter(user=request.user, confirmed=True)
    pending_friendships = Friendship.objects.filter(friend=request.user, confirmed=False)
    form = AddFriendForm(user=request.user)
    return render(request, 'friendslist/friendslist.html', {
        'friendships': friendships,
        'pending_friendships': pending_friendships,
        'form': form
    })

@login_required
def add_friend(request):
    if request.method == 'POST':
        form = AddFriendForm(request.POST, user=request.user)
        if form.is_valid():
            friend_username = form.cleaned_data['friend_username']
            friend = User.objects.get(username=friend_username)
            Friendship.objects.create(user=request.user, friend=friend)
            return redirect('friendslist')  # Redirect to the friends list page
        else:
            # Add an error message if the form is invalid
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('friendslist')
    else:
        form = AddFriendForm(user=request.user)
    return render(request, 'friendslist/add_friend.html', {'form': form})

@login_required
def friendsdetail(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    events = Planner.objects.filter(user=friend)
    wishlist_items = WishlistItem.objects.filter(user=friend)
    return render(request, 'friendslist/frienddetail.html', {
        'friend': friend,
        'events': events,
        'wishlist_items': wishlist_items
    })

@login_required
def confirm_friendship(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id, friend=request.user)
    if request.method == 'POST':
        friendship.confirmed = True
        friendship.save()
        return HttpResponseRedirect(reverse('friendslist'))
    return render(request, 'friendslist/confirm_friendship.html', {'friendship': friendship})