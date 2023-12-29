from django.views import generic
from django.shortcuts import render
from product.models import Variant, Product, ProductVariantPrice, ProductVariant
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    
    
class ProductListView(generic.TemplateView):
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        title = self.request.GET.get('title')
        variant = self.request.GET.get('variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')

        variant_name = Variant.objects.all()
        variant_title_list = []

        for vn in variant_name:
            product_variants = ProductVariant.objects.filter(variant__title=vn.title).values_list('variant_title', flat=True).distinct()
            variant_title_list.append({'variant_name': vn, 'product_variants': product_variants})

        variants = ProductVariantPrice.objects.all()
        queryset = Product.objects.prefetch_related("product_variant_price").all()

        if title:
            queryset = queryset.filter(title__icontains=title)
        if variant:
            print(variant)
            # queryset = queryset.filter(product_variant_price__variant__title=variant)
        if price_from and price_to:
            queryset = queryset.filter(product_variant_price__price__range=(price_from, price_to))
        if date:
            queryset = queryset.filter(created_at__date=date)

        context['variant_name'] = variant_name
        context['variant_title_list'] = variant_title_list
        context['variant'] = variants
        context['product'] = queryset
        context['product_count'] = queryset.count()

        return context