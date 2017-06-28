from __future__ import unicode_literals
from django.db import models
from ..bestLogin.models import User
from PIL import Image
from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor


class ProductManager(models.Manager):
    def addNewLike(self, likeId, userId):
        selected_user = User.userManager.get(id=userId)
        like = self.get(id=likeId)
        like.likes.add(selected_user)
        like.save()

    def addProductToCart(self, productId, userId):
        selected_user = User.userManager.get(id=userId)
        item = self.get(id=productId)
        item.add.add(selected_user)
        item.save()

class Product(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    likes = models.ManyToManyField(User, related_name="users_likes")
    add = models.ManyToManyField(User, related_name="users_cart")
    #model_pic = models.ImageField(upload_to = 'imageApp/images/products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model_pic = fields.ImageField(upload_to='imageApp/images/products/', dependencies=[
        FileDependency(attname='model_jpeg', processor=ImageProcessor(
            format='JPEG', scale={'max_width': 400, 'max_height': 400})),
    ])
    model_jpeg = fields.ImageField(upload_to='imageApp/images/products/')

    pManager = ProductManager()


class Review(models.Model):
    content = models.TextField()
    rating = models.CharField(max_length=200)
    avg_rating = models.ManyToManyField(User, related_name="users_ratings")
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)









# Product
# - name
# - code
# - description
# - price
# - likes
# - stock (items left)
#
# Cart
# - total
# - items (list) (Product)
#
# OrderDetails
# - orderId
# - Date
# - billing address
# - shipping address
#


    # def save(self, *args, **kwargs):
    #     if self.model_pic:
    #         self.model_pic = get_thumbnail(self.model_pic, '400x400', quality=99, format='JPEG')
    #     super(Product, self).save(*args, **kwargs)


    # def save(self, force_insert=True, force_update=True, using=None):
    #
    #     if not self.id and not self.model_pic:
    #         return
    #
    #     super(Product, self)
    #
    #     image = Image.open(self.model_pic)
    #
    #     size = ( 400, 400)
    #     image.resize(size, Image.ANTIALIAS)
    #     image.save(self.model_pic.path)
