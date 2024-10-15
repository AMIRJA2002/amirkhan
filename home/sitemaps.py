from django.contrib.sitemaps import Sitemap
from .models import Post, Product


class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class ProductSitemap(Sitemap):
    changefreq = "daily"  # فرکانس به‌روزرسانی سایت مپ
    priority = 0.8        # اولویت نمایش URLها در سایت مپ

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()  # باید مطمئن شویم get_absolute_url برای Product تعریف شده است