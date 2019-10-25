import json
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from goods.models import Goods
from django.core import serializers

__author__ = 'litl'


class GoodsListView(View):
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()
        for good in goods:
            # json_dict = {}
            # json_dict['name'] = good.name
            # json_dict['category'] = good.category.name
            # json_dict['market_price'] = good.market_price
            # json_list.append(json_dict)
            # return HttpResponse(json.dumps(json_list), content_type='application/json')
            json_data = serializers.serialize('json', goods)
            json_data = json.loads(json_data)
            return JsonResponse(json_data, safe=False)