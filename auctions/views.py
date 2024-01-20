from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *

from .create import Create_Form,AuctionItem

from .models import User


def index(request):
    items = AuctionItem.objects.all()
    user = request.user
    if user.is_authenticated:
        if  WatchList.objects.filter(watcher = user).exists():
            watchedItems = user.watching.item_list.all()
            ids = [item.id for item in items]
            watchedIds = [item.id for item in watchedItems]

            
            for watchedId in watchedIds:
                if watchedId not in ids:
                    return render(request,"auctions/index.html",{
                        'items':items,
                    })
                else:
                    return render(request,'auctions/index.html',{
                        'watchedIds':watchedIds,
                        "items":items 
                    })
        # for item creators, button need to be "closed" and disabled for closed items
        if Winner.objects.all():
            win_items_list = Winner.objects.values_list('win_item__title', flat=True)
            item_list = list(win_items_list)
        
            return render(request, "auctions/index.html",{
                'items' : items,
                'winItems':item_list,
            })
    return render(request,'auctions/index.html',{
        'items':items
    })
    


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Check if authentication successful
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
            newuser = User.objects.create_user(username, email, password)
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, newuser)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def item_info(request,auction_id):
    item = AuctionItem.objects.get(pk = auction_id)
    #for logged in users
    if request.user.is_authenticated:
        #if logged in user is not an owner
        if request.user != item.creator:
            #if current user having some winning conditions
            if Winner.objects.filter(winner = request.user).exists():
                #if current item is win_item
                if Winner.objects.filter(win_item = item):
                    winnerObject = Winner.objects.get(win_item = item)
                    if winnerObject:
                        if winnerObject.winner == request.user:
                            return render(request,"auctions/item-info.html",{
                                "item":item,
                                "won_item":f"Congrulation! You have won {item.title}"
                            })
        #for item owners
        else:
            return render(request,'auctions/item-info.html',{
                'item':item
            })
    #for non-logged in users
    return render(request,'auctions/item-info.html',{
        "item": item
    })


@login_required

def create_auction(request):
    user =request.user
    categories = Category.objects.all()
    if categories:
        if request.method == 'POST':
            form = Create_Form(request.POST)
            if form.is_valid():
                new_title = form.cleaned_data['title']
                new_img = form.cleaned_data['img_url']
                new_description = form.cleaned_data['description']
                new_price = form.cleaned_data['price']
                
                newAuctionItem = AuctionItem(
                    title = new_title,
                    img_url = new_img,
                    description = new_description,
                    price = new_price,
                    creator = user,
                )
                newAuctionItem.save()

                #retrieve the created item from database with id
                newAuctionItem = get_object_or_404(AuctionItem, id=newAuctionItem.id)
                selected_category = Category.objects.get(pk = int(request.POST['category-select']))
                newAuctionItem.categories.add(selected_category)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request,'auctions/create.html',{
                    'message' : "Cannot create an auction item!"
                })
        else:
            form = Create_Form()
            return render(request,'auctions/create.html',{
                'form':form,
                'categories' :categories
            })
    else:
        return render(request,'auctions/create.html',{
            'alert':"Category is empty! Please create at least one category first!"
        })
    
#comment system
def add_comment(request,auction_id):
    item = AuctionItem.objects.get(pk = auction_id)
    if request.method == "POST":
        user = request.user
        text = request.POST['comment']
        comment = Comment.objects.create(comment_text = text,commenter = user)
        item.comments.add(comment)
        return HttpResponseRedirect(reverse("item-info", args=[auction_id]))
    
#bid system
def place_bid(request,auction_id):
    user = request.user
    item = AuctionItem.objects.get(pk = auction_id)
    
    price = int(item.price)
    if request.method == "POST":
        max_bid = item.current_bids.order_by('-amount').first()
        bidAmount = int(request.POST['bid-input'])

        if max_bid is not None: # if there is max_bid already, compare with max-bid amount
            if bidAmount <= max_bid.amount:
                return render(request,'auctions/item-info.html',{
                        "item":item,
                        "message":f"Your need to increase you Bid Amount!"
                    })   
            else:
                placeBid = Bid.objects.create(amount = bidAmount, bidder = user)
                item.current_bids.add(placeBid)
                return render(request,'auctions/item-info.html',{
                    "item":item,
                    "success":f"Congrulation! You've successfully bid this item."
                })
        else: #if its the first bid, compare with original price
            if bidAmount < price:
                return render(request,'auctions/item-info.html',{
                        "item":item,
                        "message":f"Your need to increase you Bid Amount!"
                    })
            else:
                placeBid = Bid.objects.create(amount = bidAmount, bidder = user)
                item.current_bids.add(placeBid)
                return render(request,'auctions/item-info.html',{
                    "item":item,
                    "success":f"Congrulation! You've successfully bid this item."
                }) 
    else:
        return HttpResponseRedirect(reverse('item-info',args=[auction_id]))

#only owners can close the item and max bidder will win the item
def close_auction(request,auction_id):
    items = AuctionItem.objects.all()
    item = AuctionItem.objects.get(pk = auction_id)

    if request.method == "POST":
        # Get the maximum bid of the current item
        max_bid = item.current_bids.order_by('-amount').first()

        if max_bid:
            # Retrieve the bidder who placed the maximum bid
            max_bidder = max_bid.bidder
            if Winner.objects.filter(winner = max_bidder, win_item = item).exists():
                return HttpResponseRedirect(reverse('index'))
            else:
                Winner.objects.create(winner=max_bidder , win_item = item)
                win_items_list = Winner.objects.values_list('win_item__title', flat=True)
                item_list = list(win_items_list)
                return render(request,'auctions/index.html',{
                    "message":f"You have successfully closed the item: {item.title}",
                    "items":items,
                    'winItems':item_list
                })
                

            
        return render(request,'auctions/index.html',{
            "message":f"You have successfully closed the item: {item.title}",
            "items":items
        })
    
#item will be deleted when auction winner get the product
def delete_auction(request,auction_id):
    item = AuctionItem.objects.get(pk = auction_id)
    item.delete()
    return HttpResponseRedirect(reverse('index'))

#watch function
def watch(request,auction_id):
    item = AuctionItem.objects.get(pk = auction_id)
    items = AuctionItem.objects.all()
    user = request.user
    if request.method == "POST":
        watcher_instance, created = WatchList.objects.get_or_create(watcher = user)
        watcher_instance.item_list.add(item)
        if created:
            watcher_instance.item_list.add(item)
        return HttpResponseRedirect(reverse('watched-items'))

    return render(request,'auctions/index.html',{
        'message':f"Watching, {item.title} ...",
        'items':items
    })

#watched item list
def watched_items(request):
    user = request.user
    
    if WatchList.objects.filter(watcher = user):
        itemList = WatchList.objects.get(watcher = user).item_list

        return render(request,'auctions/watchedItems.html',{
            "items":itemList
        })
    else:
        return render(request,'auctions/watchedItems.html',{
            "message": "No Items In Watch List!"
        })
    
#remove watched item
def remove_item(request,auction_id):
    user = request.user
    item = AuctionItem.objects.get(pk = auction_id)
    watcher = WatchList.objects.get(watcher = user)
    watcher.item_list.remove(item)
    return HttpResponseRedirect(reverse("watched-items"))
    
#for category list page
def category_list(request):
    all_categories = Category.objects.all()
    return render(request,'auctions/category.html',{
        "categories":all_categories
    })

#to view items based on category
def category_item(request,category_id):
    category = Category.objects.get(pk = category_id)
    items = AuctionItem.objects.filter(categories = category)
    if items:
        return render(request,'auctions/categoryItems.html',{
            "category":category,
            "items":items
        })
    else:
        return render(request,'auctions/categoryItems.html',{
            "message":f"No auction items in this category"
        })
    
#create new category
def new_category(request):
    if request.method == "POST":
        input = request.POST['newCategory']
        if input:
            if Category.objects.filter(name__iexact=input).exists():
                return render(request,'auctions/category.html',{
                        "error":"Category already exists!",
                        "categories":Category.objects.all()
                    })
            else:
                Category.objects.create(name = input)
                return render(request,'auctions/category.html',{
                    "message": "Category created successfully!",
                    "categories":Category.objects.all()
                })
        else:
            HttpResponseRedirect(reverse('category-list'))