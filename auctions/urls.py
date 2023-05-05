
from django.urls import path
from . import views
from .views import CreateListing, Listings, ListingDetail, DeleteListing, UpdateBidView, Comment, WatchlistItem, Create_Watchlist, Bid_Winner, DeleteWatchlist, UserProfile, UserListing, MyWinners, MyBids, MyWins


urlpatterns = [
    path('', Listings.as_view(), name="index"),
    path('create/', CreateListing.as_view(), name="create"),
    path('delete/<int:pk>/', DeleteListing.as_view(), name='delete'),
    path('listing/', Listings.as_view(), name="listing"),
    path('listing-details/<int:pk>/',
         ListingDetail.as_view(), name="listing_detail"),
    path('listing_update/<int:pk>/',
         UpdateBidView.as_view(), name='bid_update'),
    path('comment/<int:pk>/', Comment.as_view(), name="comment"),
    path('watchlist/', WatchlistItem.as_view(), name="watchlist"),
    path('create_watchlist/create/<int:listing_id>/',
         Create_Watchlist.as_view(), name='create_watchlist'),
    path('delete_watchlist/<int:pk>/',
         DeleteWatchlist.as_view(), name="delete_watchlist"),
    path('winner/<int:listing_id>/', Bid_Winner.as_view(), name='winner'),
    path('profile/<int:pk>/', UserProfile.as_view(), name="user_profile"),
    path('my_list', UserListing.as_view(), name="mylist"),
    path('my_winners', MyWinners, name="mywinners"),
    path('my_bids', MyBids, name="my_bids"),
    path('my_wins', MyWins, name="my_wins")

]
