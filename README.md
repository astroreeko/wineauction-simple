#Django wineauction-simple v0.1
Simple Django Wine Auction Site 


## Version dependencies:
            
Python3         3.9.2  
Django          4.1.10
djongo          1.3.6
shortuuid       1.0.11
Pillow          8.1.2

MongoDB


## Special Attention
This software use MongoDB (via djongo 1.3.6) instead of SQL for database storage



### Database Models (MongoDB)

AuctionItem
    - AuctionItem_id_random (PK)
    - ProductName
    - ProductCNname
    - Description
    - Quantity
    - Estimate value
    - Reserve
    - Current_Highest_bid (Accepted Price)
    - Current_Highest_bidder -> WineMembers
    - Current_Highest_bidderMaxPrice (Winning Members's highest bid price for AuctionItem)
    - Bid increment (Refer to bid Function)
    - Provenience (Not implemented in this version)
    - Other_info e.g conditional report
    - AuctionItem_imgs
    - AuctionEndDate
    - Status e.g Finished (False) or Ongoing (True)

WineMembers
    - MemberUsername (PK)
    - Password
    - Email
    - Wechat
    - Mobile
    - About_me
    - InternalMsg 
    - TotalBids (maybe implement)
    - TotalBidValue (maybe implement)


BidHistory
    - Bid_id_random (PK) 
    - AuctionItem_id_random (FK) -> AuctionItem
    - memberUsername (FK) -> WineMembers
    - MaxBidPrice

WonOrder (combine all auction items won on the same day )
    - WonOrders_id_random (PK)
    - WineMember_random (FK) -> WineMembers
    - AuctionItem_id_random (FK) -> AuctionItem
    - Quantity
    - Buyers_Premium
    - Total_price
    - Order_Status
    - Internal_msg

WonOrderItems
    - wonOrder_id_random (FK)
    - itemNo
    - itemName
    - price (unit price)
    - quantity
    - totalPrice (unit price x quantity)
    - buyersPremium (totalPrice x 0.15)
    - itemTotal (totalPrice + buyersPremium)


WineMemberWatchAuctionItems 
(This version will only show last 30 auction Items)
    - Memberusername (FK) > WineMembers
    - AuctionItem_id_random (FK) > AuctionItem


### API Functions

#### Get oneAuctionItem JSON data

 - Send to API product auctionItem_id_random get back AuctionItem JSON Data
 - Available to all users

#### Get allAuctionItem JSON data

 - Send request get back auctionItem JSOn Data
 - Available to all users

#### Get userWatchAuctionListActive
 
 - Send request
    - logged wineMember
 - Return Json Data of current active auction item data, that is watched by wineMember 

#### Get userWatchAuctionListFinished

 - Send request
    - logged wineMember
 - Return Json Data of Finished auction it data, that is watched by wineMember

#### Get userWonList ()

 - Send request
    - logged wineMember
 - Process:  
 - Return Json Data of Won Order for wineMember.


#### Send bid request

 - Available to loggined wineMember
 - Send bid request data
    - WineMember.MemberUsername
    - AuctionItem.AuctionItem_id_random
    - MaxBidPrice
 - API backedn process
    - check user is loggined it
    - check bid price is correct number of correct BidIncrement
        - ( bidPrice - Reserver ) / BidIncrement  = should equal whole number
        If No, reject (reason: incorrect bid Price)
        If Yes,
            - proceed with logic [Event: When WineMember a bid on a AuctionItem]
            - once done, return bidSuccess msg and update user onscreen data


### Bid Function
 
 0-100      RMB     +2
 100-300    RMB     +5
 300-1000   RMB     +10
 1000+      RMB     +20



### Events

#### When WineMember make a bid on a AuctionItem
 - Check Bid price is higher
    if not reject bid
        return Json, "Bid Rejected, price incorrect please check again. "
    if higher
        - Get AuctionItem's current HighestBidder's MaxBid
        - Check if new bid coming from the same wineuser as current HighestBidder
            If Yes
            -  replace current_highest_bidderMaxPrice with new higherPrice
                return Json, "price update success, update local client with new data"
            If No
            - Compare it with new bidder's MaxBid
                If both Max Bid is the same (value)
                    - Change AuctionItem's HighestBid = max Bid
                    - Keep HighestBidder member the same
                If Max Bid has a difference 
                    - Chose member with highest Max Bid price
                    - Set new current_highestestBidPrice = 2nd highest's maxbid price + bidIncrement
                    - Set Current_highestBidder = highest Bidder
                    - Set current_highestBidderMaxBidPrice = highest bidder's max price
                    return Json, "Bid success - You have the winning bid" update local with new data
                
                    Notify losing Bidder, that they have been outbidd use Outbid Event


### Outbid Event
 - send sms / email 
    - productName, productCNname, quantity, current_highestPrice
    - auctionItem_imgs
    - AuctionEndDate
    - Link to make a bid


### Creating WonOrders Batch process - Run everyday at 6.01pm Beijing Time
  - Get list of Auctions that has ended today
    - Set Status to AuctionItems without Current_Highest_bidder to Status to Passed
    - filter keep only AutionItems with a Current_Highest_bidder and sort by ascending 

        - Create WonOrder 
            - create new WonOrder    
                - add new WonOrderItems while wineMember is the same
                    - Send order email to wineMember
                - if wineMember is different, change and create a new WonOrder, cont until end


