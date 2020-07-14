from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings

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
    context = {'categoria': categoria_pagina, 'produtos': produtos}
    return render(request, 'store/home.html', context)


def produtoPagina(request, categoria_slug, produto_slug):
    try:
        produto = Produto.objects.get(categoria__slug=categoria_slug, slug=produto_slug)
    except expression as e:
        raise e 
    context = {'produto': produto}
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

# def cart(request):

    """ if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, concluido=False)
        items = pedido.itempedido_set.all()
        cartItems = pedido.get_cart_items
    else:
        items = []
        pedido = {'get_cart_tota':0, 'get_cart_items':0,'shipping':False}
        cartItems = pedido['get_cart_items']

    context = {'items': items, 'pedido':pedido, 'cartItems':cartItems} """
  #  context = {}
  #  return render(request, 'store/cart.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
            )
        cart.save()
    try:
        cart_item = CartItem.objects.get(produto=produto, cart=cart)
        if cart_item.quantidade < cart_item.produto.stock:
            cart_item.quantidade += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            produto=produto,
            quantidade=1,
            cart=cart
            )
        cart_item.save()

    return redirect('cart')


def cart(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.produto.preco * cart_item.quantidade)
            counter += cart_item.quantidade
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Nyau Galeria - Novo Pedido'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    
    return render(request, 'store/cart.html', dict(cart_items=cart_items, total=total, counter=counter, data_key=data_key, stripe_total=stripe_total, description=description))


def cart_remove(request, produto_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    cart_item = CartItem.objects.get(produto=produto, cart=cart)
    if cart_item.quantidade > 1:
        cart_item.quantidade -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def cart_remove_produto(request, produto_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    produto = get_object_or_404(Produto, id=produto_id)
    cart_item = CartItem.objects.get(produto=produto, cart=cart)
    cart_item.delete()
    return redirect('cart')

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


""" def updateItem(request):
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

    return JsonResponse('Produto adicionado com sucesso', safe=False) """


""" def processarPedido(request):
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
    return JsonResponse('Pagamento efectuado com sucesso', safe=False) """