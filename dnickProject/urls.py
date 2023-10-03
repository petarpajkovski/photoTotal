"""
URL configuration for dnickProject project.

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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from photoTotal import views

urlpatterns = [
    path('', views.get_homepage, name='get_homepage'),
    path('admin/', admin.site.urls),
    # Login Paths
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    # Brands Paths
    path('add_brands/', views.add_brand, name='add_brand'),
    path('delete_brand/<int:pk>', views.delete_brand, name='delete_brand'),
    # Cameras Paths
    path('admin_camera/', views.admin_camera, name='admin_camera'),
    path('add_camera/', views.add_camera, name='add_camera'),
    path('delete_camera/<int:pk>', views.delete_camera, name='delete_camera'),
    path('camera_page/', views.camera_page, name='camera_page'),
    # Lenses Paths
    path('admin_lenses/', views.admin_lens, name='admin_lenses'),
    path('add_lenses/', views.add_lens, name='add_lenses'),
    path('delete_lenses/<int:pk>', views.delete_lens, name='delete_lenses'),
    path('lens_page/', views.lens_page, name='lens_page'),
    # Accessories Paths
    path('admin_accessories/', views.admin_accessories, name='admin_accessories'),
    path('add_accessories/', views.add_accessories, name='add_accessories'),
    path('delete_accessories/<int:pk>', views.delete_accessories, name='delete_accessories'),
    path('accessories_page/', views.accessories_page, name='accessories_page'),
    # Product Paths
    path('product/<int:pk>', views.product_page, name="product_page"),
    # Cart Paths
    path('cart/', views.cart, name='cart'),
    # Checkout Paths
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    # Search Paths
    path('search/', views.search, name='search'),
    # Photos Paths :TODO
    # path('photos/', views.photos, name='photos'),
    # path('add_photo/', views.photos_form, name='add_photo'),
    # User Paths :TODO
    # path('profile/', views.profile, name='profile'),
    # path('user_photo_delete/<int:pk>', views.photos_delete, name='user_photo_delete'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
