from django.db import models
from users.models import UserAccount
import uuid

hc_choice=(
    ('1','No'),
    ('2','Yes')
) 

# Create your models here.
class Address(models.Model):
    house = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.CharField(max_length=20)
    

class PropertyDetails(models.Model):
    cid = models.CharField(max_length=50)
    size = models.FloatField()
    size_unit = models.CharField(max_length=20)
    lot_size = models.FloatField()
    rooms = models.IntegerField()
    bed = models.IntegerField()
    bath = models.IntegerField()
    floor = models.IntegerField()
    roofing = models.CharField(max_length=100)
    structure = models.CharField(max_length=100)

class Property(models.Model):
    sku = models.UUIDField(max_length=100, blank=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    price = models.FloatField()
    price_unit = models.CharField(max_length=50)
    price_type = models.CharField(max_length=30)
    thumbnail = models.ImageField(upload_to='thumbnail/')
    property_category = models.CharField(max_length=50)
    post_type = models.CharField(max_length=100)
    loc = models.CharField(max_length=500)
    lat = models.CharField(max_length=100)
    long = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    desc = models.TextField(max_length=5000)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    details = models.ForeignKey(PropertyDetails, on_delete=models.CASCADE)
    hide_contact = models.CharField(max_length=10, choices=hc_choice, default=1)

    def __str__(self):
        return self.sku


class Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pimages/')

class Video(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    video = models.ImageField(upload_to='pvideo/')