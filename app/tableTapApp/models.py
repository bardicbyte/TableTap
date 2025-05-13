from django.db import models
from django.contrib.auth.models import User

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    website = models.URLField(max_length=255)
    logo_url = models.URLField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Menus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='menus')
    
    def __str__(self):
        return f"{self.name} - {self.business.name}"
    
class Tables(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Menu_Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menus, on_delete=models.CASCADE, related_name='categories')
    
class Menu_Items(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    image_url = models.URLField(max_length=255)
    menu_category = models.ForeignKey(Menu_Categories, on_delete=models.CASCADE)
    
class Item_Options(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    menu_item = models.ForeignKey(Menu_Items, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2)

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    table_id = models.ForeignKey(Tables, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)

class Order_Items(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu_Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    special_instructions = models.TextField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Table_Sessions(models.Model):
    id = models.AutoField(primary_key=True)
    table_id = models.ForeignKey(Tables, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order_Item_Options(models.Model):
    id = models.AutoField(primary_key=True)
    order_item = models.ForeignKey(Order_Items, on_delete=models.CASCADE)
    item_option = models.ForeignKey(Item_Options, on_delete=models.CASCADE)
    option_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Subscription(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.CharField(max_length=32, choices=PLAN_CHOICES)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.plan} ({'Active' if self.is_active else 'Inactive'})"
    