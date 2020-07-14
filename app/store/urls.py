from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('categoria/<slug:categoria_slug>', views.home, name="produtos_por_categoria"),
    path('categoria/<slug:categoria_slug>/<slug:produto_slug>', views.produtoPagina, name="produto_detalhe"),
    path('about/', views.about, name="about"),
    path('cart/add/<int:produto_id>', views.add_cart, name="add_cart"),
    path('cart/', views.cart, name="cart"),
    path('cart/remove/<int:produto_id>', views.cart_remove, name="cart_remove"),
    path('cart/remove_produto/<int:produto_id>', views.cart_remove_produto, name="cart_remove_produto"),
]


