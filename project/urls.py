from django.contrib import admin

from django.urls import path,include
from app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [

    path('api-auth/',include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/', admin.site.urls),
    
    path('register/', views.register, name='register'),
    path('user/',views.user_info),

    path('products/<str:name>/',views.all_products),
    path('product/<int:id>/', views.product_details),
    path('products/', views.getAllProducts),
    path('create/product/', views.PostProduct.as_view()),
    
    path('cart/', views.user_cart),
    path('cart/add/', views.AddToCart),
    path('cart/products', views.user_cart_products),
    
    path('checkout/', views.Checkout),

    path('wishlist/<int:pk>', views.Wishlist_pk),
    path('wishlist/', views.AddToWishlist),

]
