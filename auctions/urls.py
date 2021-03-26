from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist_add/<int:listing_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:listing_id>", views.watchlist_remove, name="watchlist_remove"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("bid_close/<int:listing_id>", views.bid_close, name="bid_close"),
    path("comments/<int:listing_id>", views.comments, name="comments"),
    path("categories", views.categories, name="categories")
]

# this scripy allows us to use media from local disk

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                    document_root=settings.MEDIA_ROOT)
