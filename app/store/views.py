from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import datetime

from core.models import *



def home(request, categoria_slug=None):
    categoria_pagina = None
    produtos = None
    if categoria_slug!=None:
        categoria_pagina = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = Produto.objects.filter(categoria=categoria_pagina)
    else:
        produtos = Produto.objects.all()
    context = {'categoria': categoria_pagina, 'produtos': produtos, 'cartItems':cartItems}
    return render(request, 'store/home.html', context)


def produtoPagina(request, categoria_slug, produto_slug):
    try:
        produto = Produto.objects.get(categoria__slug=categoria_slug, slug=produto_slug)
    except expression as e:
        raise e 
    context = {'produto': produto, 'cartItems':0}
    return render(request, 'store/produto_detalhe.html', context)

def about(request):
    context = {}
    return render(request, 'store/about.html')

def store(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, concluido=False)
        items = pedido.itempedido_set.all()
        cartItems = pedido.get_cart_items
    else:
        items = []
        pedido = {'get_cart_tota':0, 'get_cart_items':0, 'shipping':False}
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
        pedido = {'get_cart_tota':0, 'get_cart_items':0,'shipping':False}
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
        pedido = {'get_cart_tota':0, 'get_cart_items':0,'shipping':False}
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


def processarPedido(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, concluido=False)
        total = float(data['form']['total'])
        pedido.transaction_id = transaction_id

        if total == float(pedido.get_cart_total):
            pedido.concluido = True
        pedido.save()

        if pedido.shipping == True:
            EnderecoEntrega.objects.create(
                cliente=cliente,
                pedido=pedido,
                endereco=data['shipping']['endereco'],
                cidade=data['shipping']['cidade'],
                bairro=data['shipping']['bairro'],
                rua=data['shipping']['rua'],
                numero=data['shipping']['numero'],
            )

    else:
        print('User is not logged in')
    return JsonResponse('Pagamento efectuado com sucesso', safe=False)