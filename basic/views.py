from django.shortcuts import get_object_or_404, render , redirect
from django.core.exceptions import ObjectDoesNotExist    
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.mail import send_mail
from proshop.settings import EMAIL_HOST_USER
import random
from .models import CATEGORY_CHOICES
import razorpay
from django.views.decorators.csrf import csrf_exempt



def index(request):
    
    topItems = Item.objects.filter(display=False, instock=True)
    
    dict1 = {}
    l1 = []
    for i in topItems:
        if i.name not in dict1:
            dict1[i.name] = 1 
            l1.append(i)
    
    ran = random.sample(l1, k = 3)
    
    form = EnquiryForm()
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('messageConfirmation')
        
    
    context = {
        'ran':ran,    
        'topItems': topItems,
        
        'form': form,
    }
    return render(request, 'index.html' , context)

def messageConfirmation(request):
    return render(request, 'message_confirmation.html')

    
def item(request , pk):
    item =Item.objects.get(pk=pk)
    items = Item.objects.filter(name=item.name)
    l1 = []

    for i in items:
        l1.append(i) 
    l1.remove(item)
    
    reviews = Reviews.objects.filter(item=item).order_by('date')
    reviewsCount = reviews.count()
    if request.method =='POST':
        review = request.POST.get('review')
        value = request.POST.get('value')
        new = Reviews.objects.create(user=request.user , rating=value , text =review , item=item)
        new.save()
        messages.success(request , 'new review')
        return redirect('item', pk=item.pk )
    context = {
        'item': item,
        'ran':l1,
        'reviews':reviews,
        'count':reviewsCount
    }
    return render(request, 'item.html' , context)



def signin(request):
    if request.method == 'POST':
        phone = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        profile = Profile.objects.filter(phone=phone)
        

        if profile:
            username = profile[0].user.username
            user = authenticate(request , username=username, password=pwd)
            if user is not None:
                login(request , user)
                return redirect('index')
            else:
                messages.error(request , 'Wrong Phone Number or Password ')
                return redirect('signin')
        else:
            messages.warning(request , 'No User record found')
            return redirect('signin')   
              
    return render(request, 'signin.html')

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        phone = request.POST.get('telphone')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')
        


        if User.objects.filter(username = uname).exists():
            messages.error(request, "This username is already taken")
            return redirect('register')
        elif Profile.objects.filter(phone = phone).exists():
            
            messages.success(request, "Unique Phone Number")
        else:
            if pwd1 != pwd2:
                
                messages.warning(request , 'not')
                return redirect('register')
            else:
                user = User.objects.create_user(username=uname ,email="" , password=pwd1 )
                user.save()
                newProfile = Profile.objects.create(user = user , phone = phone)
                newProfile.phone = phone
                
                newProfile.save()
                wishlist = Wishlist.objects.create(user = user)
                wishlist.save()
                login(request, user)

                return redirect('index')
             
               
           
    return render(request , 'register.html')

def logoutPage(request):
    logout(request)
    return redirect('index')

category = ['Preworkout','Intraworkout','Protein','Gainer', 'Other']
def shop(request):
    dict1 = {}
    l1 = []
    
    items = Item.objects.filter(instock=True)
    for i in items:
        if i.name not in dict1:
            dict1[i.name] = 1 
            l1.append(i)
    
    itemCount = len(l1)
    dict2 = {}
    for i in items:
        if i.name in dict2:
            dict2[i.name] +=1 
        else:
            dict2[i.name] = 1 
    
    
    

    
    if request.method == "POST":
        cate  = request.POST.get('category')
        return redirect('shop2', cate)
    keys = list(dict2.keys())  
    main = []
    for i in keys:
        sam= []
        for j in items:
            if i == j.name :
                sam.append(j)  
        main.append(sam)

    params = {
        'allItems':items,
        'items' : l1,
        'count':itemCount,
        'main':main,
        'category': category 
    }
    return render(request , 'shop.html' , params)
def shop2(request,pk):
    dict1 = {}
    l1 = []
    
    items = Item.objects.filter(category=pk, instock=True)
    
    for i in items:
        if i.name not in dict1:
            dict1[i.name] = 1 
            l1.append(i)
    
    itemCount = len(l1)
    dict2 = {}
    for i in items:
        if i.name in dict2:
            dict2[i.name] +=1 
        else:
            dict2[i.name] = 1 
    
    count =0 
    main = []
    keys = list(dict2.keys())  
    main = []
    for i in keys:
        sam= []
        for j in items:
            if i == j.name :
                sam.append(j)  
        main.append(sam)
    
    params = {
        'allItems':items,
        'items' : items,
        'count':itemCount,
        'main':main,
        'category': category ,
        'pk':pk
    }
    return render(request , 'shop2.html', params)
    
def blog(request):
    return render(request , 'blog.html')

def contact(request):
    form = EnquiryForm()
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('messageConfirmation')
    context = {
        'form':form
    }
    return render(request , 'contact.html' , context)

@login_required(login_url='signin')
def addToCart(request , pk):
    item = Item.objects.get(id=pk)
    orderItem,created = OrderItem.objects.get_or_create(user=request.user , ordered=False , item=item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id = item.id).exists():
            orderItem.qty = orderItem.qty + 1
            orderItem.save()
            messages.success(request , 'Qty updated')
            return redirect('cart')
        else:
            order.items.add(orderItem)
            messages.warning(request , 'new item')
            return redirect('cart')
    else:
        time = timezone.now()
        order = Order.objects.create(user=request.user , ordered=False , date=time)
        order.items.add(orderItem)
        
        messages.error(request , 'new order')
        return redirect('cart')

@login_required(login_url='signin')
def addSingleItem(request ,pk):
    item = Item.objects.get(id=pk)
    orderItem,created = OrderItem.objects.get_or_create(user=request.user , ordered=False , item=item)
    order_qs = Order.objects.filter(
        user = request.user , 
        ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id = item.id).exists():
            order_item = OrderItem.objects.filter(
                user = request.user,
                item = item,
                ordered = False
            )[0]
            
            order_item.qty += 1
            order_item.save()
            return redirect('cart')
        else:
            order.items.add(orderItem)
            messages.warning(request , 'new item')
            return redirect('cart')
    else:
        time = timezone.now()
        order = Order.objects.create(user=request.user , ordered=False , date=time)
        order.items.add(orderItem)
        
        messages.error(request , 'new order')
        return redirect('cart')

def removeSingleItem(request , pk):
    item = get_object_or_404(Item , id=pk)
    
    order_qs = Order.objects.filter(
        user = request.user , 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id = item.id).exists():

            order_item = OrderItem.objects.filter(
                user = request.user,
                item = item, 
                 ordered=False
            )[0]
            if order_item.qty >1:
                order_item.qty -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                
                order_item.delete()
                
            
            

            return redirect('cart')
        else:
            return render(request, '404.html')
    else:
        return render(request, '404.html')

def removeItem(request , pk):
    
    item = Item.objects.get(id=pk)
    order_qs = Order.objects.filter(user=request.user , ordered=False )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists():
            orderItem = OrderItem.objects.filter(user = request.user , item = item , ordered=False)[0]
            order.items.remove(orderItem)
            orderItem.delete()
            return redirect('cart')
        else:
            
            return render(request, '404.html')
    else:
        
        return render(request, '404.html')


def cart(request):
    items = Item.objects.all()
    if request.user.is_authenticated is not False:

        try:
            order = Order.objects.get(user=request.user , ordered=False)
            
        except ObjectDoesNotExist:
            order = None
            
            pass
    else:
        order= None
        
    context ={
        'order': order,
        'items':items
    }
    return render(request , 'cart.html' , context)

def aboutus(request):
    x = Item.objects.all()
    items = []
    for i in range(0,len(x)):
        if i <4:
            items.append(x[i])
    

    context = {
        'items': items
    }
    return render(request , 'about.html' , context)

def reorder(request , pk):
    previousOrder = Order.objects.get(id=pk)
    for i in previousOrder.items.all():
        orderItem,created = OrderItem.objects.get_or_create(user=request.user , ordered=False , item = i.item)
        order_qs = Order.objects.filter(user=request.user , ordered=False )
        
        
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__id = i.item.id).exists():
                orderItem.qty = orderItem.qty + i.qty
                orderItem.save()
                
            else:
                orderItem.qty = i.qty
                orderItem.save()
                order.items.add(orderItem)
                
        else:
            date = timezone.now()
            order = Order.objects.create(user=request.user , ordered=False ,date=date )
            order.items.add(orderItem)
            
        



    return redirect('cart')

def order_details(request , pk):
    order = Order.objects.get(id=pk)
    
    params = {'order': order}
    return render(request , 'profile/order-detail.html' ,params)

def checkout(request):
    
    form = CheckoutForm(initial={'state': '1'})
    profile = Profile.objects.get(user=request.user)
    main_address = Billing_Address.objects.filter(user=request.user).last()
    order = Order.objects.get(user = request.user , ordered=False)
    
    if not order.coupon:
        order.final_amount= order.get_total_amount()
    order.save()
    
    if request.method == 'POST':
        try:
            
            form = CheckoutForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                street_address = form.cleaned_data['street_address']
                phone = form.cleaned_data['phone']
                state = form.cleaned_data['state']
                email = form.cleaned_data['email']
                
                if form.cleaned_data['state'] != '--':
                    bill = Billing_Address.objects.create(email=email,name=name, user=request.user , home=street_address , phone=phone , state=state )
               
                    bill.save()
                    
                    if not profile.address.filter(home=bill).exists():
                    
                        profile.phone = phone
                        profile.address.add(bill)
                    
                    order.billing_address = bill
                    
                    
                    order.save()
                    return redirect('payment', pk=bill.id)
                else:
                    messages.error(request , 'Please enter')
                    return redirect('checkout')
                
                
                
                
            else:
                return render(request, '404.html')

        except ObjectDoesNotExist:
            form = None
            order = None
    
        
    context = {
    'form' :form,
    'profile':profile,
    'main_address': main_address,
    'order':order,
    }
    return render(request , 'checkout.html' , context)


client = razorpay.Client(auth=('rzp_live_Wjeh8Li3xOZLVH', 'gLu07fHwYMGB7UDFeINGHIuh'))

def removeCoupon(request,pk):
    order = Order.objects.get(id=pk)
    order.coupon_bool = False
    order.final_amount += order.coupon.amount
    order.coupon = None
    order.save()
    messages.info(request,'Removed')
    return redirect('payment', pk=order.billing_address.id)


def payment(request,pk):
    order = Order.objects.get(user = request.user , ordered=False )
    coupons = list(Coupons.objects.all())
    coupon = [str(x.tag) for x in coupons]
    
    billing_address = Billing_Address.objects.get(id=pk)
    order.billing_address = billing_address
    order.final_amount = order.get_total_amount()
    order.save()
    

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        
        if  not order.coupon_bool:
                
                if coupon_code in coupon:
                    x = Coupons.objects.get(tag = coupon_code)
                    order.final_amount = int(order.final_amount -((x.amount/100)*order.final_amount))
                    order.coupon_bool = True
                    order.coupon = x 
                    
                    x.order_items.add(order)
                    x.save()
                    
                    messages.success(request , 'Hogaya')
                    order.save()
                else:
                    all1 = Coupons.objects.filter(tag = coupon_code)
                    if len(all1)>0:
                        x = all1[0]
                    else:
                        x = None
                    messages.error(request , 'Invalid code')    
        else:
            x = order.coupon
            messages.warning(request, 'Already Applied')
        
    else:
        x =order.coupon
        
    amount = order.final_amount * 100  
    razorpay_order = client.order.create(dict(amount=amount,
                                                       currency='INR',
                                                       payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = 'https://'+ str(get_current_site(request))+ '/paymenthandler'
    
    context  ={
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': 'rzp_live_Wjeh8Li3xOZLVH',
        'razorpay_amount': amount,
        'currency': 'INR',
        'callback_url': callback_url,
        'order':order,
        'billing_address':billing_address,
        'code':x
    }
    
    return render(request , 'stripe.html' , context)

 
@csrf_exempt
def paymenthandler(request):
    order = Order.objects.get(user = request.user , ordered=False )
    amount = order.get_total_amount() * 100 
    # only accept POST request.
    if request.method == "POST":
        try:
            
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            order.razorpay_id = razorpay_order_id
            order.payment_id = payment_id
            order.signature = signature
            
            order.save()
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
  
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            
            if result is None:
                amount = amount  # Rs. 200
                try:
  
                    # capture the payemt
                    client.payment.capture(payment_id, amount)
  
                    # render success page on successful caputre of payment
                    return redirect('success')
                except:
  
                    # if there is an error while capturing payment.
                    return redirect('fail')
            else:
  
                # if signature verification fails.
                return redirect('success')
        except:
  
            # if we don't find the required parameters in POST data
            return HttpResponse('Nothing Happened')
    else:
       # if other than POST request is made.
        return HttpResponse('Nthing')
def usePrevious(request , pk):
    address = Billing_Address.objects.get(id=pk)
    order = Order.objects.get(user = request.user , ordered=False)
    order.billing_address = address
    return redirect('payment' , pk=address.id)




def success(request):
    order = Order.objects.get(user = request.user , ordered=False)
    order.ordered = True
    order.save()

    for i in order.items.all():
        i.ordered = True
        i.save()
    
    
    send_mail(
            'Order Confirmed',
            'Your Order, #'+str(order.id)+' Is Confirmed With Us. For Any Assistance, Call +91-8851661538. Thank You',
            EMAIL_HOST_USER,
            [order.billing_address.email],
            fail_silently=True,
        )
    
    return render(request , 'success.html')
    
def fail(request):
    return HttpResponse('Payment Failure')

def dashboard(request):
    if  request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user , ordered=True).order_by('-date')
        orderCount = orders.count()
        billing_address = Billing_Address.objects.filter(user=request.user).last()
    else:
        orders = None
        orderCount = None
        billing_address= None
    context = {'orders':orders,
    'orderCount':orderCount,
    'billingAddress':billing_address}

    return render(request , 'profile/homepage.html' , context)

def profile(request):
    profile = Profile.objects.get(user=request.user )
    
    context = {'profile':profile}
    return render(request , 'profile/profile.html', context)

def editProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST , instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'done')
            return redirect('editProfile',pk=profile.id)
        else:
            messages.error(request, 'not done')
            return redirect('editProfile', pk=profile.id)
    context = {'profile':profile,
    'form':form}
    return render(request , 'profile/editProfile.html', context)

def address(request):
    orders = Order.objects.filter(user=request.user , ordered=True)
    profile = Profile.objects.get(user = request.user)
    context = {'profile':profile,
    'orders':orders}
    return render(request , 'profile/address.html', context)

def orders(request):
    orders = Order.objects.filter(user=request.user , ordered=True).order_by('-date')
    context = {'orders':orders}
    return render(request , 'profile/orders.html' , context)

@login_required(login_url='signin')
def wishlist(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.get(user=request.user)
        
    else:
        wishlist = None
    context  = {
        'wishlist':wishlist
        }
    return render(request , 'wishlist.html' , context)

@login_required(login_url='signin')
def addToWishlist(request, pk):
    item = Item.objects.get(id=pk)
    wishlist = get_object_or_404(Wishlist , user=request.user)
    if not wishlist.items.filter(item__id = item.id).exists():
        wishlist.items.add(item)
        messages.success(request, 'added to wishlist')
        return redirect('wishlist')
    
    return redirect('wishlist')



def removeFromWishlist(request, pk):
    item = Item.objects.get(id=pk)
    wishlist2 = get_object_or_404(Wishlist , user=request.user)
    
    if not wishlist2.items.filter(item__id = item.id).exists():
        wishlist2.items.remove(item)
        messages.success(request, 'removed from wishlist')
        
    
    return redirect('wishlist')

def blog(request):
    blogs = Blog.objects.all()
    context = {'blogs':blogs}
    return render(request , 'blog/blog.html', context)

def blogDetail(request,pk):
    blog = Blog.objects.get(id=pk)
    context = {
        'blog':blog }
    return render(request, 'blog/blog-detail.html', context)

def policy(request):
    return render(request , 'policy.html')

def termsAndConditions(request):
    return render(request, 'terms-and-conditions.html')

def privacyPolicy(request):
    return render(request, 'privacy-policy.html')

def shippingPolicy(request):
    return render(request, 'shipping-policy.html')