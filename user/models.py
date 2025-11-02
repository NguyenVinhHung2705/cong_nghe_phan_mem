from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=50, unique=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    online_status = models.BooleanField(default=False)
    role = models.CharField(max_length=10, default="user")
    address = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    shop_name = models.CharField(max_length=255, default="Chưa đăng kí shop")
    shop_address = models.CharField(max_length=255, default="Chưa đăng kí shop")
    def __str__(self):
        Id = self.id
        Username = self.username if self.username is not None else "NULL"
        Password = self.password if self.password is not None else "NULL"
        Email = self.email if self.email is not None else "Trống"
        Date_of_birth = self.date_of_birth if self.date_of_birth is not None else "Trống"
        Create_at = self.create_at
        Online_status = self.online_status
        Role = self.role
        Address = self.address if self.address is not None else "Trống"
        Gender = self.gender if self.gender is not None else "Trống"
        Shop_name = self.shop_name
        Shop_address = self.shop_address

        return (
            f"id: {Id} | "
            f"username: {Username} | "
            f"password: {Password} | "
            f"email: {Email} | "
            f"date_of_birth: {Date_of_birth} | "
            f"create_at: {Create_at} | "
            f"online_status: {Online_status} | "
            f"role: {Role} | "
            f"address: {Address} | "
            f"gender: {Gender} | "
            f"shop_name: {Shop_name} | "
            f"shop_address: {Shop_address}"
        )