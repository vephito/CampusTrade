
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.list import ListView
from auctions.models import *
from adminpanel.forms import EditForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.views import LogoutView

# Create your views here.


def admin_login(request):
    try:
        # if request.user.is_authenticated:
        #   return redirect('dashboard')
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.info(request, 'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user_obj = authenticate(username=username, password=password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('dashboard')

            messages.info(request, ' Invalid password')
            return redirect('ad_login')
        return render(request, 'admin/ad_login.html')

    except Exception as e:
        print(e)


def dashboard(request):
    # recent_actions_value = recent_actions(request)
    # return render(request, 'admin/dashboard.html')
    # return render(request, 'admin/dashboard.html', {'recent_actions_value': recent_actions_value})
    log_entries = LogEntry.objects.all().order_by('-action_time')[:10]

    # Get a list of content types for the log entries
    content_type_ids = [log_entry.content_type_id for log_entry in log_entries]
    content_types = ContentType.objects.filter(id__in=content_type_ids)

    return render(request, 'admin/dashboard.html', {'log_entries': log_entries, 'content_types': content_types})


class Listings(ListView):
    model = Listing
    template_name = 'admin/listing.html'
    context_object_name = 'listings'
    paginate_by = 20
    ordering = ['-date_created']


class DeleteListing(DeleteView):
    model = Listing
    context_object_name = 'listings'
    success_url = reverse_lazy('listingadmin')
    template_name = 'admin/listing_confirm_delete.html'


class EditListing(UpdateView):
    model = Listing
    form_class = EditForm
    template_name = 'admin/edit.html'
    success_url = reverse_lazy('listingadmin')


class CommentsListing(ListView):
    model = Listing

    template_name = 'admin/comments_listing.html'
    context_object_name = 'listings'
    paginate_by = 9
    ordering = ['-date_created']


class Comments(ListView):
    model = Comment
    context_object_name = 'comments'

    template_name = 'admin/comments.html'
    paginate_by = 9

    def get_queryset(self):
        listing = Listing.objects.get(pk=self.kwargs['pk'])
        return Comment.objects.filter(listing=listing).order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(pk=self.kwargs['pk'])
        return context


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['user', 'listing', 'text']
    template_name = 'admin/comment_update_form.html'
    success_url = reverse_lazy('listingcomments')

    def get_success_url(self):
        return reverse_lazy('listingcomments', kwargs={'pk': self.kwargs['listing_pk']})


class DeleteComment(DeleteView):
    model = Comment
    context_object_name = 'comment'

    success_url = reverse_lazy('listingcomments')
    template_name = 'admin/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('listingcomments', kwargs={'pk': self.kwargs['listing_pk']})

#  USER

# display all user


def user_admin(request):
    users = User.objects.all()
    return render(request, 'admin/user_admin.html', {'users': users})

# Edit user info


def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = UserChangeForm(instance=user)

    return render(request, 'admin/user_edit.html', {'form': form})

# Delete user


def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('user_admin')
    # return render(request, 'admin/user_delete.html', {'user': user})

# Recent log Entries


def recent_actions(request):
    log_entries = LogEntry.objects.all().order_by('-action_time')[:10]

    # Get a list of content types for the log entries
    content_type_ids = [log_entry.content_type_id for log_entry in log_entries]
    content_types = ContentType.objects.filter(id__in=content_type_ids)

    return render(request, 'admin/recent_actions.html', {'log_entries': log_entries, 'content_types': content_types})


class CategoryListing(ListView):
    model = Category

    template_name = 'admin/category_listing.html'
    context_object_name = 'categories'
    paginate_by = 9


class CategoryUpdate(UpdateView):
    model = Category
    fields = ['title']
    template_name = 'admin/category_update_form.html'
    success_url = reverse_lazy('admin_category')


class CreateCategory(CreateView):
    model = Category
    fields = ['title']
    template_name = 'admin/create_category.html'
    success_url = reverse_lazy('admin_category')


def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    return redirect('admin_category')


class WinnerListing(ListView):
    model = Winner
    template_name = 'admin/winner_listing.html'
    context_object_name = 'winners'
    paginate_by = 9


class CreateWinner(CreateView):
    model = Winner
    fields = ['winner', 'win_item']
    template_name = 'admin/create_winner.html'
    success_url = reverse_lazy('winner_listing')

    def form_valid(self, form):
        response = super().form_valid(form)
        win_item = form.cleaned_data.get('win_item')
        win_item.sold = True
        win_item.save()
        return response


class BidListing(ListView):
    model = Listing
    template_name = 'admin/bid_listing.html'
    context_object_name = 'listings'
    ordering = '-date_created'
    # paginate_by = 9


class BidList(ListView):
    model = Bid
    template_name = 'admin/bid_list.html'
    context_object_name = 'bids'
    # paginate_by = 9

    def get_queryset(self):
        listing = Listing.objects.get(pk=self.kwargs['pk'])
        return Bid.objects.filter(listing=listing).order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listing'] = Listing.objects.get(pk=self.kwargs['pk'])

        return context


class BidEdit(UpdateView):
    model = Bid
    fields = ['bidder', 'bid_amount']
    template_name = 'admin/bid_update_form.html'
    success_url = reverse_lazy('bid_list')

    def get_success_url(self):
        return reverse_lazy('bid_list', kwargs={'pk': self.kwargs['listing_pk']})


class BidDelete(DeleteView):
    model = Bid
    context_object_name = 'bid'

    success_url = reverse_lazy('bid_list')
    template_name = 'admin/bid_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('bid_list', kwargs={'pk': self.kwargs['listing_pk']})


class CustomLogoutView(LogoutView):
    pass
