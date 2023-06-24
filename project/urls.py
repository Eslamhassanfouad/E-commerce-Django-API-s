"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path,include
from app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    
    #Search by name URL
    path('products/<str:name>/',views.all_products),
    path('user/<int:pk>',views.user_info),
------------------------------------------------------------------------------------------------------------------------
    
    
    
    path('api-auth/',include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('register/', views.register, name='register'),
=======

    path('products/', views.getAllProducts),
    path('products/<str:name>/', views.searchProduct),
    path('get-product/<int:id>/', views.getProduct),
    path('create-product/', views.createProduct),
    path('update-product/<int:id>/', views.updateProduct),
    path('delete-product/<int:id>/', views.deleteProduct),
   # path('products/<str:name>/',views.all_products),
    path('user/<int:pk>',views.user_info),

-------------------------------------------------------------------------------------------------------------------------
    
    # Wishlist retrieve
    path('wishlist/<int:pk>', views.Wishlist_pk),
    # Checkout
    path('checkout/<int:pk>', views.Checkout_pk),
    
]
