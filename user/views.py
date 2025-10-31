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
        if User.objects.filter(username = Username).exists():
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

def forgot_password(request):
    return render(request, 'user/forgot_password.html')

def logout_view(request):
    request.session.flush()  # xóa tất cả session
    return redirect('index')

def profile(request):
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if 'id' not in request.session:
        return redirect('/user/login')
    
    # Lấy thông tin user từ session
    user_id = request.session.get('id')
    username = request.session.get('username')

    # Có thể lấy thêm dữ liệu từ DB nếu muốn
    user = User.objects.get(id=user_id)

    return render(request, 'user/profile.html', {
        'user': user,
    })

def export_profile_pdf(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Khai báo font Unicode (đường dẫn tới font .ttf)
    font_path = os.path.join("assets", "font", "DejaVuSans.ttf")
    pdfmetrics.registerFont(TTFont("DejaVu", font_path))

    # Tạo PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{user.username}_profile.pdf"'

    # Tạo canvas PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # ======= Header =======
    p.setFont("DejaVu", 18)
    p.drawString(180, height - 80, "THÔNG TIN NGƯỜI DÙNG")

    # ======= Thông tin người dùng =======
    p.setFont("DejaVu", 12)
    y = height - 130
    line_height = 25

    info = [
        ("ID người dùng", user.id),
        ("Tên đăng nhập", user.username),
        ("Mật khẩu (ẩn demo)", "********"),
        ("Email", user.email or "Chưa có"),
        ("Ngày sinh", user.date_of_birth.strftime("%d/%m/%Y") if user.date_of_birth else "Chưa có"),
        ("Ngày tạo tài khoản", user.create_at.strftime("%d/%m/%Y %H:%M") if user.create_at else "Không rõ"),
        ("Trạng thái online", "Đang hoạt động" if user.online_status else "Ngoại tuyến"),
        ("Vai trò", user.role),
        ("Địa chỉ", user.address or "Chưa có"),
        ("Giới tính", user.gender or "Chưa có"),
        ("Xuất lúc", timezone.now().strftime("%d/%m/%Y %H:%M:%S")),
    ]

    for label, value in info:
        p.drawString(100, y, f"{label}: {value}")
        y -= line_height

    y -= 40
    p.setFont("DejaVu", 11)
    p.drawString(100, y, "Báo cáo được tạo tự động bởi hệ thống Django")

    p.showPage()
    p.save()
    return response
