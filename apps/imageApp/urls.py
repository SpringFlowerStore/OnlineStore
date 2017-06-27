from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name = "main"),
    url(r'^index$', views.index, name = "index"),
    url(r'^uploadAnImage$', views.uploadImage, name = "uploadImage"),
    url(r'^showImage$', views.allImages, name = "showImage"),
    url(r'^changeUserDetails$', views.changeUserDetails, name = "changeUserDetails"),
    url(r'^changeUserIcon$', views.changeUserIcon, name = "changeUserIcon"),
    url(r'^showUser$', views.showUser, name = "showUser"),
    url(r'^show$', views.all_show, name = "all_show"),
    url(r'^see_product/(?P<id>\d+)$', views.see_product, name = "see_product"),
    url(r'^cart$', views.cart, name = "cart"),
    url(r'^like/(?P<id>\d+)$', views.likeProduct, name= "like"),
]
