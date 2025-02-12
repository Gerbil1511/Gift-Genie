from django.urls import path
from . import views

urlpatterns = [
    path('', views.friendship_list, name='friendslist'),
    path('confirm/<int:friendship_id>/', views.confirm_friendship, name='confirm_friendship'),
    # path('search-usernames/', views.search_usernames, name='search-usernames'),
    path('add-friend/', views.add_friend, name='add_friend'),
    path('friend/<int:friend_id>/', views.friendsdetail, name='friendsdetail'),
]
