from email.mime import image
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, null=True) 
    slug = models.SlugField(max_length=200,unique=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shops:category_list', args=[self.slug])



class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True,blank=True)
    slug = models.SlugField(max_length=200,unique=True,null=True)
    description = models.TextField(blank=True)



    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        
        return url
    
    def get_absolute_url(self):
        return reverse('shops:product_detail', args=[self.slug])


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.order_id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])

        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    
class Comment(models.Model):
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    commenter_name = models.CharField(max_length=200)
    comment_body = models.TextField(max_length=350)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.product.name, self.commenter_name)
