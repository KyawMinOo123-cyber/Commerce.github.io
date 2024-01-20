createsuperuser (or) use current admin : username: kyaw , pw: k123

# 1: Visitors (users without register or login)
- can only view the default item lists page and category.
- clicking on a category will let the user see current items that are in associated category
- clicking on an item will take user to item info page
- will see item details including current bids and comments
- but unable to place bid or add comments

#2: Logged in users
- can create auction item
- can create category
- can place bid
- can add comments
- can add watch list and remove

#3: Admin
- Admin user will see additional "Admin" button at the navigations
- clicking on it will take user to django admin interface
- can do everything to users,categories,comments,bids,watchList ...
- also have same abilities as loged in users at the website


- item creators can close the auction
- if item winner(who place the max-bid) click on closed item will get a message about their winning
- when item winner click "get the product" button , that item will be removed

- item is created but if no ones place bids on it will restrict the creator from closing the item
- items having at least one bidder can be closed by the creator
