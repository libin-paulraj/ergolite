from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "home"


urlpatterns = [
    path('', views.home_view, name='home'),
    path('category/', views.category_view, name='category'),
    path('products/',views.products_view, name='products'),
    path('contact/',views.contact_view, name='contact'),
    path('addcart/', views.add_cart_view, name='add_cart'), 
    path('cart/', views.cart_view, name='cart'),
    path('productdetail/<int:id>/', views.product_details, name='productdetail'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('register',views.register_view, name='register'),
    # path('update/<int:product_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    # path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('checkout/', views.checkout, name='checkout'),
    path("remove/<int:cart_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('checkout/', views.checkout, name='checkout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)