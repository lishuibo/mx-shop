"""mxshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
# from goods.views import GoodsListView
from rest_framework_jwt.views import obtain_jwt_token
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, IndexCategoryViewSet
from mxshop.settings import MEDIA_ROOT
from trade.views import ShopCartViewSet, OrderViewSet, AliPayViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet
from users.views import SmsCodeViewSet, UserViewSet
import xadmin

router = DefaultRouter()

router.register(r'goods', GoodsListViewSet, base_name="goods")
router.register(r'categorys', CategoryViewSet, base_name="categorys")
router.register(r'codes', SmsCodeViewSet, base_name="codes")
router.register(r'users', UserViewSet, base_name="users")
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")
router.register(r'messages', LeavingMessageViewSet, base_name="messages")
router.register(r'address', AddressViewSet, base_name="address")
router.register(r'shopcarts', ShopCartViewSet, base_name="shopcarts")
router.register(r'orders', OrderViewSet, base_name="orders")
router.register(r'banners', BannerViewSet, base_name="banners")
router.register(r'indexgoods', IndexCategoryViewSet, base_name="indexgoods")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    # path('goods/', GoodsListView.as_view(), name='goods-list'),
    path('docs/', include_docs_urls(title='restframework文档')),
    path('api-auth/', include('rest_framework.urls')),
    re_path('^', include(router.urls)),
    path('login/', views.obtain_auth_token),
    # path('login/', obtain_jwt_token),
    path('alipay/return/', AliPayViewSet.as_view()),
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
    path('', include('social_django.urls', namespace='social'))
]
