from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Menus, Business, Menu_Items, Menu_Categories, Orders, Order_Items, Tables
import qrcode
from io import BytesIO
import decimal

# Create your views here.
def index(request):
    return render(request, 'tableTapApp/index.html')

@login_required
def menu_management(request):
    business = get_object_or_404(Business, owner=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        Menus.objects.create(
            name=name,
            description=description,
            is_active=is_active,
            business=business
        )
        return redirect('tableTapApp:menu_management')
    menus = Menus.objects.filter(business=business)
    return render(request, 'tableTapApp/menu_management.html', {'menus': menus})

@login_required
@require_POST
def create_menu(request):
    business = get_object_or_404(Business, owner=request.user)
    name = request.POST.get('name')
    description = request.POST.get('description', '')
    is_active = request.POST.get('is_active') == 'on'

    menu = Menus.objects.create(
        name=name,
        description=description,
        is_active=is_active,
        business=business
    )
    
    return redirect('tableTapApp:menu_management')

@login_required
def get_menu(request, menu_id):
    business = get_object_or_404(Business, owner=request.user)
    menu = get_object_or_404(Menus, id=menu_id, business=business)
    
    return JsonResponse({
        'id': menu.id,
        'name': menu.name,
        'description': menu.description,
        'is_active': menu.is_active
    })

@login_required
@require_POST
def update_menu(request, menu_id):
    business = get_object_or_404(Business, owner=request.user)
    menu = get_object_or_404(Menus, id=menu_id, business=business)
    
    menu.name = request.POST.get('name')
    menu.description = request.POST.get('description', '')
    menu.is_active = request.POST.get('is_active') == 'on'
    menu.save()
    
    return redirect('tableTapApp:menu_management')

@login_required
@require_POST
def delete_menu(request, menu_id):
    business = get_object_or_404(Business, owner=request.user)
    menu = get_object_or_404(Menus, id=menu_id, business=business)
    menu.delete()
    
    return JsonResponse({'status': 'success'})

@login_required
def menu_detail(request, menu_id):
    business = get_object_or_404(Business, owner=request.user)
    menu = get_object_or_404(Menus, id=menu_id, business=business)
    categories = menu.categories.all()
    categories_data = []
    for cat in categories:
        items = cat.menu_items_set.all() if hasattr(cat, 'menu_items_set') else cat.menu_items.all() if hasattr(cat, 'menu_items') else []
        # Fallback: get items by foreign key
        if not items:
            from .models import Menu_Items
            items = Menu_Items.objects.filter(menu_category=cat)
        items_data = [
            {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': str(item.price),
            } for item in items
        ]
        categories_data.append({
            'id': cat.id,
            'name': cat.name,
            'items': items_data
        })
    return JsonResponse({
        'menu': {
            'id': menu.id,
            'name': menu.name,
        },
        'categories': categories_data
    })

@login_required
@require_POST
@csrf_exempt
def create_category(request, menu_id):
    business = get_object_or_404(Business, owner=request.user)
    menu = get_object_or_404(Menus, id=menu_id, business=business)
    try:
        data = json.loads(request.body)
        name = data.get('name')
        if not name:
            return JsonResponse({'status': 'error', 'error': 'Name is required.'})
        from .models import Menu_Categories
        cat = Menu_Categories.objects.create(
            name=name,
            business_id=business,
            menu=menu
        )
        return JsonResponse({'status': 'success', 'id': cat.id, 'name': cat.name})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})

@login_required
@require_POST
@csrf_exempt
def edit_category(request, cat_id):
    from .models import Menu_Categories
    cat = get_object_or_404(Menu_Categories, id=cat_id)
    business = get_object_or_404(Business, owner=request.user)
    if cat.business_id != business:
        return JsonResponse({'status': 'error', 'error': 'Permission denied.'})
    try:
        data = json.loads(request.body)
        name = data.get('name')
        if not name:
            return JsonResponse({'status': 'error', 'error': 'Name is required.'})
        cat.name = name
        cat.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})

@login_required
@require_POST
@csrf_exempt
def delete_category(request, cat_id):
    from .models import Menu_Categories
    cat = get_object_or_404(Menu_Categories, id=cat_id)
    business = get_object_or_404(Business, owner=request.user)
    if cat.business_id != business:
        return JsonResponse({'status': 'error', 'error': 'Permission denied.'})
    try:
        cat.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})

@login_required
@require_POST
@csrf_exempt
def create_item(request, cat_id):
    cat = get_object_or_404(Menu_Categories, id=cat_id)
    business = get_object_or_404(Business, owner=request.user)
    if cat.business_id != business:
        return JsonResponse({'status': 'error', 'error': 'Permission denied.'})
    try:
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description', '')
        price = data.get('price')
        image_url = data.get('image_url', '')
        if not name or price is None:
            return JsonResponse({'status': 'error', 'error': 'Name and price are required.'})
        item = Menu_Items.objects.create(
            name=name,
            description=description,
            price=price,
            text=description,
            image_url=image_url,
            menu_category=cat
        )
        return JsonResponse({'status': 'success', 'id': item.id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})

@login_required
def get_item(request, item_id):
    item = get_object_or_404(Menu_Items, id=item_id)
    business = get_object_or_404(Business, owner=request.user)
    if item.menu_category.business_id != business:
        return JsonResponse({'status': 'error', 'error': 'Permission denied.'})
    return JsonResponse({
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': str(item.price),
        'image_url': item.image_url,
        'menu_category': item.menu_category.id
    })

@login_required
@require_POST
@csrf_exempt
def edit_item(request, item_id):
    item = get_object_or_404(Menu_Items, id=item_id)
    business = get_object_or_404(Business, owner=request.user)
    if item.menu_category.business_id != business:
        return JsonResponse({'status': 'error', 'error': 'Permission denied.'})
    try:
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description', '')
        price = data.get('price')
        image_url = data.get('image_url', '')
        if not name or price is None:
            return JsonResponse({'status': 'error', 'error': 'Name and price are required.'})
        item.name = name
        item.description = description
        item.price = price
        item.text = description
        item.image_url = image_url
        item.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})

@login_required
@require_POST
@csrf_exempt
def delete_item(request, item_id):
    item = get_object_or_404(Menu_Items, id=item_id)
    business = get_object_or_404(Business, owner=request.user)
    if item.menu_category.business_id != business:
        return JsonResponse({'status': 'error', 'error': 'Permission denied.'})
    try:
        item.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})

def menu_qr_code(request, menu_id):
    # Generate a QR code for the menu's public link
    from django.urls import reverse
    menu_url = request.build_absolute_uri(reverse('tableTapApp:public_menu', args=[menu_id]))
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(menu_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return HttpResponse(buffer, content_type="image/png")

def public_menu(request, menu_id):
    # Placeholder: Render a simple public menu page
    menu = get_object_or_404(Menus, id=menu_id)
    categories = menu.categories.all()
    return render(request, 'tableTapApp/public_menu.html', {'menu': menu, 'categories': categories})

@csrf_exempt
def submit_order(request, menu_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'error': 'POST required'})
    try:
        data = json.loads(request.body)
        table_number = data.get('table_number')
        items = data.get('items', [])
        if not table_number or not items:
            return JsonResponse({'status': 'error', 'error': 'Table number and items required.'})
        # Find or create table
        table, _ = Tables.objects.get_or_create(name=table_number)
        # Calculate total
        total = sum(decimal.Decimal(str(i['price'])) * int(i['qty']) for i in items)
        order = Orders.objects.create(table_id=table, total_price=total, payment_method='Unpaid')
        for i in items:
            menu_item = Menu_Items.objects.get(id=i['id'])
            Order_Items.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=i['qty'],
                special_instructions='',
                item_price=menu_item.price
            )
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})

@login_required
def orders_page(request):
    orders = Orders.objects.all().order_by('-id')
    for order in orders:
        order.order_items = Order_Items.objects.filter(order=order)
    return render(request, 'tableTapApp/orders.html', {'orders': orders})

@login_required
@require_POST
def mark_order_completed(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    order.is_paid = True
    order.save()
    return redirect('tableTapApp:orders_page')
