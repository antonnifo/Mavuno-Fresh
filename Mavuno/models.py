from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from hitcount.models import HitCount
from taggit.managers import TaggableManager



class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager,
                     self).get_queryset().filter(available=True)

class BaseContent(models.Model):
  
    publish  = models.DateTimeField(default=timezone.now)            
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    
    class Meta:
        abstract = True

class Category(BaseContent):
        name = models.CharField(max_length=200)
        slug = models.SlugField(max_length=200,
                    unique=True)
                   
        class Meta:
            ordering = ('updated',)
            verbose_name = 'category'
            verbose_name_plural = 'categories'

        def __str__(self):
            return self.name

        def get_absolute_url(self):
            return reverse('mavuno:product_list_by_category',
               args=[self.slug])


class Product(BaseContent):
    
    objects = models.Manager() # The default manager.
    is_available   = AvailableManager()
    tags = TaggableManager()

    category    = models.ForeignKey(Category,
                    related_name='products',
                            on_delete=models.CASCADE)
    name        = models.CharField(max_length=200, db_index=True)
    slug        = models.SlugField(max_length=200, db_index=True)
    image       = models.ImageField(upload_to='products/%Y/%m/%d',
                                 blank=True)
    seller      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_products')  
    phone       = models.CharField(max_length=200, db_index=True)                           
    description = RichTextUploadingField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    location    = models.CharField(max_length=200, db_index=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                    related_query_name='hit_count_generic_relation')
    available   = models.BooleanField(default=True)

    
    class Meta:
        index_together = (('id', 'slug'),)
    
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mavuno:product_detail',
               args=[self.id, self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    image   = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        verbose_name        = 'Product_image'
        verbose_name_plural = 'Product_images'

    def __str__(self):
        return self.product.name