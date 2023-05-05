from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.db.models import Max, Q
from django.shortcuts import get_object_or_404, redirect
from .models import Listing, Bid, Comment, Watchlist, Winner, User, Category
from .forms import BidForm, CommentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db import models

# Create your views here.
# didn't check the mail yet


def send_overbid_email(last_bidder, bid_amount, listing):
    subject = f"You have been outbid on {listing.title}"
    message = f"Dear {last_bidder.username},\n\n" \
        f"You have been outbid on the following listing: {listing.title}.\n\n" \
        f"The current highest bid is ₹{bid_amount}.\n\n" \
        f"Thank you for participating in the auction.\n\n" \
        f"Best regards,\n" \
        f"The Auction Team"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [last_bidder.email])

# https://www.youtube.com/watch?v=dQw4w9WgXcQ


def send_participants_email(participants, winner, bid_amount):
    subject = 'The auction has ended'
    # message = f'The auction for {winner.win_item.title} has ended.'\
    #     f"{winner.winner} has Won the Auction with the bid of ${bid_amount}.\n\n" \
    #     f"Thank you for participating in the auction.\n\n" \
    #     f"Best regards,\n" \
    #     f"The Auction Team"
    message = f"""
    <html>
    <body>
    <p>The auction for <b>{winner.win_item.title}</b> has ended.</p>
              <p><b>{winner.winner}</b> has Won the Auction with the bid of <b>${bid_amount}</b>.</p>
              <p>Thank you for participating in the auction. Guess what? We have a surprise for you!</p>
              <p><a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">Click here to find out!</a>🎁</p>
              <br><br><p>Best regards,</p>
              <p>The Auction Team</p>
              </body>
              </html>"""

    from_email = settings.EMAIL_HOST_USER
    for participant in participants:

        send_mail(subject, '', from_email, [
                  participant.email], html_message=message)


def send_winner_email(winner):
    subject = "Congratulations! You Won the Auction"

    # message = f"Dear {winner.winner},\n\nI am delighted to inform you that you have won the auction for {winner.win_item.title}. Congratulations on your successful bid!\n\nPlease contact the seller, {winner.win_item.user.username}, at {winner.win_item.user.email}, to arrange for payment and collection of the item. The seller will be happy to discuss the logistics with you and answer any questions you may have.\n\nPlease note that as the winner of the auction, you are expected to complete the transaction within 7 days of receiving this email. If you encounter any issues or difficulties, please do not hesitate to contact us and we will be happy to assist you.\n\nThank you for participating in our auction and we hope that you will enjoy your new purchase.\n\nBest regards,\nThe Auction Team"
    message = f"""
        </head>
        <body>
            <div class="message-container">
            <h2>Congratulations! You Won the Auction</h2>
            <p>Dear {winner.winner},</p>
            <p>I am delighted to inform you that you have won the auction for {winner.win_item.title}. Congratulations on your successful bid!</p>
            <p><a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">Click here to Claim!</a>🎁</p>
            <p>Please contact the seller, {winner.win_item.user.username}, at <a href="mailto:{winner.win_item.user.email}">{winner.win_item.user.email}</a>, to arrange for payment and collection of the item. The seller will be happy to discuss the logistics with you and answer any questions you may have.</p>
            <p>Please note that as the winner of the auction, you are expected to complete the transaction within 7 days of receiving this email. If you encounter any issues or difficulties, please do not hesitate to <a href="mailto:campustradeofficial@gmail.com">contact us</a> and we will be happy to assist you.</p>
            <p>Thank you for participating in our auction and we hope that you will enjoy your new purchase.</p>
            <p>Best regards,</p>
            <p>The Auction Team</p>
            </div>
        </body>
        </html>
        """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [winner.winner.email]
    send_mail(subject, '', from_email,
              recipient_list, html_message=message)


def send_random_email(winner):
    subject = "Congratulations! You Won the Auction"
    # message = f'Dear {winner.winner},\n\nCongratulations! You won the auction for {winner.win_item.title}.\n\nPlease contact @{winner.win_item.user.email} to claim your item.\n\nThank you for participating in our auction.\n\nBest regards,\nThe Auction Team'
    message = f"""
        <html>
            <body>
                <p>Dear {winner},</p>
                <p style="font-size: 16px;">I am delighted to inform you that you have won the auction.</p>
                <p><a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">Click here to Claim!</a>🎁</p>
                <p style="font-size: 16px;">Congratulations on your successful bid!</p>
                <p style="font-size: 16px;">Please contact the seller, at to arrange for payment and collection of the item. The seller will be happy to discuss the logistics with you and answer any questions you may have.</p>
                <p style="font-size: 16px;">Please note that as the winner of the auction, you are expected to complete the transaction within 7 days of receiving this email. If you encounter any issues or difficulties, please do not hesitate to contact us and we will be happy to assist you.</p>
                <p style="font-size: 16px;">Thank you for participating in our auction and we hope that you will enjoy your new purchase.</p>
                <p style="font-size: 16px;">Best regards,<br>The Auction Team</p>
            </body>
        </html>
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [winner]
    send_mail(subject, message, from_email,
              recipient_list, html_message=message)


def index(request):
    return render(request, 'auctions/index.html')


class CreateListing(CreateView):
    model = Listing
    fields = ['title', 'image', 'price', 'description', 'category', 'sold']
    template_name = 'auctions/create.html'
    success_url = reverse_lazy('listing')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # return super(CreateListing, self).form_valid(form)
        response = super().form_valid(form)
        bid = Bid(
            bidder=self.request.user,
            listing=self.object,
            bid_amount=form.cleaned_data['price']
        )
        bid.save()
        return response


class Listings(ListView):
    model = Listing
    template_name = 'auctions/listing.html'
    context_object_name = 'listings'
    paginate_by = 9
    ordering = ['-date_created']

    def get_queryset(self):
        search_input = self.request.GET.get('search-area') or ''
        category = self.request.GET.get('category') or ''
        queryset = Listing.objects.filter(Q(sold=False) | Q(
            sold__isnull=True)).order_by('-date_created')
        if search_input:
            queryset = queryset.filter(title__icontains=search_input)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        search_input = self.request.GET.get('search-area') or ''

        context['search_input'] = search_input
        return context


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
        listing = self.get_object()
        winner = Winner.objects.filter(win_item=listing).first()
        current_highest_bid = listing.get_highest_bid()
        context['winner'] = winner
        context['highest'] = current_highest_bid
        if self.request.user.is_authenticated:
            context['form1'] = BidForm()
            context['form2'] = CommentForm()
        return context


class UpdateBidView(UpdateView):
    model = Bid
    form_class = BidForm
    template_name = 'auctions/bidform.html'

    def get_object(self, queryset=None):
        """
        Returns the Bid object that should be updated.
        """
        listing = get_object_or_404(Listing, pk=self.kwargs['pk'])
        try:
            bid = Bid.objects.get(listing=listing, bidder=self.request.user)
        except Bid.DoesNotExist:
            bid = Bid(listing=listing, bidder=self.request.user)
            bid.save()
        return bid

    def form_valid(self, form):
        bid_amount = form.cleaned_data['bid_amount']
        listing = get_object_or_404(Listing, pk=self.kwargs['pk'])
        current_highest_bid = listing.get_highest_bid()
        last_bidder = Bid.objects.filter(listing=listing, bid_amount=Bid.objects.filter(
            listing=listing).aggregate(max_bid=models.Max('bid_amount'))['max_bid']).first().bidder

        last_bidder = last_bidder
        current_bidder = self.request.user
        if bid_amount <= current_highest_bid:
            return self.form_invalid(form)
        send_overbid_email(last_bidder, bid_amount, listing)
        bid = form.save(commit=False)
        bid.listing = listing
        bid.bidder = self.request.user

        bid.save()
        messages.success(self.request, 'Bid successful!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Bid Failed! Amount must be higher than the current highest bid.')
        return redirect('listing_detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful form submission.
        """

        return reverse_lazy('listing_detail', kwargs={'pk': self.kwargs['pk']})


class Comment(CreateView):
    model = Comment
    fields = ['text']
    template_name = 'auctions/commentform.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.listing_id = self.kwargs['pk']
        send_random_email("thohrnikk11@gmail.com")
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
            participants = User.objects.filter(
                bid_user__listing=listing).exclude(pk=bid_winner.bidder.pk)
            winner = Winner.objects.create(
                winner=bid_winner.bidder, win_item=listing)
            winner.save()
            send_winner_email(winner)
            send_participants_email(
                participants, winner, bid_winner.bid_amount)
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


# class MyWinners(ListView):
#     model = Winner
#     template_name = 'auctions/my_winners.html'
#     context_object_name = 'winners'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['winners'] = context['winners'].filter(
#             winner=self.request.user)
#         return context
def MyWinners(request):
    listings = Listing.objects.filter(user=request.user)
    context = {
        'listings': listings
    }
    return render(request, 'auctions/my_winners.html', context)


def MyBids(request):
    user_bids = Bid.objects.filter(bidder=request.user)

    listings = []
    for bid in user_bids:
        if bid.listing not in listings:
            listings.append(bid.listing)

    context = {
        'listings': listings,
        'user_bids': user_bids
    }
    return render(request, 'auctions/my_bids.html', context)


def MyWins(request):
    user_wins = Winner.objects.filter(winner=request.user)

    context = {
        'user_wins': user_wins
    }
    return render(request, 'auctions/my_wins.html', context)
