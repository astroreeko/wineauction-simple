from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Bid Function - this determines what is bid increments

def bidFunction(reserve):
    
    if reserve <= 100:
        return 2
    elif reserve <= 300:
        return 5
    elif reserve <= 1000:
        return 10
    else:
        return 20


# Customer User Manager for admin page

class CustomAccountManager(BaseUserManager):
    
    def create_user(self, memberId, memberUsername, email, wechat, mobile, fullname, 
                    aboutMe, password, **other_fields):
    
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_active', True)

        if not wechat:
            raise ValueError(_("请输入微信账号... 方便发货联系你"))

        if not fullname:
            raise ValueError(_("请输入你的名字"))

        user = self.model(memberId = memberId, memberUsername = memberUsername, 
                          email = email, wechat = wechat, mobile = mobile,
                          fullname=fullname, aboutMe = aboutMe, **other_fields )

        user.set_password(password)
        user.save()
        return user
    
    
    def create_superuser(self, memberId, memberUsername, email, wechat, mobile, fullname, 
                         aboutMe, password, **other_fields):
    
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        # other_fields.setdefault('is_admin', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(memberId, memberUsername, email, wechat, mobile,
                                fullname, aboutMe, password, **other_fields)



# Create your models here.

# Date Structure Definition

class AuctionItem(models.Model):
    auctionItem_id_random = models.UUIDField(
        primary_key=True, 
        default=ShortUUIDField(
            length=16, 
            max_length=40, prefix="aid_", 
            alphabet="abcdefg1234"
        ), 
        max_length=50, 
        on_delete=models.DO_NOTHING,
        editable=False
    )
    productName = models.CharField(max_length=200, blank=False)
    productCNname = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(max_length=6, blank=False)   
    estimateValue = models.IntegerField(max_length=12, blank=False)
    reserve = models.IntegerField(max_length=12, blank=False)
    current_highestBidPrice = models.IntegerField(max_length=12, blank=True)
    current_highestBidder = models.CharField(max_length=40, blank=True)
    current_highestBidderMaxBidPrice = models.IntegerField(max_length=12, blank=True)
    bidIncrement = models.IntegerField(max_length=10, default=bidFunction(reserve))
    # Provenience - not implemented in this version
    otherInfo = models.TextField(blank=True)
    auctionItem_imgs = models.ImageField(
        upload_to=None, 
        height_field=None, 
        width_field=None, 
        max_length=100
    )
    status = models.BooleanField(default=True)  # if auction is ongoing (True) or Finished (False) 
    
    def __str__(self):
        return self.productName


class WineMembers(AbstractBaseUser, PermissionsMixin):

    memberUsername = models.CharField(primary_key=True, max_length=40, unique=True)
    email = models.CharField(_('电子邮箱'), max_length=100)
    wechat = models.CharField(_('微信号'), max_length=80)
    mobile = models.CharField(_('手机号'), max_length=50)
    fullname = models.CharField(_('名字'), max_length=80)
    aboutMe = models.CharField(_('个性签名'), max_length=50)
    start_date = models.DateTimeField(default=timezone.now)
    internalMsg = models.TextField(_('内部留言'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    
class BidHistory(models.Model):
    bid_id_random = models.UUIDField(
        primary_key=True, 
        default=ShortUUIDField(
            length=24, 
            max_length=40, prefix="bid_", 
            alphabet="abcdefg1234"
        ), 
        max_length=50, 
        on_delete=models.DO_NOTHING,
        editable=False
    )  
    auctionItem_id_random = models.ForeignKey(AuctionItem, on_delete=models.DO_NOTHING)
    memberUsername = models.ForeignKey(WineMembers, on_delete=models.DO_NOTHING)
    maxBidPrice = models.IntegerField(max_length=12)
    


class SuccessfulOrder(models.Model):
    wonOrder_id_random = models.UUIDField(
        primary_key=True, 
        default=ShortUUIDField(
            length=16, 
            max_length=40, prefix="won_", 
            alphabet="abcdefg1234"
        ),
        max_length=50, 
        on_delete=models.DO_NOTHING,
        editable=False
    )
    memberUsername = models.ForeignKey(WineMembers, on_delete=models.DO_NOTHING)
    #buyersPremium = models.IntegerField(max_length=6)
    
    orderStatus = models.CharField(max_length=50)
    logisticData = models.CharField(max_length=150)
    internalMsg = models.TextField(blank=True)
    totalOrderPrice = models.IntegerField(max_length=12)  
    
class SuccessfulOrderItems(models.Model):
    wonOrder_id_random = models.ForeignKey(SuccessfulOrder, on_delete=models.DO_NOTHING)
    itemNo = models.IntegerField(max_length=12)
    productName = models.CharField(max_length=200)
    productCNname = models.CharField(max_length=100)
    price = models.IntegerField(max_length=12)
    quantity = models.IntegerField(max_length=6)   
    totalPrice = models.IntegerField(max_length=12)
    buyersPremium = models.IntegerField(max_length=12)
    itemTotal = models.IntegerField(max_length=12)
      
            
# class OnlineJob(models.Model):
#     jbCode = models.CharField(primary_key=True, max_length=50)
#     user_name = models.ForeignKey(NewUser, on_delete=models.DO_NOTHING)
#     redUsername = models.CharField(max_length=100)
#     jbKeyword1 = models.CharField(max_length=30)
#     jbKeyword2 = models.CharField(max_length=30)
#     jbLike = models.CharField(max_length=10)
#     jbSave = models.CharField(max_length=10)
#     jbComment = models.CharField(max_length=10)
#     jbRequestAmt = models.IntegerField(default=10)    #Amt required by users to be done by other users
#     jbDoneAmt = models.IntegerField(default=0) # Amt of times jb wad done by other users
#     jbDLAmt = models.IntegerField(default=0)   # Amt of times jb was downloaded to other users
#     jbOnloadDate = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="上传时间" ) # auto generate data time field
#     jbActive = models.BooleanField(default=True)  # job active or not
    
#     def __str__(self):
#         return self.jbCode
    
    