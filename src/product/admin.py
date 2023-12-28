from django.contrib import admin
from .models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice

class VariantAdmin(admin.ModelAdmin):
    
    fields = [
        "title",
        "description",
        "active"
    ]
admin.site.register(Variant, VariantAdmin)

class ProductAdmin(admin.ModelAdmin):
    
    fields = [
        "title",
        "sku",
        "description",
        "created_at",
        "updated_at"
    ]
    
    readonly_fields = [
        "created_at",
        "updated_at"
    ]
    
admin.site.register(Product, ProductAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    
    fields = [
        "product",
        "file_path"
    ]
admin.site.register(ProductImage, ProductImageAdmin)

class ProductVariantAdmin(admin.ModelAdmin):
    
    fields = [
        "variant_title",
        "variant",
        "product"
    ]
admin.site.register(ProductVariant, ProductVariantAdmin)
class ProductVariantPriceAdmin(admin.ModelAdmin):
    
    fields = [
        "product_variant_one",
        "product_variant_two",
        "product_variant_three",
        "price",
        "stock",
        "product",
    ]
admin.site.register(ProductVariantPrice, ProductVariantPriceAdmin)
