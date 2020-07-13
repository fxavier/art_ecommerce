from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('categoria/<slug:categoria_slug>', views.home, name="produtos_por_categoria"),
    path('categoria/<slug:categoria_slug>/<slug:produto_slug>', views.produtoPagina, name="produto_detalhe"),
    path('about/', views.about, name="about"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('update-item/', views.updateItem, name="update-item"),
    path('process-pedido/', views.processarPedido, name="process-pedido"),
]


