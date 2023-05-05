from django.contrib import admin
from .views import user_admin, user_edit, user_delete, recent_actions, CategoryListing, CategoryUpdate, CreateCategory, category_delete, CustomLogoutView, WinnerListing, CreateWinner, BidListing, BidList, BidDelete, BidEdit
from django.urls import path, include
from .views import admin_login, dashboard, Listings, DeleteListing, EditListing, CommentsListing, Comments, CommentUpdateView, DeleteComment

urlpatterns = [
    path('ad_login/', admin_login, name="ad_login"),
    path('dashboard/', dashboard, name="dashboard"),
    path('listing/', Listings.as_view(), name="listingadmin"),
    path('delete-listing/<int:pk>', DeleteListing.as_view(), name="deletelisting"),
    path('edit-listing/<int:pk>/edit/',
         EditListing.as_view(), name="editlisting"),
    path('comments-listing/', CommentsListing.as_view(), name="commentslisting"),
    path('listing/<int:pk>/comments/',
         Comments.as_view(), name="listingcomments"),
    path('listing/<int:listing_pk>/comment/<int:pk>/edit/',
         CommentUpdateView.as_view(), name="commentedit"),
    path('listing/<int:listing_pk>/comment/<int:pk>/delete/',
         DeleteComment.as_view(), name="deletecomment"),
    path('user_admin/', user_admin, name='user_admin'),
    path('user_admin/users/<int:user_id>/edit/', user_edit, name='user_edit'),
    path('user_admin/users/<int:user_id>/delete/',
         user_delete, name="user_delete"),
    path('admin_logs/', recent_actions, name="admin_logs"),
    path('admin_category/', CategoryListing.as_view(), name="admin_category"),
    path('admin_category/<int:pk>/edit/',
         CategoryUpdate.as_view(), name="admin_category_edit"),
    path('create_category/', CreateCategory.as_view(), name="create_category"),
    path('user_admin/category/<int:category_id>/delete/',
         category_delete, name="category_delete"),
    path('user_admin/winners/', WinnerListing.as_view(), name="winner_listing"),
    path('user_admin/winner/create', CreateWinner.as_view(), name="create_winner"),
    path('user_admin/bid/listing/', BidListing.as_view(), name="bidlisting"),
    path('user_admin/<int:pk>/bid/',
         BidList.as_view(), name="bid_list"),
    path('user_admin/<int:listing_pk>/bid/<int:pk>/edit/',
         BidEdit.as_view(), name="bidedit"),
    path('user_admin/<int:listing_pk>/bid/<int:pk>/delete/',
         BidDelete.as_view(), name="deletebid"),

    path("ad_logout/", CustomLogoutView.as_view(next_page='ad_login'), name="ad_logout"),
]
