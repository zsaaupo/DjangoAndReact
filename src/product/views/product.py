from django.views import generic
from django.shortcuts import render
from product.models import Variant, Product


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
        
        product_count = Product.objects.count()
        
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.prefetch_related("product_variant_price").all()
        context['product_count'] = product_count
        
        return context