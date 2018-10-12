from rest_framework import serializers
from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import AutoSlugField

# Create your models here. 
ACTIVE = 'ACTIVE'
PAUSED = 'PAUSED'
PENDING = 'PENDING_EMAIL_VALIDATION'
SUSPENDED = 'SUSPENDED'
PROFILE_STATUS = (
    (ACTIVE, 'Active'),
    (PAUSED, 'Paused'),
    (SUSPENDED, 'Suspended'),
    (PENDING, 'PENDING_EMAIL_VALIDATION'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    picture = models.URLField(blank=True)
    bio = models.TextField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=17, blank=True) # validators should be a list
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    img = models.CharField(max_length=150, default="")
    title = models.CharField(max_length=50, default="")
    description = models.TextField(max_length=1000, default="")
    productRating = models.IntegerField(default=0, blank=True)
    manufacturer = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0, blank=True)
    quantity = models.IntegerField(default=0, blank=True)
    slug = AutoSlugField(null=True, default=None, unique=True, populate_from='name')
#dont need a product category bc its an intermediate model, because it is so common, Django 
#already does it for you, automatically because there are two foreign keys.

#model, extends from Model 
class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    description = models.TextField(max_length=1000, default="")
    slug = models.SlugField(max_length=150, unique=True ,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #this is how the category relates to product, products is the name of the variable
    products = models.ManyToManyField(Product, related_name='categories', blank=True)   
    
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    url = models.CharField(max_length=150, default="")
    comment = models.CharField(max_length=200, default="")

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True)
    rating_int = models.IntegerField(default=0, blank=True)
    comment = models.CharField(max_length=200, default="")

class Shoppingcart(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank=True)
    quantity = models.IntegerField(default=0, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tracking = models.CharField(max_length=150, default="")

class Special(models.Model):
    expiration = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True)
    percentage = models.DecimalField(
        max_digits=2, decimal_places=1, default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Coupon(models.Model):
    expiration = models.DateTimeField(auto_now_add=True)
    usage_count = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Purchase(models.Model):
    date = models.DateTimeField(auto_now_add=True) 

class Transaction(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True)
    special = models.ForeignKey(
        Special, on_delete=models.CASCADE, blank=True)
    shoppingcart = models.ForeignKey(
        Shoppingcart, on_delete=models.CASCADE, blank=True)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, blank=True)

        
class Search(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True)
    searchTerm = models.CharField(max_length=50, default="")
    
class Profile(models.Model):
    product = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'img','title','description', 'productRating', 'manufacturer', 'price', 'quantity', 'slug')
       
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'products', 'slug', 'description')
        
class ShoppingcartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoppingcart
        exclude = ()

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ()
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'comment', 'product', 'url')

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('date', 'id')
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ()

class SpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Special
        exclude = ()

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('expiration', 'usage_count','created_at', 'updated_at', 'id')
         

 
 

