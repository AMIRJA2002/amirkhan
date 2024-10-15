from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap, ProductSitemap


sitemaps = {
    'posts': PostSitemap,
    'products': ProductSitemap,
}


app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('post/<int:id>/', views.PostDetailView.as_view(), name='post-detail'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('user-order/', views.UserOrderView.as_view(), name='user-order'),
    path('contact/', views.ContactUsView.as_view(), name='contact'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('product/<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

