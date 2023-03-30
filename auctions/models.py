from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=24)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"  # admin page name


class Listing(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=60, default=None)
    image = models.ImageField(
        upload_to="images/", blank=True, null=True)
    price = models.IntegerField(default=0)
    description = models.TextField()
    sold = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)


class Bid(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bid_user")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bid_listing")
    bid_amount = models.IntegerField(default=0)
    bid_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)


class Winner(models.Model):
    winner = models.ForeignKey(User, on_delete=models.CASCADE)
    win_item = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watch_items")
    # date_added = models.DateTimeField(auto_now_add=True)
    total_items = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['items']

    def __str__(self):
        return f"{self.user.username}'s watchlist for {self.items.title}"

# class Category(models.Model):
#     category = models.CharField(max_length=24, blank=True, null=True)


# class Listing(models.Model):
#     title = models.CharField(max_length=64, default="None")
#     description = models.TextField(default="None")
#     price = models.IntegerField(default=0)
#     image = models.ImageField(blank=True, null=True, max_length=500,
#                               default="https://images.unsplash.com/photo-1613140952277-1c6bd0386ff5?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=2734&q=80")
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="owner")
#     category = models.ForeignKey(
#         'Category', on_delete=models.CASCADE, related_name="listing_category")

#     def __str__(self):
#         return f"{self.title} {self.user}"


# class Bid(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
#     bid = models.IntegerField()

#     def __str__(self):
#         return f'bid on item: {self.listing} by {self.user} with the price of ${self.bid}'


# class Watchlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.user} added a watchlist on the item {self.listing}"


# class Comments(models.Model):
#     user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
#     listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)
#     comments = models.TextField(null=True)

#     def __str__(self):
#         return f"{self.comments} {self.user} {self.listing}"


# class Winner(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.user} is the winner of the product {self.listing}"
