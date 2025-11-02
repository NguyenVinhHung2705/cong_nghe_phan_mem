from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.shortcuts import get_object_or_404
from .models import User
from django.utils import timezone
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
# Create your views here.

def login(request):
    if request.method == "POST":
        Username = request.POST.get("username")
        Password = request.POST.get("password")

        
        user = User.objects.filter(username=Username, password=Password).exists()
        # Nếu đăng nhập đúng
        if user:
            tmp_user = User.objects.get(username = Username, password = Password)
            request.session['id'] = tmp_user.id
            request.session['username'] = tmp_user.username
            return HttpResponse("""
                <script>
                    alert("Đăng nhập thành công!");
                    window.location.href = '/dashboard';
                </script>
            """)
        else:
            return render(request, 'user/login.html', {'error': 'Sai username hoặc password'})
        
    return render(request, 'user/login.html')


def register(request):
    if request.method == "POST":
        Username = request.POST.get("username")
        Password = request.POST.get("password")
        Password_again = request.POST.get("password_again")
        if Password != Password_again:
            return render(request, 'user/register.html', {'error': 'Mật khẩu không trùng nhau'})
        elif User.objects.filter(username = Username).exists():
            return render(request, 'user/register.html', {'error': 'Đã tồn tại người dùng này'})
        User.objects.create(
            username = Username,
            password = Password
        )
        return HttpResponse("""
                <script>
                    alert("Đăng kí thành công!");
                    window.location.href = '/user/login';
                </script>
            """)
    return render(request, 'user/register.html')


def logout_view(request):
    request.session.flush()  # xóa tất cả session
    return redirect('index')

def profile(request):
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if 'id' not in request.session:
        return redirect('/user/login')
    
    # Lấy thông tin user từ session
    user_id = request.session.get('id')

    # Có thể lấy thêm dữ liệu từ DB nếu muốn
    user = User.objects.get(id=user_id)

    return render(request, 'user/profile.html', {
        'user': user,
    })

def export_profile_pdf(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # ===== Khai báo font Unicode =====
    font_path = os.path.join("assets", "font", "DejaVuSans.ttf")
    pdfmetrics.registerFont(TTFont("DejaVu", font_path))

    # ===== Tạo phản hồi PDF =====
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{user.username}_profile.pdf"'

    # ===== Khởi tạo canvas =====
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # ===== Tiêu đề =====
    p.setFont("DejaVu", 18)
    p.drawCentredString(width / 2, height - 80, "THÔNG TIN NGƯỜI DÙNG")

    # ===== Bảng thông tin =====
    p.setFont("DejaVu", 12)
    y = height - 130
    line_height = 25
    label_x = 100     # cột trái
    value_x = 300     # cột phải

    # Dữ liệu hiển thị
    info = [
        ("ID người dùng", user.id),
        ("Tên đăng nhập", user.username),
        ("Email", user.email or "Chưa có"),
        ("Ngày sinh", user.date_of_birth.strftime("%d/%m/%Y") if user.date_of_birth else "Chưa có"),
        ("Ngày tạo", user.create_at.strftime("%d/%m/%Y %H:%M") if user.create_at else "Không rõ"),
        ("Vai trò", user.role or "Không xác định"),
        ("Địa chỉ", user.address or "Chưa có"),
        ("Giới tính", user.gender or "Chưa có"),
        ("Tên shop", user.shop_name or "Chưa có"),
        ("Địa chỉ shop", user.shop_address or "Chưa có"),
    ]

    # In từng dòng ra PDF
    for label, value in info:
        p.drawString(label_x, y, f"{label}:")
        p.drawString(value_x, y, str(value))
        y -= line_height

    # ===== Thời gian xuất =====
    y -= 20
    p.setFont("DejaVu", 10)
    p.drawString(label_x, y, f"Xuất lúc: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # ===== Ghi chú =====
    y -= 30
    p.setFont("DejaVu", 10)
    p.drawString(label_x, y, "Báo cáo được tạo tự động bởi hệ thống Django.")

    # ===== Lưu trang =====
    p.showPage()
    p.save()

    return response

def dang_ky_ban_hang(request):
    if 'id' not in request.session:
        return redirect('login')  # nếu chưa đăng nhập
    user_id = request.session['id']
    user = User.objects.get(id=user_id)  # lấy user từ DB bằng id trong session
    if user.role != "user-advance" or user.role != "admin":
        return render(request, 'user/dang_ky_ban_hang.html')
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        shop_address = request.POST.get('shop_address')

        user.shop_name = shop_name
        user.shop_address = shop_address
        user.role = 'user-advance'
        user.save()
        return redirect('index')  # chuyển về trang chủ
    
from django.shortcuts import render, redirect
from django.conf import settings
from product.models import Product

def khu_vuc_ban_hang(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')

    # Nếu người bán gửi form thêm sản phẩm
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        description = request.POST.get('description', '')
        image_file = request.FILES.get('image')

        # Tạo sản phẩm mới bằng ORM
        Product.objects.create(
            user_id=user_id,
            product_name=product_name,
            price=price,
            description=description,
            image=image_file
        )

        return redirect('khu_vuc_ban_hang')

    # Lấy danh sách sản phẩm của người bán hiện tại
    products = Product.objects.filter(user_id=user_id).order_by('-id')

    return render(request, 'user/khu_vuc_ban_hang.html', {
        'products': products
    })

    
