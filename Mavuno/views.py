
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from .models import Category, Product, ProductImage

PRODUCTS = Product.is_available.all()
CATEGORIES = Category.objects.all()


def product_list(request, product_id=None,category_name=None,category_slug=None):
 
    def get_category(name):
        return Category.objects.filter(name=name)

    products = PRODUCTS

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    category_name = None
    if category_name:
        category = get_object_or_404(Category, name=category_name)
        products = products.filter(category=category)

    paginator = Paginator(products, 12)
    page = request.GET.get('page')

    
    try:
        products = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        products = paginator.page(1)

    except EmptyPage:
        # If page is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)

    return render(request,
          'all-classifieds.html',
                    {
                        "page": page,
                        "products" : products,
                        "category" : category,
                        "category_name":category_name,
                        "product_id" : product_id,
                        "categories": CATEGORIES

                    })

def product_detail(request, id, slug):

    product = get_object_or_404(Product,
                            id=id,
                            slug=slug,
                            available=True)

    return render(request,
              'single.html',
              {
                  'product': product, 
                  'product_images': ProductImage.objects.filter(product=product)[:5],
            
              }) 