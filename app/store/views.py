from django.shortcuts import render
from django.http import JsonResponse
import json

from core.models import *


def store(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, concluido=False)
        items = pedido.itempedido_set.all()
        cartItems = pedido.get_cart_items
    else:
        items = []
        pedido = {'get_cart_tota':0, 'get_cart_items':0}
        cartItems = pedido['get_cart_items']

    produtos = Produto.objects.all()
    context = {'produtos':produtos, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):

    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, concluido=False)
        items = pedido.itempedido_set.all()
        cartItems = pedido.get_cart_items
    else:
        items = []
        pedido = {'get_cart_tota':0, 'get_cart_items':0}
        cartItems = pedido['get_cart_items']

    context = {'items': items, 'pedido':pedido, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, concluido=False)
        items = pedido.itempedido_set.all()
        cartItems = pedido.get_cart_items
    else:
        items = []
        pedido = {'get_cart_tota':0, 'get_cart_items':0}
        cartItems = pedido['get_cart_items']

    context = {'items': items, 'pedido':pedido, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    produtoId = data['produtoId']
    action = data['action']

    print('Action:', action)
    print('Produto:', produtoId)

    cliente = request.user.cliente
    produto = Produto.objects.get(id=produtoId)
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, concluido=False)

    itemPedido, criado = ItemPedido.objects.get_or_create(pedido=pedido, produto=produto)

    if action == 'add':
        itemPedido.quantidade = (itemPedido.quantidade + 1)
    elif action == 'remove':
        itemPedido.quantidade = (itemPedido.quantidade - 1)

    itemPedido.save()

    if itemPedido.quantidade <= 0:
        itemPedido.delete()

    return JsonResponse('Produto adicionado com sucesso', safe=False)