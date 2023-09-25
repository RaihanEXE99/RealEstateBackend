from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
# Create your views here.

@api_view(['GET'])
def property(request, *args, **kwargs):
    sku = request.GET.get('sku')
    try:
        p = Property.objects.get(sku=sku)
    except:
        p = None

    if p:
        imgs = Image.objects.filter(property=p)

        try:
            vid = Video.objects.get(property=p)
        except:
            vid = None

        data = {
            'title': p.title,
            'desc': p.desc,
            'price': p.price,
            'price_unit': p.price_unit,
            'pricetype': p.price_type,
            'thumbnail': p.thumbnail,
            'post_type': p.post_type,
            'pcat': p.property_category,
            'loc': p.loc,
            'lat': p.lat,
            'long': p.long,
            'pdate': p.date,
            'house': p.address.house,
            'street': p.address.street,
            'area': p.address.area,
            'city': p.address.city,
            'state': p.address.state,
            'country': p.address.country,
            'zip': p.address.zip,
            'size': p.details.size,
            'size_unit': p.details.size,
            'lot_size': p.details.lot_size,
            'rooms': p.details.rooms,
            'bed': p.details.bed,
            'bath': p.details.bath,
            'floor': p.details.floor,
            'roofing': p.details.roofing,
            'structure': p.details.structure,
            'hide_contact': p.hide_contact,

        }

        data['images'] = list()

        if imgs:
            for i in imgs:
                data['images'].append(i.image)
        
        if vid:
            data['video'] = vid

        return Response(data)
    
    else:

        return Response({'error': 'Property Not Found!'}, status="404")