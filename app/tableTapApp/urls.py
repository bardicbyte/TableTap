from django.urls import path
from . import views

app_name = 'tableTapApp'

urlpatterns = [
    # Main Pages
    path('', views.index, name='index'),  
    path('menu-management/', views.menu_management, name='menu_management'),
    path('orders/', views.orders_page, name='orders_page'),

    # Menu Management
    # path('menu-management/create/', views.create_menu, name='create_menu'),  # Removed as it's not needed for direct access
    path('api/menus/<int:menu_id>/', views.get_menu, name='get_menu'),
    path('api/menus/<int:menu_id>/update/', views.update_menu, name='update_menu'),
    path('api/menus/<int:menu_id>/delete/', views.delete_menu, name='delete_menu'),
    path('api/menus/<int:menu_id>/detail/', views.menu_detail, name='menu_detail'),

    # Category Management
    path('api/menus/<int:menu_id>/categories/create/', views.create_category, name='create_category'),
    path('api/categories/<int:cat_id>/edit/', views.edit_category, name='edit_category'),
    path('api/categories/<int:cat_id>/delete/', views.delete_category, name='delete_category'),

    # Item Management
    path('api/categories/<int:cat_id>/items/create/', views.create_item, name='create_item'),
    path('api/items/<int:item_id>/', views.get_item, name='get_item'),
    path('api/items/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('api/items/<int:item_id>/delete/', views.delete_item, name='delete_item'),

    # Public Menu and QR
    path('menu/<int:menu_id>/qr/', views.menu_qr_code, name='menu_qr_code'),
    path('menu/<int:menu_id>/view/', views.public_menu, name='public_menu'),
    path('menu/<int:menu_id>/view/order/', views.submit_order, name='submit_order'),

    # Order Management
    path('orders/<int:order_id>/complete/', views.mark_order_completed, name='mark_order_completed'),
] 