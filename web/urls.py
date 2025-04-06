# web/urls.py
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('product/', views.product, name='product'),
    path('carts/', views.carts, name='carts'),
    path('contact/', views.contact, name='contact'),
    path('emailsend/', views.emailsend, name='emailsend'),
    path('product/detail-<str:product_code>/', views.product_detail, name='product_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
