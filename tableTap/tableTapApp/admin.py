from django.contrib import admin
from .models import (
    Users,
    Roles,
    Business,
    Tables,
    Menu_Categories,
    Menu_Items,
    Item_Options,
    Orders,
    Order_Items,
    Table_Sessions,
    Order_Item_Options
)

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('created_at',)

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone', 'email')
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)

@admin.register(Menu_Items)
class MenuItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'menu_category')
    search_fields = ('name', 'description')
    list_filter = ('menu_category', 'created_at')

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_id', 'is_paid', 'total_price', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('id', 'table_id__name')

@admin.register(Order_Items)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'item_price')
    search_fields = ('order__id', 'menu_item__name')

# Register remaining models with basic configuration
admin.site.register(Roles)
admin.site.register(Tables)
admin.site.register(Menu_Categories)
admin.site.register(Item_Options)
admin.site.register(Table_Sessions)
admin.site.register(Order_Item_Options)
