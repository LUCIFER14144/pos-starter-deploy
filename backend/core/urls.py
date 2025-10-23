from django.urls import path
from . import views
urlpatterns = [
    path('products/', views.products_list),
    path('products/create/', views.create_product),
    path('sales/', views.create_sale),
    path('negotiations/', views.negotiations_list),
    path('negotiations/<int:nid>/approve/', views.approve_negotiation),
    path('manager/verify_pin/', views.verify_manager_pin),
]
