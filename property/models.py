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
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.CharField(max_length=20)
    

class PropertyDetails(models.Model):
    cid = models.CharField(max_length=50)
    size_unit = models.CharField(max_length=20)
    size = models.FloatField()
    rooms = models.IntegerField()
    bed = models.IntegerField()
    bath = models.IntegerField()
    floor = models.IntegerField()
    built = models.IntegerField(null=True)
    structure = models.CharField(max_length=100)
    garage = models.CharField(max_length=10, choices=hc_choice, default=2)
    garage_size = models.FloatField(null=True)
    available_from = models.DateField(null=True)

class Image(models.Model):
    image = models.ImageField(upload_to='pimages/')

class Video(models.Model):
    video = models.ImageField(upload_to='pvideo/')

class Property(models.Model):
    sku = models.UUIDField(max_length=100, blank=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    price = models.FloatField()
    price_unit = models.CharField(max_length=50)
    price_type = models.CharField(max_length=30)
    thumbnail = models.ImageField(upload_to='thumbnail/')
    property_category = models.CharField(max_length=50)
    property_status = models.CharField(max_length=50, null=True)
    post_type = models.CharField(max_length=100)
    loc = models.CharField(max_length=500)
    lat = models.FloatField(max_length=100)
    long = models.FloatField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    desc = models.TextField(max_length=5000)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    details = models.ForeignKey(PropertyDetails, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image)
    video = models.OneToOneField(Video, on_delete=models.CASCADE, null=True)
    hide_contact = models.CharField(max_length=10, choices=hc_choice, default=1)
    images = models.ManyToManyField(Image,blank=True,default=None)
    video = models.OneToOneField(Video, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.sku)