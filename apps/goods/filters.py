from django.db.models import Q
from goods.models import Goods

__author__ = 'litl'
import django_filters


class GoodsFilter(django_filters.rest_framework.FilterSet):
    pricemin = django_filters.NumberFilter(name="shop_price", lookup_expr="gte")
    pricemax = django_filters.NumberFilter(name="shop_price", lookup_expr="lte")
    top_category = django_filters.NumberFilter(name="category", method='top_category_filter')
    # name = django_filters.CharFilter(name="name", lookup_expr="icontains")

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']