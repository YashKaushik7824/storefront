from django.contrib import admin,messages
from django.db.models import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse
from . import models

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<100','Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<100':
            return queryset.filter(inventory__lt=100)





@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    autocomplete_fields = ['collection']
    search_fields = ['title']

    prepopulated_fields = {
        'slug': ['title']
    }

    actions = ['clear_inventory']
    # fields = ['title','slug']
    # exclude = ['promotion']
    # readonly_fields = ['title']

    list_display = ['title','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection','last_update',InventoryFilter]

    def collection_title(self,product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory <100:
            return 'Low'
        return 'OK'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{updated_count} products are successfully updated',
            messages.ERROR
        )

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0
# class OrderItemInline(admin.StackedInline):
#     autocomplete_fields = ['product']
#     min_num = 1
#     max_num = 10
#     model = models.OrderItem
#     extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id','placed_at','customer']

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership','orders']
    list_editable=['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='order_count')
    def orders(self, customer):
        # reverse('admin:app_model_page')
        url = (reverse('admin:store_order_changelist') 
               + '?'
               + urlencode({
                   'customer__id': str(customer.id)
               }))
        return format_html('<a href="{}">{} Order</a>',url,customer.order_count)
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count = Count('order')
        )

# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # reverse('admin:app_model_page')
        url = (reverse('admin:store_product_changelist') 
               + '?'
               + urlencode({
                   'collection__id': str(collection.id)
               }))
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
        
    
   
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )

# admin.site.register(models.Product,ProductAdmin)