from django.urls import path , include
from . import views
urlpatterns = [
    #dashboard
    path('' , views.adminindex , name='adminindex'),

    #auth
    path('adminLogin' , views.adminLogin , name='adminLogin'),
    path('adminLogout' , views.logoutPage , name='adminLogout'),

    #order
    path('order/<str:pk>/', views.orderDetail , name='orderDetail'), 
    path('allOrders' , views.allOrders , name='allOrders'),
    
    path('order-delete/<str:pk>', views.orderDelete , name='orderDelete'),

    path('product/<str:pk>/', views.productDetail , name='productDetail'), 
    path('allProducts' , views.allProducts , name='allProducts'),
    path('newProduct' , views.newProduct , name='newProduct'),
    path('updateProduct/<str:pk>' , views.updateProduct , name="updateProduct"),
    path('deleteProduct/<str:pk>/', views.deleteProduct , name='deleteProduct'),

    path('profile' , views.profile , name="adminprofile"),
    #profile Detail

    #enquiry
    path('enquiry' , views.enquiry , name='enquiry'),
    path('mark/<str:pk>' , views.mark , name="mark"),
    path('allEnquiry' , views.allEnquiry , name='allEnquiry'),

    path('coupons', views.coupons , name='coupons'),
    path('coupons/<str:pk>', views.couponsDetail , name='couponsDetail'),
]