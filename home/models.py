from django.contrib.auth import get_user_model
from django.db import models
import jdatetime
from django.urls import reverse, reverse_lazy

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    image = models.ImageField(upload_to='post/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:30]

    def get_jalali_date(self):
        if self.created_at:
            return jdatetime.date.fromgregorian(date=self.created_at).strftime('%Y/%m/%d')
        return None

    def get_absolute_url(self):
        return reverse('home:post-detail', kwargs={'id': self.id})  # نام الگوی URL و آرگومان‌ها


class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def format_number(self, number=None):
        if number:
            return '{:,}'.format(number)

        return '{:,}'.format(self.price)

    def get_absolute_url(self):
        return reverse_lazy('home:product-detail', kwargs={'id': self.id})


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'

    def get_jalali_date(self):
        if self.created_at:
            return jdatetime.date.fromgregorian(date=self.created_at).strftime('%Y/%m/%d')
        return None

    def format_number(self):
        return '{:,}'.format(self.total_price)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=1)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=300)
    message = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.email}'



class AdminNumbers(models.Model):
    admin1 = models.CharField(max_length=11, null=True, blank=True)
    admin2 = models.CharField(max_length=11, null=True, blank=True)


class UserChatId(models.Model):
    chat_id = models.CharField(max_length=10000)

