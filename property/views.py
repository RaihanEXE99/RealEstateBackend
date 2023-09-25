from django.shortcuts import render
from django.http import JsonResponse
import json
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny 
# Create your views here.

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
        print(data)

        # Image field files cannot be shown as a JSON response
        return Response(data) #Temporary Check
    
    else:

        return Response({'error': 'Property Not Found!'}, status="404")
    

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