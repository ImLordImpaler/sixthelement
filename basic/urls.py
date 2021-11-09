from django.urls import path , include
from . import views
urlpatterns = [
    
    path('' , views.index , name='index'),
    path('item/<str:pk>/' , views.item , name='item'),
    

    #auth 
    path('signin' , views.signin , name='signin'),
    path('register', views.register , name='register'),
    path('logoutPage' , views.logoutPage , name='logoutPage'),

    #nav 
    path('shop' , views.shop , name='shop'),
    path('filter/<str:pk>' , views.shop2 , name='shop2'),
    
    path('blog' , views.blog , name='blog'),
    path('contact' , views.contact , name='contact'),
    path('aboutus' , views.aboutus , name='aboutus'),

    path('reorder/<str:pk>', views.reorder , name='reorder'),
    path('add-to-cart/<str:pk>' , views.addToCart , name='addToCart'),
    path('remove-single-item/<str:pk>' , views.removeSingleItem , name='removeSingleItem'),
    path('add-single-item/<str:pk>' , views.addSingleItem , name='addSingleItem'),
    path('remove-item/<str:pk>' ,views.removeItem , name='removeItem'),

    #cart
    path('cart' , views.cart , name='cart'),
    path('payment/<str:pk>' , views.payment , name='payment'),
    path('success' , views.success , name='success'),
    path('checkout' , views.checkout , name='checkout'),
    path('fail' , views.fail , name='fail'),
    path('paymenthandler' , views.paymenthandler , name='paymenthandler'),
    
    path('order-details/<str:pk>' , views.order_details , name='order_details'),
    #blog
    path('blog', views.blog , name='blog'),
    path('blog/<str:pk>' , views.blogDetail , name='blogDetail'),
    
    #profile
    path('dashboard' , views.dashboard , name='dashboard'),
    path('profile' , views.profile , name='profile'),
    path('editProfile/<str:pk>' , views.editProfile , name='editProfile'),
    path('address' , views.address , name='address'),
    path('orders', views.orders , name='orders'),

    path('remove-coupon/<str:pk>/', views.removeCoupon , name='remove-Coupon'),
    #wishlist 
    path('wishlist' , views.wishlist , name='wishlist'),
    path('add-to-wishlist/<str:pk>' , views.addToWishlist , name='addToWishlist'),
    path('remove-from-wishlist/<str:pk>' , views.removeFromWishlist , name='removeFromWishlist'),

    path('policy' , views.policy , name='policy'),

    path('message_confirmation' , views.messageConfirmation , name='messageConfirmation'),
    
    path('terms-and-conditions' , views.termsAndConditions , name='tandC'),
    path('privacy-policy' , views.privacyPolicy , name='privacyPolicy'),
    path('shipping-policy' , views.shippingPolicy , name='shippingPolicy')
    
]