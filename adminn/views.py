from django.shortcuts import render, redirect 
from basic.models import Order , Item ,Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login , logout , authenticate
from basic.models import Item , Profile , Order , Enquiry, Coupons
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


@login_required(login_url='adminLogin')
@user_passes_test(lambda u: u.is_superuser)
def adminindex(request):
    displayItems = []
    displayOrders = []
    orders = Order.objects.filter(ordered=True).order_by('-date')
    
    items = Item.objects.all()
    for i in range(len(orders)):
        if i<6:
            displayOrders.append(orders[i])
    for i in range(len(items)):
        if i<6:
            displayItems.append(items[i])

    ordersCount = orders.count()
    itemsCount = items.count()
    profiles = Profile.objects.all().count()
    enquiry = Enquiry.objects.filter(status=False).count()
    context = {
        'items': displayItems,
        'orders': displayOrders,
        'ordersCount': ordersCount,
        'itemsCount': itemsCount,
        'profiles': profiles,
        'enquiry':enquiry
    }
    return render(request , 'adminn/dashboard.html' , context)
@csrf_exempt
def adminLogin(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        user = authenticate(request ,username= uname , password=pwd)
        if user is not None:
            if user.is_superuser:
                login(request , user)
                return redirect('adminindex')

            else:
                messages.error(request , 'Not Super User')
        else:
            messages.warning(request , 'Wrong ')
    return render(request , 'adminn/signin.html')

def logoutPage(request):
    logout(request)
    return redirect('adminLogin')
@login_required(login_url='adminLogin')
def orderDetail(request, pk):
    order = Order.objects.get(id=pk)
    params = {'order': order}
    return render(request , 'adminn/order-detail.html',params) 
@login_required(login_url='adminLogin')
def productDetail(request , pk):
    product = Item.objects.get(id=pk)
    context ={
        'product': product
    }
    return render(request , 'adminn/product-detail.html' , context)

@login_required(login_url='adminLogin')
def allOrders(request):
    orders = Order.objects.filter(ordered=True)
    context = {
        'orders': orders
    }
    return render(request , 'adminn/orders.html' ,context)
@login_required(login_url='adminLogin')
def orderDelete(request,pk):
    order = Order.objects.get(id=pk)
    for i in order.items.all():
        i.delete()
    order.delete()
    return redirect('allOrders')
@login_required(login_url='adminLogin')
def allProducts(request):
    products = Item.objects.all()
    context = {
        'products': products
    }
    return render(request , 'adminn/products.html' , context)
@login_required(login_url='adminLogin')
def deleteProduct(request, pk):
    item = Item.objects.get(id=pk)
    item.delete()
    return redirect('allProducts')
@login_required(login_url='adminLogin')
def newProduct(request):
    form = NewItemForm()
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request , 'ADded')
            return redirect('adminindex')
        else:
            print(form.errors)
            return HttpResponse('<h1>Wrong Action</h1>')

    context = {'form': form}
    return render(request , 'adminn/newProduct.html' , context)

@login_required(login_url='adminLogin')
def updateProduct(request , pk):
    product = Item.objects.get(id=pk)
    form  = NewItemForm(instance=product)
    if request.method == 'POST':
        form = NewItemForm(request.POST , instance=product )
        str1 = str(product.name) +" "+ str(product.flavour)+" " + str(product.qty)
        if form.is_valid():
            form.save()
            messages.success(request , str1)
            return redirect('allProducts')
        else:
            messages.error(request , 'Something Wrong. Call Us At 9910691503 for Support!')
            return redirect('updateProduct', pk=product.id)

    context = {
        'form':form,
        'product':product,
    }
    return render(request , 'adminn/update-item.html', context)

@login_required(login_url='adminLogin')
def profile(request):
    profile = Profile.objects.all()
    
    context = {
        'profile':profile,
    }
    return render(request , 'adminn/profile.html' ,context)

@login_required(login_url='adminLogin')
def enquiry(request):
    enquiry = Enquiry.objects.filter(status=False)
    context = {
        'enquiry':enquiry,
    }
    return render(request , 'adminn/enquiry.html' , context)

@login_required(login_url='adminLogin')
def mark(request, pk):
    enquiry = Enquiry.objects.get(id=pk)
    enquiry.status = True
    enquiry.save()  
    messages.success(request, 'enquiry',)
    return redirect('enquiry')

@login_required(login_url='adminLogin')
def allEnquiry(request):
    enquiry = Enquiry.objects.all()
    context = {'enquiry': enquiry}
    return render(request , 'adminn/allEnquiry.html', context)


def coupons(request):
    coupons = Coupons.objects.all()
    
    if request.method == 'POST':
        code = request.POST.get('code')
        percent = request.POST.get('percent')

        obj = Coupons.objects.create(tag=code, amount=percent)
        obj.save()
        messages.success(request,'New Coupon Created Successfully')
        return redirect('coupons')
    
    
    context = {'coupons': coupons}
    return render(request , 'adminn/coupons.html', context)

def couponsDetail(request , pk):
    coupon = Coupons.objects.get(id=pk)
    l1 = []

    for i in coupon.order_items.all():
        if i.ordered == True:
            l1.append(i)

    
    context = {
        'coupon': coupon,
        'orders':l1,
        'count': len(l1)
    }
    return render(request , 'adminn/coupon_detail.html', context)