from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null = True, related_name='+')#+ tells django to not create the reverse relation -> use to prevent circular relations causing error due to same name -> if reverse relation is important give it a related_name to prevenyt name clash
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()#write default value or make it nullable # we used method1 and thus default value '-' directly in migration file and not in our model # letters hyphen underscore and numbers allowed
    description = models.TextField(null = True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
        # validators=[MinValueValidator(1,message=)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)#if parent class written after child class -> 'Collection' <- use like this
    # promotion = models.ManyToManyField(Promotion, related_name='products')#related name -> name in Promotion class(reverse relation) by default product_set
    promotion = models.ManyToManyField(Promotion,blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    class Meta:
        ordering = ['first_name','last_name']
    # class Meta:
    #     # db_table = 'store_customers' #not preferred as by default singular
    #     indexes = [
    #         models.Index(fields=['last_name' , 'first_name'])
    #     ]

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING,'PENDING'),
        (PAYMENT_STATUS_COMPLETE,'COMPLETE'),
        (PAYMENT_STATUS_FAILED, "FAILED")
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=6 , default='201013')
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)#CASCASE/PROTECT/SET_NULL/SET_DEFAULT
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)#CASCASE/PROTECT/SET_NULL/SET_DEFAULT #one to many relationship

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

