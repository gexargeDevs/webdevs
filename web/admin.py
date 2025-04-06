from django.contrib import admin
from .models import Partner, Discount, Product, Order, ProductImage

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'companyName', 'partner_valid_date')
    search_fields = ('fullname', 'companyName')

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('valid_date', 'discount_percent', 'set_date', 'display_products')
    filter_horizontal = ('products',)
    date_hierarchy = 'valid_date'

    def display_products(self, obj):
        return ", ".join([product.name for product in obj.products.all()])
    display_products.short_description = "პროდუქტები"

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'code', 'storage_quantity')
    search_fields = ('name', 'code')
    readonly_fields = ('code',)
    inlines = [ProductImageInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'clients')
    search_fields = ('id', 'clients')