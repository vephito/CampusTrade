from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect
from .models import Listing, Bid, Comment, Watchlist, Winner, User, Category
from .forms import BidForm, CommentForm


def index(request):
    return render(request, 'auctions/index.html')


class CreateListing(CreateView):
    model = Listing
    fields = ['title', 'image', 'price', 'description', 'category', 'sold']
    template_name = 'auctions/create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateListing, self).form_valid(form)


class Listings(ListView):
    model = Listing
    template_name = 'auctions/listing.html'
    context_object_name = 'listings'
    paginate_by = 9
    ordering = ['-date_created']


class DeleteListing(DeleteView):
    model = Listing
    context_object_name = 'listings'
    success_url = reverse_lazy('listing')


class ListingDetail(DetailView):
    model = Listing
    # fields = "__all__"
    # form_class = BidForm
    context_object_name = 'listings'
    template_name = 'auctions/listdetail.html'
    # success_url = reverse_lazy('listing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form1'] = BidForm()
            context['form2'] = CommentForm()
        return context


class UpdateBidView(CreateView):
    model = Bid
    form_class = BidForm
    template_name = 'auctions/bidform.html'

    def form_valid(self, form):
        bidamount = form.cleaned_data['bid_amount']
        listing = get_object_or_404(Listing, pk=self.kwargs['pk'])
        form.instance.bidder = self.request.user
        form.instance.listing = get_object_or_404(
            Listing, pk=self.kwargs['pk'])
        form.instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Get the primary key of the listing associated with the bid object
        listing_pk = self.object.listing.pk
        # Redirect to the listing detail page for the associated listing
        return reverse_lazy('listing_detail', kwargs={'pk': listing_pk})


class Comment(CreateView):
    model = Comment
    fields = ['text']
    template_name = 'auctions/commentform.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.listing_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        listing_pk = self.object.listing.pk
        return reverse_lazy('listing_detail', kwargs={'pk': listing_pk})


class WatchlistItem(ListView):
    model = Watchlist
    context_object_name = 'watchlist'
    template_name = 'auctions/watchlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['watchlist'] = context['watchlist'].filter(
            user=self.request.user)
        context['count'] = context['watchlist'].count()
        return context


class Create_Watchlist(CreateView):
    model = Watchlist
    template_name = 'auctions/watchlist.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        listing_id = self.kwargs['listing_id']
        listing = get_object_or_404(Listing, pk=listing_id)
        if Watchlist.objects.filter(user=user, items=listing).exists():
            return redirect(request.META.get('HTTP_REFERER', '/'))
        Watchlist.objects.create(user=user, items=listing)
        return redirect(request.META.get('HTTP_REFERER', '/'))


class DeleteWatchlist(DeleteView):
    model = Watchlist
    context_object_name = 'watchlist'
    success_url = reverse_lazy('watchlist')


class Bid_Winner(CreateView):
    model = Winner
    template_name = 'auctions/close_bid.html'
    fields = []

    def get(self, request, *args, **kwargs):
        listing = Listing.objects.get(pk=self.kwargs['listing_id'])
        listing.sold = True
        listing.save()
        bid_winner = Bid.objects.filter(
            listing=listing).order_by('-bid_amount').first()
        if bid_winner:
            winner = Winner.objects.create(
                winner=bid_winner.bidder, win_item=listing)
            winner.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class UserProfile(DetailView):
    model = User
    template_name = 'auctions/user_profile.html'
    context_object_name = 'profile'


class UserListing(ListView):
    model = Listing
    template_name = 'auctions/user_listing.html'
    context_object_name = 'listings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listings'] = context['listings'].filter(
            user=self.request.user)
        return context
