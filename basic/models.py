from django.db import models
from django.contrib.auth.models import User
from .STATE_CHOICES import STATE_CHOICES
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save, pre_delete,pre_save
from django.dispatch import receiver

import math
WEIGHT_CHOICES = (
    ('200 gm' , '200 gm'),
    ('255 gm' , '255 gm'),
    ('160 gm','160 gm'),
    ('260 gm' , '260 gm'),
    ('1 kg' , '1 kg'),
    ('2 kg' , '2 kg'),
    ('3 kg' , '3 kg'),
    ('60 Capsules' , '60 Capsules'),
    ('L' , 'L'),
    ('XL' , 'XL'),
)
SERVING_CHOICES = (
    ('30','30'),
    ('40','40'),
    ('60','60'),
    ('20/40','20/40'),
    ('30/60','30/60'),
)
CATEGORY_CHOICES = (
    ('Preworkout','Preworkout'),
    ('Intraworkout','Intraworkout'),
    ('Protein','Protein'),
    ('Gainer','Gainer'),
    ('Other','Other')
)
class Flavor(models.Model):
    name = models.CharField(max_length=1000)
    def __str__(self):
        return self.name
class Description(models.Model):
    text = models.CharField(max_length=1000)
    def __str__(self):
        return self.text

class Item(models.Model):
    name = models.CharField(max_length=1000)
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=1000 , choices=CATEGORY_CHOICES ,null=True , blank=True)
    qty = models.CharField(max_length=1000, choices=WEIGHT_CHOICES, null=True , blank=True )
    flavour = models.ForeignKey(Flavor , on_delete=models.CASCADE, null=True , blank=True)
    img1 = models.ImageField(null=True, blank=True)
    img2 = models.ImageField(null=True, blank=True)
    img3 = models.ImageField(null=True, blank=True)
    img4 = models.ImageField(null=True, blank=True)
    img5 = models.ImageField(null=True, blank=True)
    img6 = models.ImageField(null=True, blank=True)
    servings = models.CharField(max_length=100, null=True, blank=True , choices=SERVING_CHOICES)
    instock = models.BooleanField(default=False)
    desc = models.ForeignKey(Description , on_delete=models.CASCADE, null=True , blank=True)
    thumbnail = models.ImageField(null=True, blank=True)
    display = models.BooleanField(default=True)
    percent = models.PositiveIntegerField(default=30, validators=[MaxValueValidator(99)])

    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)], null=True, blank=True)
    afterPrice = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        if self.flavour:
            return self.name +' -- '+ self.flavour.name + ' -- ' +self.qty
        else:
            return self.name


class OrderItem(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    item = models.ForeignKey(Item , on_delete=models.CASCADE , related_name='item')
    qty = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.item.name + '    '  + str(self.qty) + ' ' +str(self.ordered) )
    def get_total(self):
        return self.item.afterPrice * self.qty

class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    final_amount = models.IntegerField(default=0)
    items = models.ManyToManyField(OrderItem)
    billing_address = models.ForeignKey('Billing_Address' , null=True, blank=True, on_delete=models.CASCADE)
    razorpay_id = models.CharField(max_length=100000000, null=True, blank=True)
    payment_id = models.CharField(max_length=10000000 , null=True, blank=True)
    signature = models.CharField(max_length=1000000000000 , null=True , blank=True)
    coupon_bool = models.BooleanField(default=False)
    coupon  = models.ForeignKey('Coupons' ,null=True, blank=True,  on_delete=models.SET_NULL)
    def __str__(self):
        return self.user.username

    def get_total_amount(self):
        total = 0
        for i in self.items.all():
            total += i.get_total()

        return total

class Coupons(models.Model):
    tag = models.CharField(max_length=1000, unique=True)
    amount = models.IntegerField(default=0)

    order_items = models.ManyToManyField(Order)
    def __str__(self):
        return self.tag
class Billing_Address(models.Model):
    name=models.CharField(max_length=1000 , null=True, blank=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    home = models.CharField(max_length=10000)
    phone = models.CharField(max_length=10 , null=True , blank=True)
    state = models.CharField(max_length=10 , choices=STATE_CHOICES)
    email = models.EmailField(max_length=1000 , null=True, blank=True)

    def __str__(self):
        return self.home
GENDER_CHOICES = (
    ('Male','Male'),
    ('Female','Female'),
)
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.ManyToManyField(Billing_Address , blank=True)
    email = models.EmailField(max_length=100 , blank=True , null=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True , blank=True)

    def __str__(self):
        return self.user.username

class Reviews(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    text = models.CharField(max_length=10000)
    rating = models.PositiveIntegerField( validators=[MaxValueValidator(5)])
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True , blank=True)
    def __str__(self):
        return self.user.username

class Wishlist(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=10000)
    content = models.TextField()
    img = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.author.username+ ' ---- '+ self.title)

class Enquiry(models.Model):
    name = models.CharField(max_length=1000)
    phone = models.CharField(max_length=10)
    message = models.TextField(blank=True , null=True)
    date = models.DateField(auto_now_add=True , null=True, blank=True)
    status  = models.BooleanField(default=False)
    def __str__(self):
        return self.name



@receiver(post_save, sender= Reviews)
def update_score(sender,created, instance, **kwargs):
    if created:
        obj = Item.objects.get(id=instance.item.id)
        reviews = Reviews.objects.filter(item=obj)
        total =0
        for i in reviews:
            total += i.rating
        rating = math.ceil(total/reviews.count())
        obj.rating = rating
        obj.save()


@receiver(post_save , sender=Item)
def update_price(sender , created , instance , **kwargs):

    percent = instance.percent
    beforeprice = instance.price - (instance.price * (percent/100))
    Item.objects.filter(id=instance.id).update(afterPrice = beforeprice)


@receiver(pre_delete ,sender = Coupons )
def update_bool(sender  , instance ,**kwargs):
    for i in instance.order_items.all():
        i.coupon_bool = False
        i.save()