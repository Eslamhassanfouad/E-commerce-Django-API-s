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
    path('user/<int:pk>',views.user_info),

    path('products/<str:name>/',views.all_products),
    path('product/<int:id>/', views.product_details),
    path('products/', views.getAllProducts),
    # path('products/<str:name>/', views.searchProduct),
    # path('create-product/', views.createProduct),
    # path('update-product/<int:id>/', views.updateProduct),
    # path('delete-product/<int:id>/', views.deleteProduct),
    # path('products/<str:name>/',views.all_products),
    
    path('cart/', views.cart_List),
    path('cart/<int:pk>', views.cart_pk),
    path('cart/<int:pk>/products', views.user_cart_products),    
    path('checkout/<int:pk>', views.Checkout_pk),

    path('wishlist/<int:pk>', views.Wishlist_pk),
]
