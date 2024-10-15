from django.contrib import admin
from .models import Post, Product, Order, OrderItem, Contact, AdminNumbers, UserChatId


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'created_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


class AdminInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'is_paid')
    inlines = (AdminInline, )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')



@admin.register(AdminNumbers)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('admin1', 'admin2')

@admin.register(UserChatId)
class ChatIdAdmin(admin.ModelAdmin):
    list_display = ('chat_id', )