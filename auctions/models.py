from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class User(AbstractUser):
    create_auction = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Category name: {self.name}"

class Bid(models.Model):
    amount = models.DecimalField(max_digits = 10, decimal_places=2)
    bidder = models.ForeignKey(User,on_delete = models.CASCADE,null = True,blank = True, related_name = 'bid_sets')

class Comment(models.Model):
    comment_text = models.TextField()
    commenter = models.ForeignKey(User,on_delete = models.CASCADE,null = True, blank = True)  
    timestamp = models.DateTimeField(default=timezone.now)

class AuctionItem(models.Model):
    title = models.CharField(max_length= 50)
    img_url = models.CharField(max_length = 512)
    description = models.TextField()
    listing_date = models.DateField(auto_now_add = True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    categories = models.ManyToManyField(Category)
    creator = models.ForeignKey(User,on_delete = models.CASCADE, related_name = "items")
    current_bids = models.ManyToManyField(Bid,related_name='current_bid',blank=True)
    comments = models.ManyToManyField(Comment,related_name='all_comments',blank=True)
    
    def __str__(self):
        return self.title

    def get_current_bids(self):
        return self.current_bids.all().order_by("-amount")
    
    def formatted_listing_date(self):
        return self.listing_date.strftime("%d-%m-%y")
    
    def get_category(self):
        return f"{self.title} is in: {self.categories}"
    

class Winner(models.Model):
    winner = models.ForeignKey(User, on_delete = models.CASCADE,related_name='winners',null = True, blank = True)
    win_item = models.ForeignKey(AuctionItem,related_name="win_items",null = True,blank =True ,on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.id}, {self.winner} , {self.win_item}"
    
    def get_winner(self):
        return self.winner
    
    def get_win_item(self):
        return self.win_item


class WatchList(models.Model):
    watcher = models.OneToOneField(User,on_delete=models.CASCADE,related_name="watching")
    item_list = models.ManyToManyField(AuctionItem,related_name="item_list")
    

