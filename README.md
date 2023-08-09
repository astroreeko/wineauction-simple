#Django wineauction-simple
Simple Django Wine Auction Site - 


## Version dependencies:
            
Python3  3.9.2  
Django 4.2.4
openjdk version "11.0.18" 2023-01-17



### Database Structure

AuctionItem
    - AuctionItem_id_random (PK)
    - ProductName
    - ProductCNname
    - Description
    - Quantity
    - Estimate value
    - Reserve
    - Current_Highest_bid
    - Current_Highest_bidder (FK) -> WineMembers
    - Provenience
    - Other_info e.g conditional report
    - AuctionItem_imgs
    - Status e.g Finished or Ongoing

WineMembers
    - WineMember_id_random (PK)
    - Wine_mb_name
    - Password
    - Email
    - Wechat
    - Mobile
    - About_me
    - member_Int_msg


BidHistory
    - Bid_id_random (PK) 
    - Auction_id_random (FK) -> Auctions
    - Wine_mb_name (FK) -> WineMembers
    - AuctionItem_id_random (FK) -> AuctionItem
    - Price

SuccessfulOrder
    - WonOrders_id_random (PK)
    - WineMember_random (FK) -> WineMembers
    - AuctionItem_id_random (FK) -> AuctionItem
    - Quantity
    - Buyers_Premium
    - Final_price
    - Order_Status
    - Internal_msg


