from django.shortcuts import render
from django.http import JsonResponse
import json
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core import serializers
from .serializer import AddressSerializer, PropertyDetailsSerializer,PropertySerializer,PropertySerializerAll
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Property, Address, PropertyDetails
from django.core.serializers import serialize
from rest_framework import serializers
from rest_framework.views import APIView
import math
# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def ploygon_s(request, *args, **kwargs):
    if request.method == "GET":
        minlat = request.GET.get('minlat')
        maxlat = request.GET.get('maxlat')
        minlng = request.GET.get('minlong')
        maxlng = request.GET.get('maxlong')
        tp = request.GET.get('type')
        cat = request.GET.get('category')

        properties = Property.objects.filter(post_type=tp, property_category=cat, lat__gte=minlat, lat__lte=maxlat, long__gte=minlng, long__lte=maxlng)

        property_serializer = PropertySerializerAll(properties, many=True)

        return JsonResponse(property_serializer.data, safe=False)
@api_view(['GET'])
@permission_classes([AllowAny])
def prop_search(request, *args, **kwargs):
    if request.method == "GET":
        lat = request.GET.get('lat')
        lng = request.GET.get('long')
        loc = request.GET.get('location')
        tp = request.GET.get('type')
        cat = request.GET.get('category')
        rad = request.GET.get('radius')
        rad = float(rad if rad!=None else 5.00)
        lat = float(lat)
        lng = float(lng)

        lat_min = lat - (0.009 * rad)
        lat_max = lat + (0.009 * rad)
        lng_min = lng - (((0.009 * rad) / 2) / math.cos(lat*math.pi/180))
        lng_max = lng + (((0.009 * rad) / 2) / math.cos(lat*math.pi/180))

        properties = Property.objects.filter(post_type=tp, property_category=cat, lat__gte=lat_min, lat__lte=lat_max, long__gte=lng_min, long__lte=lng_max)

        property_serializer = PropertySerializerAll(properties, many=True)

        return JsonResponse(property_serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny]) # Any user can view (FOR PUBLIC URLS)
def all_properties(request, *args, **kwargs):
    properties = Property.objects.all()
    
    property_serializer = PropertySerializerAll(properties, many=True)

    return JsonResponse(property_serializer.data, safe=False)


@permission_classes([AllowAny]) # Any user can view (FOR PUBLIC URLS)
def homeProp(request, *args, **kwargs):
    properties = Property.objects.all()[:9]
    property_serializer = PropertySerializerAll(properties, many=True)
    return JsonResponse(property_serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny]) # Any user can view (FOR PUBLIC URLS)
def property(request, sku):
    if request.method == "GET":
        sku = request.GET.get('sku')

        property = Property.objects.get(sku=sku)

        property_serializer = PropertySerializerAll(property, many=True)
        return JsonResponse(property_serializer.data, safe=False)

    

class PropertyCreateView(APIView):
    def post(self, request, format=None):
        request.data['address']=json.loads(request.data['address'])
        request.data['details']=json.loads(request.data['details'])
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, format=None):
    #     # Extract data from the request
    #     property_data = request.data
    #     address_data = property_data.pop('address', None)
    #     details_data = property_data.pop('details', None)

    #     # Create Address instance
    #     address_instance = Address.objects.create(**address_data) if address_data else None

    #     # Create PropertyDetails instance
    #     details_instance = PropertyDetails.objects.create(**details_data) if details_data else None

    #     # Create Property instance
    #     property_instance = Property.objects.create(address=address_instance, details=details_instance, **property_data)

    #     return Response({"sku": str(property_instance.sku)}, status=status.HTTP_201_CREATED)
    # def post(self, request, format=None):
    #     print("hellooooooo"*100)
    #     # Extract data from the request
    #     property_data = request.data
    #     request.data['address'] = json.loads(request.data['address'])
    #     request.data['detail'] = json.loads(request.data['detail'])
    #     address_data = property_data.get('address', None)
    #     details_data = property_data.pop('detail', None)

    #     # Create Address instance if data is present
    #     print(property_data)
    #     print(address_data)
    #     # print(request.POST['address[house]'])
    #     if address_data:
    #         address_instance = Address.objects.create(
    #             house=address_data.get('house'),
    #             street=address_data.get('street'),
    #             city=address_data.get('city'),
    #             state=address_data.get('state'),
    #             country=address_data.get('country'),
    #             zip=address_data.get('zip')
    #         )
    #     else:
    #         address_instance = None

    #     # Create PropertyDetails instance if data is present
    #     if details_data:
    #         details_instance = PropertyDetails.objects.create(
    #             cid=details_data.get('cid'),
    #             size_unit=details_data.get('size_unit'),
    #             size=details_data.get('size'),
    #             rooms=details_data.get('rooms'),
    #             bed=details_data.get('bed'),
    #             bath=details_data.get('bath'),
    #             floor=details_data.get('floor'),
    #             built=details_data.get('built'),
    #             structure=details_data.get('structure'),
    #             garage=details_data.get('garage'),
    #             garage_size=details_data.get('garage_size'),
    #             available_from=details_data.get('available_from')
    #         )
    #     else:
    #         details_instance = None

    #     # Create Property instance
    #     property_instance = Property.objects.create(
    #         sku=property_data.get('sku'),
    #         user_id=property_data.get('user'),  # Assuming user_id is provided in request data
    #         title=property_data.get('title'),
    #         price=property_data.get('price'),
    #         price_unit=property_data.get('price_unit'),
    #         price_type=property_data.get('price_type'),
    #         thumbnail=property_data.get('thumbnail'),
    #         property_category=property_data.get('property_category'),
    #         property_status=property_data.get('property_status'),
    #         post_type=property_data.get('post_type'),
    #         loc=property_data.get('loc'),
    #         lat=property_data.get('lat'),
    #         long=property_data.get('long'),
    #         desc=property_data.get('desc'),
    #         address=address_instance,
    #         details=details_instance,
    #         hide_contact=property_data.get('hide_contact')
    #     )
    #     return Response({"status":"Done!"},status=status.HTTP_201_CREATED)
    #     return Response({"sku": str(property_instance.sku)}, status=status.HTTP_201_CREATED)
    
# @api_view(['GET'])
# def property(request, *args, **kwargs):
#     sku = request.GET.get('sku')
#     data = {}
#     try:
#         p = Property.objects.all().first()
#     except:
#         p = None

#     if p:
#         # imgs = Image.objects.filter(property=p)

#         # try:
#         #     vid = Video.objects.get(property=p)
#         # except:
#         #     vid = None

#         # data = {
#         #     'title': p.title,
#         #     'desc': p.desc,
#         #     'price': p.price,
#         #     'price_unit': p.price_unit,
#         #     'pricetype': p.price_type,
#         #     'thumbnail': p.thumbnail,
#         #     'post_type': p.post_type,
#         #     'pcat': p.property_category,
#         #     'loc': p.loc,
#         #     'lat': p.lat,
#         #     'long': p.long,
#         #     'pdate': p.date,
#         #     'house': p.address.house,
#         #     'street': p.address.street,
#         #     'area': p.address.area,
#         #     'city': p.address.city,
#         #     'state': p.address.state,
#         #     'country': p.address.country,
#         #     'zip': p.address.zip,
#         #     'size': p.details.size,
#         #     'size_unit': p.details.size,
#         #     'lot_size': p.details.lot_size,
#         #     'rooms': p.details.rooms,
#         #     'bed': p.details.bed,
#         #     'bath': p.details.bath,
#         #     'floor': p.details.floor,
#         #     'roofing': p.details.roofing,
#         #     'structure': p.details.structure,
#         #     'hide_contact': p.hide_contact,

#         # }

#         # data['images'] = list()

#         # if imgs:
#         #     for i in imgs:
#         #         data['images'].append(i.image)
        
#         # if vid:
#         #     data['video'] = vid

#         data = model_to_dict(p)
#         print(data)

#         return JsonResponse(data)
    
#     else:

#         return Response({'error': 'Property Not Found!'}, status="404")