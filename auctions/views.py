from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea
from .models import *


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'category', 'url']
        widgets = {
            'description':Textarea(attrs={'cols':60, 'rows':2}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['title'].widget.attrs['style'] = 'width:400px; height:40px;'
        self.fields['description'].widget.attrs['style'] = 'width:600px; height:160px;'
        self.fields['starting_bid'].widget.attrs['style'] = 'width:100px; height:40px;'
        self.fields['category'].widget.attrs['style'] = 'width:200px; height:40px;'
        self.fields['url'].widget.attrs['style'] = 'width:1000px; height:40px;'

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_price']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['bid_price'].widget.attrs['style'] = 'width:100px; height:40px;'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comments"]
        widgets = {
            'comments': Textarea(attrs={'cols':120, 'rows':5}),
        }
        
    



def index(request):
    """
        renders all the active listings
    """
    return render(request, "auctions/index.html", {
        "listings":Listing.objects.all().filter(status='AC'), "BASE_DIR":"image"
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

    
    

@login_required
def create(request):
    """     
        Creat a new listing here 
    """

    if request.method == "POST":
    #validate the form, save data to database and render active listing page, request.FILES is for media stored on local disk
        form=ListingForm(request.POST, request.FILES)
    
        if form.is_valid():
            obj = Listing()
            obj.created_by=request.user
            obj.title=form.cleaned_data['title']
            obj.description=form.cleaned_data['description']
            obj.starting_bid=form.cleaned_data['starting_bid']
            obj.category=form.cleaned_data['category']
            #obj.image=form.cleaned_data['image']
            obj.url=form.data['url']
            obj.save()
            
            return HttpResponseRedirect(reverse("auctions:index"))
        

    # if request method is get render empty form
    form = ListingForm()
    return render(request, "auctions/create.html", {
        "form":form
    })


def listing(request, listing_id):
    """     
        display a selected listing and allow to bid 
    """
    bid_form = BidForm()
    comment_form = CommentForm()
    if Bid.objects.filter(bid_item=listing_id):
        bid_count = Bid.objects.filter(bid_item=listing_id).count()
        obj = Bid.objects.filter(bid_item=listing_id)
        current_bid = obj.order_by('-bid_price').first()
       
    else:
        current_bid ="none"
        bid_count = "No"

    if Watchlist.objects.filter(watched_item=listing_id, watched_by=request.user.id):
        watched = Watchlist.objects.get(watched_item=listing_id, watched_by=request.user.id)
    else: 
        watched = "Not on your watchlist yet!!"

    if Comment.objects.filter(comments_on=listing_id):
        comments = Comment.objects.filter(comments_on=listing_id)
    else:
        comments = None
    
    
    return render(request, "auctions/listing.html", {
        "listing":Listing.objects.get(pk=listing_id),
        "watched": watched,
        "bid_form":bid_form,
        "comment_form":comment_form,
        "user_name":request.user.username,
        "comments":comments,
        "bid_count":bid_count,
        "current_bid":current_bid
    })




@login_required
def watchlist(request):
    """
        render all the items watched by a user
    """
    return render(request, "auctions/watchlist.html",{
        "watchlists": Watchlist.objects.filter(watched_by=request.user.id)      
    })



@login_required
def watchlist_add(request, listing_id):
    """     
        Allows user to add item to watchlist

    """

    #add item to the watchlist table
    
    obj = Watchlist()
    obj.watched_item = Listing.objects.get(pk=listing_id)
    obj.watched_by = User.objects.get(pk=request.user.id)
    obj.save()
        
    return HttpResponseRedirect(reverse("auctions:watchlist"))
    

@login_required
def watchlist_remove(request, listing_id):
    """     
        allows user to remove item from watchlist

    """

    #add item to the watchlist table
    
    Watchlist.objects.filter(watched_item=listing_id).delete()
    return HttpResponseRedirect(reverse("auctions:watchlist"))
        
   





@login_required
def categories(request):
    """     
        display list of all categories 
    """
    if request.method == "POST":
        cat = request.POST["cat"]
        listings = Listing.objects.filter(category = cat, status="AC")
        message = "No active listing in this category"
        
        
    else:
        message = "Select category from drop down box"
        listings = None

    categories = [
        'Food',
        'Home',
        'Activities',
        'Services',
        'Recreation',
        'Travel',
        'Miscellenius'
    ]
    return render(request, "auctions/categories.html", {
        "categories": categories,
        "listings":listings,
        #"BASE_DIR":"image",
        "message":message
        
    })


@login_required
def bid(request, listing_id):
    """
        Allows user to place bid
    """

    if request.method == "POST":
    
        form=BidForm(request.POST)
    
        if form.is_valid():
            bid = form.cleaned_data['bid_price']
            listing= Listing.objects.get(pk=listing_id)
           
            if bid > listing.starting_bid:
                
                obj = Bid()
                obj.bid_price= bid
                obj.bidder= User.objects.get(pk=request.user.id)
                obj.bid_item = Listing.objects.get(pk=listing_id)
                obj.bid_status = "ON"
                obj.save()
                return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))

            else:
                return render(request, "auctions/error.html", {
                    "message": "Your bid is lower than starting bid price"
                })

@login_required
def bid_close(request, listing_id):
    """
        Allows user to close the bid
    """
    #Close the bid and announce the winner
    obj = Bid.objects.filter(bid_item=listing_id)
    if obj:
        current_bid = obj.order_by('-bid_price').first()
        
        current_bid.bid_status = "CL"
        current_bid.save()

        obj = Listing.objects.get(pk=listing_id)
        obj.status = "NA"
        obj.save()
        return HttpResponseRedirect(reverse("auctions:index"))

    return render(request, "auctions/error.html",{
                            "message":"Cannot close, no bid yet!!"
                        })
    
            
        

@login_required
def comments(request, listing_id):
    """
        Allows user to post comments
    """

    if request.method == "POST":
    #validate the form, save data to database and render active listing page
        form=CommentForm(request.POST)
    
        if form.is_valid():
            obj = Comment()
            obj.comments_by= User.objects.get(pk=request.user.id)
            obj.comments= form.cleaned_data['comments']
            obj.comments_on = Listing.objects.get(pk=listing_id)
        
            obj.save()
            
            return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))



