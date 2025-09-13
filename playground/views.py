from django.shortcuts import render
from django.db.models import Q, F, Value, Func, ExpressionWrapper,DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggedItem



# Create your views here.
def say_hello(request):

    # query_set = Product.objects.all() #all get filter #returns queryset object #manager object -> interface to database
    # all => returns all , get(lookout parameter) lookout paramm -> id but use pk instead -> pk represent primary key -> returns object instead of query_set
    #cases where query_set is evaluated by django
    # for product in query_set:
    #     print(product)
    # list(query_set)
    # query_set[0]
    # query_set[0:5]
    #thus called lazy -> called when evaluated -> useful to create complex queries
    # query_set.filter().filter().order_by()
    # product = Product.objects.get(pk=1)
    # try:
    #     product = Product.objects.get(pk=1)
    # except ObjectDoesNotExist:
    #     pass
    # product = Product.objects.filter(pk=1).first() #returns none instead of exception -> try catch alternative
    # exists = Product.objects.filter(pk=1).exists() #boolean obj
    # queryset = Product.objects.filter(unit_price = 20)
    # queryset = Product.objects.filter(unit_price__gt= 20) #gt > lt < gte >= lte <= -> lookups
    # queryset = Product.objects.filter(unit_price__range = (20,30))
    # queryset = Product.objects.filter(collection__id = 1)
    # queryset = Product.objects.filter(title__contains='mix') #startswith endswith istartswith iendswith
    # queryset = Product.objects.filter(title__icontains='mix') #case insensitive 
    # queryset = Product.objects.filter(last_update__year = 2024) #case insensitive 
    # queryset = Product.objects.filter(description__isnull = False)

    #products : inventory<90 and price <20
    #way1
    # queryset = Product.objects.filter(inventory__lt=90, unit_price__lt=20)
    #way2
    # queryset = Product.objects.filter(inventory__lt=90).filter(unit_price__lt=20)
    #products : inventory<90 or price <20
    # queryset = Product.objects.filter(Q(inverntory__lt=10) | Q(unit_price__lt=20))#Q objects help using bitwise operations
    # queryset = Product.objects.filter(inventory = F('unit_price'))
    # queryset = Product.objects.filter(inventory = F('collection_id'))
    # queryset = Product.objects.order_by('title')
    # queryset = Product.objects.order_by('-title')
    # queryset = Product.objects.order_by('unit_price','-title')
    # queryset = Product.objects.order_by('unit_price','-title').reverse()
    # queryset = Product.objects.filter(collection_id = 1).order_by('unit_price')
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price')
    # product = Product.objects.latest('unit_price')
    # queryset = Product.objects.all()[:5]#limit =5
    # queryset = Product.objects.all()[5:10]#offset =5 limit =5
    # queryset = Product.objects.values('id','title','collection__title')#dictionary
    # queryset = Product.objects.values_list('id','title','collection__title')#tuple
    # queryset = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    # queryset = Product.objects.only('id','title')# dont use -> endup with unnecessary queries
    # queryset = Product.objects.defer('description')
    # queryset = Product.objects.all()# causes extra reload while calling related columns
    # queryset = Product.objects.select_related('collection').all()
    # queryset = Product.objects.select_related('collection__nameofanotherrelatedfield').all()
    # queryset = Product.objects.prefetch_related('promotion').all()
    # queryset = Product.objects.prefetch_related('promotion').select_related('collection').all()
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # result = Product.objects.aggregate(Count('id'))
    # result = Product.objects.aggregate(count = Count('id'), min_price = Min('unit_price'))
    # result = Product.objects.filter(collection__id = 1).aggregate(count = Count('id'), min_price = Min('unit_price'))
    # queryset = Customer.objects.annotate(is_new = Value(True))
    # queryset = Customer.objects.annotate(new_id = F('id') + 1)
    # queryset = Customer.objects.annotate(
    #     full_name = Func(F('first_name'),Value(' '), F('last_name'), function='CONCAT')
    # )
    # queryset = Customer.objects.annotate(
    #     full_name = Concat('first_name', Value(' ') , 'last_name')
    # )
    # queryset = Customer.objects.annotate(
    #     orders_count = Count('order')
    # )
    # discounted_price=ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(
       
    #     discounted_price = discounted_price
    # )
    #select_related(1) -> collection 
    #prefetch_related(m) -> promotions

    # content_type = ContentType.objects.get_for_model(Product)

    # query_set = TaggedItem.objects\
    #     .select_related('tag')\
    #     .filter(
    #         content_type = content_type,
    #         object_id = 1
    #     )

    # query_set = TaggedItem.objects.get_tags_for(Product,1)

    # collection = Collection(title='') # dont use 
    # collection = Collection()
    # collection.title = 'Video Games'
    # # collection.featured_product = Product(id=1)
    # collection.featured_product = Product(pk=1)
    # # collection.featured_product_id = 1
    # collection.save()
    # collection = Collection(pk = 103)
    # collection.title = 'Games'
    # collection.featured_product = None
    # collection.save()
    # collection = Collection.objects.get(pk = 103)
    # collection.featured_product = None
    # collection.save()
    # Collection.objects.update(featured_product=None)
    # Collection.objects.filter(pk=103).update(featured_product=None)
    # Collection.objects.filter(id__gt=5).delete()
    # collection = Collection(pk=103)
    # collection.delete()

    


    # collection = Collection.objects.create(title = 'a', featured_product_id = 1)


    return render(request, 'hello.html', {'name':'Yash'})
    # return render(request, 'hello.html', {'name':'Yash', 'tags' : list(query_set)})
    # return render(request, 'hello.html', {'name':'Yash', 'result' : list(queryset)})
    # return render(request, 'hello.html', {'name':'Yash', 'result' : result})
    # return render(request, 'hello.html', {'name':'Yash', 'orders':list(queryset)})
    # return render(request, 'hello.html', {'name':'Yash', 'products':list(queryset)})
    # return render(request, 'hello.html', {'name':'Yash', 'product':product})