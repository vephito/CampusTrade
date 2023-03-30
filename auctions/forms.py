from django import forms
from .models import Bid, Comment, Listing, Category


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']

    def clean_amount(self):
        bidamount = self.cleaned_data['bid_amount']
        listing = self.instance.listing
        last_bid = Bid.objects.filter(
            listing=listing).order_by('id').last()
        if bidamount <= last_bid.bid_amount:
            raise forms.ValidationError(
                'bid_amount', 'Your bid amount must be greater than the current highest bid.')

        return bidamount


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
