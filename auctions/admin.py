from django.contrib import admin
from .models import User, Listing, Bid, Comment, Watchlist

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title","created_by","created_on", "starting_bid", "category", "status")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("watched_by", "watched_item")

class BidAdmin(admin.ModelAdmin):
    list_display = ("bid_item","bid_price","bidder","bid_status","bid_time")

class CommentAdmin(admin.ModelAdmin):
    list_display = ["comments_by", "comments_on", "comments", "commented_on"]



# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
