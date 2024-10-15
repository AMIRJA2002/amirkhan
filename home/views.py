from home.models import Post, Product, Order, OrderItem, Contact, UserChatId
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.core import serializers
from .balebot import send_message
from django.views import View
from typing import List
import json


from django.http import HttpResponse

def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Allow: /\n"
    )
    return HttpResponse(content, content_type="text/plain")




def home(request):
    last_five_posts = Post.objects.all()[:5]
    random_posts = Post.objects.order_by('?')[:2]
    return render(
        request,
        'home.html',
        {'last_five_posts': last_five_posts, 'random_posts': random_posts}
    )


def blog_post(request):
    return render(request, 'post_detail.html')


class PostListView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'post_list.html', context={'posts': posts})


class PostDetailView(View):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        return render(request, 'post_detail.html', context={'post': post})


from django.shortcuts import render, redirect
from django.http import JsonResponse


class OrderView(LoginRequiredMixin, View):
    login_url = reverse_lazy('account:login')  
    
    def get(self, request):
        products = Product.objects.all()

        return render(request, 'order.html', context={'products': products})

    def post(self, request):
        order_data = self.process_order(request)
        data = None
        for order in order_data:
            data = json.loads(order)
            if data['products'] == []:
                messages.error(request, 'محصولی انتخاب نشده است')
                return redirect('home:order')

        create_order = Order.objects.create(user=request.user)

        for product in data['products']:
            product_quantity = product['quantity']
            product_id = product['product_id']
            product = Product.objects.get(id=product_id)
            create_order.total_price += product.price * product_quantity
            create_order.save()
            order_item = OrderItem.objects.create(product=product, order=create_order, quantity=product_quantity)

        messages.success(request, 'سفارش با موقفیت ثبت شد.')
        self.send_message_to_bale(create_order)
        return redirect('home:home')

    def process_order(self, request):
        if request.method == 'POST':
            product_ids = [key for key in request.POST.keys() if key.startswith('product_id_')]

            products = []

            for product_id_key in product_ids:
                index = product_id_key.split('_')[-1]

                product_id = request.POST.get(product_id_key)

                quantity = int(request.POST.get(f'quantity_{index}', 0))

                description = request.POST.get(f'description_{index}', '')

                if quantity > 0:
                    product_data = {
                        'product_id': product_id,
                        'quantity': quantity,
                        'description': description
                    }
                    products.append(product_data)

            response_data = {
                'products': products
            }

            return JsonResponse(response_data)
        else:
            return redirect('home:index')

    def send_message_to_bale(self, order):
        # ساخت متن برای پیام
        message = f"شماره سفارش: {order.id} 🎉\n" \
                  f"شماره مشتری: {order.user.phone_number}\n" \
                  f"وضعیت پرداخت: {'پرداخت نشده' if not order.is_paid else 'پرداخت شده'}\n" \
                  f"مجموع قیمت سفارش: {order.format_number()}\n" \
                  f"تاریخ ایجاد: {order.get_jalali_date()}\n" \
                  f"سفارش ها:\n"

        # افزودن اطلاعات هر محصول به پیام
        for item in order.items.all():
            message += f"  - نام محصول: {item.product.name}, تعداد: {item.quantity}, " \
                       f"قیمت هر محصول: {item.product.format_number()}, قیمت کل: {item.product.format_number(number=item.product.price * item.quantity)}\n"

        # ارسال پیام
        chats = UserChatId.objects.all()
        for i in chats:
            send_message(i.chat_id, message)


class UserOrderView(LoginRequiredMixin, View):
    def get(self, request):
        user_orders = Order.objects.filter(user=request.user).prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('product'))
        )

        return render(request, 'user_order.html', context={'user_orders': user_orders.order_by('-created_at')})


class ContactUsView(View):
    def get(self, request):
        return render(request, 'contactus.html')    
    
    def post(self, request):
        name = request.POST.get('fullname')
        email = request.POST.get('user-email')
        message = request.POST.get('message')

        print(name, email, message)

        Contact.objects.create(name=name, email=email, message=message)


        messages.success(request, 'پیام شما با موفقیت ارسال شد.')
        return redirect('home:home')


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'  # مسیری که تمپلیت لیست محصولات قرار دارد
    context_object_name = 'products'  # نامی که در تمپلیت استفاده می‌شود
    paginate_by = 10  # تعداد محصولات در هر صفحه (اختیاری)

# ویوی جزییات محصول
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'  # مسیری که تمپلیت جزییات محصول قرار دارد
    context_object_name = 'product'  # نامی که در تمپلیت استفاده می‌شود
    pk_url_kwarg = 'id'  # نام پارامتری که از URL می‌گیریم (اینجا id)