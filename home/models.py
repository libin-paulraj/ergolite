from django.db import models
from django.contrib.auth.models import User


CHAIR_CATEGORIES = [("Most populer","MostPopuler"),
                    ("HOMETOP", "Home top"),("HOMEBOTTOM", "Home bottom"),("OFFICECHAIRS","Office chairs"),
                    ("INTERIOR"," interior"),("DIRECTORCHAIR","director_chair"),("PREMIUM","Premium_chair"),
                    ("WORKFORCE","Workforce_chair"),("LOUNGE","Lounge_chair"),("VISITOR","Visitor_chair"),("CAFETERIA","Cafeteria_chair")]

class Chairs(models.Model):
    image = models.ImageField(upload_to="chairs", height_field=None, width_field=None, max_length=None)
    name = models.CharField(max_length=500)
    description = models.TextField()
    price = models.IntegerField()
    # discount = models.IntegerField() 
    category = models.CharField(max_length=50, choices=CHAIR_CATEGORIES )
    order = models.IntegerField()
    

    def __str__(self):
        return f"{self.name} - {self.category}"

    class Meta:
        ordering = ['category', 'order']
       
class Usermodel(models.Model):

    username=models.CharField(max_length=150)
    password=models.CharField(max_length=150)
    phonenumber=models.CharField( max_length=50)

    def __str__(self):
        return f"{self.username}"

class CartModel(models.Model):
    user = models.ForeignKey(Usermodel, on_delete=models.CASCADE)
    cart = models.ForeignKey(Chairs, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.cart.name}"

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='products/')

#     def __str__(self):
#         return self.name    