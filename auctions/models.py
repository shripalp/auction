from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    FOOD= 'Food'
    HOME= 'Home'
    ACTIVITIES= 'Activities'
    SERVICES= 'Services'
    RECREATION= 'Recreation'
    TRAVEL= 'Travel'
    MISC= 'Miscellenius'
    item_categories = [
        (FOOD, 'Food'),
        (HOME, 'Home'),
        (ACTIVITIES, 'Activities'),
        (SERVICES, 'Services'),
        (RECREATION, 'Recreation'),
        (TRAVEL, 'Travel'),
        (MISC, 'Miscellenius')
    ]
    ACTIVE= 'AC'
    INACTIVE= 'NA'

    status_categories = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Not Active')
    ]

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=300)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now=True)
    category = models.CharField(choices=item_categories, default=HOME, max_length=30)
    image = models.ImageField(upload_to="media", blank=True)
    url = models.URLField(max_length=500, blank=True)
    status = models.CharField(choices=status_categories, default=ACTIVE, max_length=2)

    def is_active(self):
        return self.status == self.ACTIVE
    
    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):

    OPEN = "ON"
    CLOSED = "CL"
    status_categories = [
        (CLOSED, 'Closed'),
        (OPEN, 'Open')
    ]
    bid_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    bid_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid_status = models.CharField(choices=status_categories, default=OPEN, max_length=2)
    bid_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.bid_item}: bid_price:{self.bid_price}"
    
    def is_open(self):
        return self.bid_status == self.OPEN
 

class Comment(models.Model):
    comments_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comments_on = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comments = models.TextField(max_length=500, blank=True)
    commented_on = models.DateTimeField(auto_now=True)

class Watchlist(models.Model):
    watched_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="watchlists")
    watched_item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="watchlists")

