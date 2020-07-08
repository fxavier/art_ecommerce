from django.contrib import admin

from .models import Produto, Categoria, Pedido, Cliente, ItemPedido, EnderecoEntrega


admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(Cliente)
admin.site.register(ItemPedido)
admin.site.register(EnderecoEntrega)