from django.views import generic
from django.shortcuts import render
from product.models import Variant, Product, ProductVariantPrice, ProductVariant, ProductImage
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response


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
            queryset = queryset.filter(product_variant__variant_title=variant)
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
    
class CreateProductAPI(CreateAPIView):

    def post(self, request):
        result = {}
        try:
            data = request.data
            if 'product_name' not in data or data['product_name'] == '':
                result['massage'] = "Product name can not be null."
                result['error'] = "Product Name"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'product_sku' not in data or data['product_sku'] == '':
                result['massage'] = "Product SKU can not be null."
                result['error'] = "Product SKU"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'description' not in data or data['description'] == '':
                result['massage'] = "Description can not be null."
                result['error'] = "Description"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            
            product = Product()
            
            product.title = data['product_name']
            product.sku = data['product_sku']
            product.description = data['description']
            product.save()

            productObject = Product.objects.filter(sku=data['product_sku']).first()
            
            productVarian = ProductVariant()

            
            for i in data["variant_list"]:
                
                existVariant = ProductVariant.objects.filter(variant_title=i["tagOne"][0]["variant_one"]).first()
                if not existVariant:
                    variant_option = i["tagOne"][1]["option"]
                    variant_instance = Variant.objects.filter(title=variant_option).first()
                    if variant_instance:
                        productVarian.variant = variant_instance
                        productVarian.variant_title = i["tagOne"][0]["variant_one"]
                        productVarian.product = productObject
                        productVarian.save()
                    else:
                        result['message'] = f"Variant option '{variant_option}' not found."
                        return Response(result, status=HTTP_400_BAD_REQUEST)
                    
                existVariant = ProductVariant.objects.filter(variant_title=i["tagTwo"][0]["variant_two"]).first()
                if not existVariant:
                    variant_option = i["tagTwo"][1]["option"]
                    variant_instance = Variant.objects.filter(title=variant_option).first()
                    if variant_instance:
                        productVarian.variant = variant_instance
                        productVarian.variant_title = i["tagTwo"][0]["variant_two"]
                        productVarian.product = productObject
                        productVarian.save()
                    else:
                        result['message'] = f"Variant option '{variant_option}' not found."
                        return Response(result, status=HTTP_400_BAD_REQUEST)
                    
                existVariant = ProductVariant.objects.filter(variant_title=i["tagThree"][0]["variant_three"]).first()
                if not existVariant:
                    variant_option = i["tagThree"][1]["option"]
                    variant_instance = Variant.objects.filter(title=variant_option).first()
                    if variant_instance:
                        productVarian.variant = variant_instance
                        productVarian.variant_title = i["tagThree"][0]["variant_three"]
                        productVarian.product = productObject
                        productVarian.save()
                    else:
                        result['message'] = f"Variant option '{variant_option}' not found."
                        return Response(result, status=HTTP_400_BAD_REQUEST)

            for i in data["variant_list"]:
                
                vOne = i["tagOne"][0]["variant_one"]
                vTwo = i["tagTwo"][0]["variant_two"]
                vThree = i["tagThree"][0]["variant_three"]
                price = i["price"]
                stock = i["stock"]

                pvPrice = ProductVariantPrice()
                pvPrice.product_variant_one = ProductVariant.objects.filter(variant_title=vOne).first()
                pvPrice.product_variant_two = ProductVariant.objects.filter(variant_title=vTwo).first()
                pvPrice.product_variant_three = ProductVariant.objects.filter(variant_title=vThree).first()
                pvPrice.product = productObject
                pvPrice.price = price
                pvPrice.stock = stock
                pvPrice.save()
                

            productImage = ProductImage()
            
            try:
                if 'product_image' in data:
                    if data['product_image']!='' and data['product_image']:
                        productImage.file_path = data['product_image']
                        productImage.product = productObject
                        productImage.save()
            except:
                return Response("Please prvide a valide image")
            
            result['message'] = "Product created successfully."
            return Response(result)

        except Exception as ex:
            return Response(str(ex))
        
class EditProductAPI(CreateAPIView):

    def post(self, request, sku):
        result = {}
        try:
            data = request.data
            if 'product_name' not in data or data['product_name'] == '':
                result['massage'] = "Product name can not be null."
                result['error'] = "Product Name"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'product_sku' not in data or data['product_sku'] == '':
                result['massage'] = "Product SKU can not be null."
                result['error'] = "Product SKU"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            if 'description' not in data or data['description'] == '':
                result['massage'] = "Description can not be null."
                result['error'] = "Description"
                return Response(result, status=HTTP_400_BAD_REQUEST)
            
            productObject = Product.objects.filter(sku=sku).first()
            
            productObject.title = data['product_name']
            productObject.sku = data['product_sku']
            productObject.description = data['description']
            productObject.save()
            
            productVarian = ProductVariant()
            productVariantPrice = ProductVariantPrice()
            
            for i in data["variant_list"]:
                
                existVariant = ProductVariant.objects.filter(variant_title=i["tagOne"][0]["variant_one"]).first()
                if not existVariant:
                    variant_option = i["tagOne"][1]["option"]
                    variant_instance = Variant.objects.filter(title=variant_option).first()
                    if variant_instance:
                        productVarian.variant = variant_instance
                        productVarian.variant_title = i["tagOne"][0]["variant_one"]
                        productVarian.product = productObject
                        productVarian.save()
                    else:
                        result['message'] = f"Variant option '{variant_option}' not found."
                        return Response(result, status=HTTP_400_BAD_REQUEST)
                    
                existVariant = ProductVariant.objects.filter(variant_title=i["tagTwo"][0]["variant_two"]).first()
                if not existVariant:
                    variant_option = i["tagTwo"][1]["option"]
                    variant_instance = Variant.objects.filter(title=variant_option).first()
                    if variant_instance:
                        productVarian.variant = variant_instance
                        productVarian.variant_title = i["tagTwo"][0]["variant_two"]
                        productVarian.product = productObject
                        productVarian.save()
                    else:
                        result['message'] = f"Variant option '{variant_option}' not found."
                        return Response(result, status=HTTP_400_BAD_REQUEST)
                    
                existVariant = ProductVariant.objects.filter(variant_title=i["tagThree"][0]["variant_three"]).first()
                if not existVariant:
                    variant_option = i["tagThree"][1]["option"]
                    variant_instance = Variant.objects.filter(title=variant_option).first()
                    if variant_instance:
                        productVarian.variant = variant_instance
                        productVarian.variant_title = i["tagThree"][0]["variant_three"]
                        productVarian.product = productObject
                        productVarian.save()
                    else:
                        result['message'] = f"Variant option '{variant_option}' not found."
                        return Response(result, status=HTTP_400_BAD_REQUEST)

            for i in data["variant_list"]:
                
                vOne = i["tagOne"][0]["variant_one"]
                vTwo = i["tagTwo"][0]["variant_two"]
                vThree = i["tagThree"][0]["variant_three"]
                price = i["price"]
                stock = i["stock"]

                pvPrice = ProductVariantPrice()
                pvPrice.product_variant_one = ProductVariant.objects.filter(variant_title=vOne).first()
                pvPrice.product_variant_two = ProductVariant.objects.filter(variant_title=vTwo).first()
                pvPrice.product_variant_three = ProductVariant.objects.filter(variant_title=vThree).first()
                pvPrice.product = productObject
                pvPrice.price = price
                pvPrice.stock = stock
                pvPrice.save()
                
            productImage = ProductImage()
            
            try:
                if 'product_image' in data:
                    if data['product_image']!='' and data['product_image']:
                        productImage.file_path = data['product_image']
                        productImage.product = productObject
                        productImage.save()
            except:
                return Response("Please prvide a valide image")
            
            result['message'] = "Product created successfully."
            return Response(result)

        except Exception as ex:
            return Response(str(ex))