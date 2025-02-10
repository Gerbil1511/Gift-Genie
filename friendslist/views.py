from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Friendship
from .forms import AddFriendForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from planner.models import Planner
from wishlist.models import WishlistItem


def search_usernames(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('term', '')
        users = User.objects.filter(username__icontains=query)
        results = [user.username for user in users]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


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


class FriendshipListView(ListView):
    model = Friendship
    template_name = 'friendslist/friendslist.html'
    context_object_name = 'friendships'

    def get_queryset(self):
        return Friendship.objects.filter(
            user=self.request.user, confirmed=True
            )


def create_friendship(request):
    if request.method == 'POST':
        user = request.user
        friend_id = request.POST.get('friend_id')
        friend = User.objects.get(id=friend_id)
        friendship = Friendship(user=user, friend=friend)
        try:
            friendship.save()
            return redirect('success_url')
        except ValidationError as e:
            return render(request, 'friendship_form.html', {'error': e.message})
    return render(request, 'friendship_form.html')


def confirm_friendship(request, friendship_id):
    friendship = get_object_or_404(
        Friendship, id=friendship_id, friend=request.user
        )
    if request.method == 'POST':
        friendship.confirmed = True
        friendship.save()
        return HttpResponseRedirect(reverse('friendslist'))


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
