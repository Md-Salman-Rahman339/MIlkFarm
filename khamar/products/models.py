from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    Name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True,null=True,blank=True)

    def __str__(self):
        return self.Name

class Product(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='products/media/uploads',blank=True,null=True)
    buying_price=models.DecimalField(max_length=100,decimal_places=2,max_digits=12)
    category=models.OneToOneField(Category,on_delete=models.CASCADE)
    buyer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    id = models.AutoField(primary_key=True)


    def __str__(self):
        return self.title

class Review(models.Model):
    product=models.ForeignKey(Product,related_name='comments',on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField()

    def __str__(self):
        return f"comments by {self.user.username}"

    

class BuyProduct(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return f"Buy this: {self.product.title}"






