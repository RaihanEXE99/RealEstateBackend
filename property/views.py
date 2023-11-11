from django.shortcuts import render
from django.http import JsonResponse
import json
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny import math
=======

from .serializer import AddressSerializer, PropertyDetailsSerializer,PropertySerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Property, Address, PropertyDetails

from rest_framework.views import APIView

<<<<<<< HEAD
import math
=======

from .serializer import AddressSerializer, PropertyDetailsSerializer,PropertySerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Property, Address, PropertyDetails

from rest_framework.views import APIView
>>>>>>> 79bfe526891b114ccd47ce69edfe4de5a8230aa2
# Create your views here.


def prop_search(request, *args, **kwargs):
    if request.method == "GET":
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')

        lat_min = lat - 0.090
        lat_max = lat + 0.090
        lng_min = lng - (0.045 / math.cos(lat*math.pi/180))
        lng_max = lng + (0.045 / math.cos(lat*math.pi/180))

        properties = Property.objects.filter(lat__gte=lat_min, lat__lte=lat_max, long__gte=lng_min, long__lte=lng_max)

        titles = [property.title for property in properties]

        data = {
            'titles': titles
        }

        return JsonResponse(data)

@api_view(['GET'])
@permission_classes([AllowAny]) # Any user can view (FOR PUBLIC URLS)
def all_properties(request, *args, **kwargs):
    properties = Property.objects.all()
    titles = [property.title for property in properties]

    data = {
        'titles': titles
    }

    return JsonResponse(data)
    
@api_view(['GET'])
@permission_classes([AllowAny]) # Any user can view (FOR PUBLIC URLS)
def property(request, sku):
    # sku = request.GET.get('sku')
    data = {}
    try:
        print('Try running')
        p = Property.objects.all().first()
        print(p)
    except:
        print('ex running')
        p = None

    if p:
        data = model_to_dict(p)
        data['thumbnail'] = data['thumbnail'].url
        data['address'] = model_to_dict(p.address)
        data['details'] = model_to_dict(p.details)
        print(data)

        # Image field files cannot be shown as a JSON response
        return Response(data) #Temporary Check
    
    else:

        return Response({'error': 'Property Not Found!'}, status="404")
    

class PropertyCreateView(APIView):
    def post(self, request, format=None):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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