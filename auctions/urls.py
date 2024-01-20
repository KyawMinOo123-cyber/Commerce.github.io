from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create-auction',views.create_auction, name='create-auction'),
    path('<int:auction_id>/item-info',views.item_info,name = "item-info"),
    path('<int:auction_id>/add-comment',views.add_comment,name="add-comment"),
    path('<int:auction_id>/place-bid',views.place_bid,name="place-bid"),
    path('<int:auction_id>/close-auction',views.close_auction,name="close-auction"),
    path('<int:auction_id>/delete_auction',views.delete_auction,name="delete-auction"),
    path('<int:auction_id>/watch_list',views.watch,name="watch"),
    path('watched_items',views.watched_items,name = "watched-items"),
    path('<int:auction_id>/remove',views.remove_item,name="remove"),
    path('category_list',views.category_list,name="category-list"),
    path('<int:category_id>/category_item',views.category_item,name="category-item"),
    path('new_category',views.new_category,name="new-category"),
    path('admin/', admin.site.urls, name='admin')
]
