##  TableTap


- TableTap is a Software as a Service (SaaS) platform designed specifically for
restaurants, cafes, and coffee shops to streamline their ordering process.

- This innovative platform allows these businesses to sign up and create a
digital menu, complete with categories, items, and prices. 

- Upon setting up their account, they can enter the total number of tables in their establishment.

- The system then generates unique QR codes for each table, which can be
printed out and placed at tables for guests to scan.

## Main Features:

- Digital Menu Creation:
  - Create and customize digital menus with categories, items, and prices.
  - Add images, descriptions, and nutritional information to menu items.
  - Set menu visibility and availability for different times of day or days of the week.

- Table QR Code Generation:
  - Generate unique QR codes for each table in the establishment.
  - Print these QR codes and place them at tables for easy scanning.

- Ordering and Payment:
    Staff can view and manage orders from the TableTap dashboard.


Project (app/) - The overall website configuration:
app/                 
├── tableTap/             
│   ├── settings.py       
│   ├── urls.py          
│   └── wsgi.py          


App (tableTapApp/) - The specific functionality:
tableTapApp/              
├── models.py            
├── views.py            
├── admin.py           
└── templates/         
    └── tableTapApp/   

├── accounts/            # User management
│   └── (authentication, profiles, roles)

## Django Page Creation Process:

1. **Template** (HTML):
   - Located in templates directory
   - Contains the actual HTML/content
   - Can extend base templates
   - Uses Django template language

2. **View** (Python):
   - Handles the logic/processing
   - Gets data from models
   - Renders templates with context
   - Located in views.py

3. **URL** (Python):
   - Maps URLs to views
   - Defines URL patterns
   - Handles URL parameters
   - Located in urls.py

4. **Connect URLs**:
   - Add app URLs to main project urls.py
   - Use include() to connect app-specific URLs
   - Example:
     ```python
     # project/urls.py
     urlpatterns = [
         path('app/', include('app.urls')),
     ]
     ```

Example Flow:
1. User visits URL
2. URL pattern matches and calls view
3. View processes data and renders template
4. Template displays to user