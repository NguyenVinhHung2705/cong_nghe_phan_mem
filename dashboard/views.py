from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from product.models import Product

def index(request):
    product_list = Product.objects.all()
    list_session = request.session

    # --- Thêm phân trang ---
    paginator = Paginator(product_list, 8)  # 8 sản phẩm mỗi trang
    page_number = request.GET.get('page')   # lấy ?page= trên URL
    products = paginator.get_page(page_number)  # lấy dữ liệu trang tương ứng

    # --- Context ---
    context = {'products': products}
    if list_session.get('id'):
        context['list_session'] = list_session

    return render(request, 'dashboard/index.html', context)
