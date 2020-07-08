import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


def product_image_file_path(instance, filename):
    """Generates file name """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/produtos', filename)

CIDADES = (
    ('Maputo','Maputo'),
    ('Matola', 'Matola'),
    ('Xai-Xai', 'Xai-Xai'),
    ('Inhambane', 'Inhambane'),
    ('Chimoio', 'Chimoio'),
    ('Beira', 'Beira'),
    ('Tete', 'Tete'),
    ('Quelimane', 'Quelimane'),
    ('Nampula', 'Nampula'),
    ('Pemba', 'Pemba'),
    ('Lichinga', 'Lichinga')
)

class Categoria(models.Model):
    nome = models.CharField(max_length=250, unique=True)
    descricao = models.TextField(blank=True)


    def __str__(self):
        return self.nome


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=255, null=True)

    def __str__(self):
        return self.nome
    

class Produto(models.Model):
    nome = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to=product_image_file_path, blank=True, null=True)
    stock = models.IntegerField()
    ano = models.IntegerField(null=True)
    tema = models.CharField(max_length=200, null=True, blank=True)
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True, blank=True)
    tecnica = models.CharField(max_length=200, null=True, blank=True)
    dimensoes = models.CharField(max_length=200, null=True, blank=True)
    disponivel = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_actualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nome',)

    def save(self, *args, **kwargs):
        if not self.slug and self.nome:
            self.slug = slugify(self.nome)
        super(Produto, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('detalhe_produto', args=[self.categoria.slug, self.slug])

    def __str__(self):
        return self.nome

    @property
    def imageURL(self):
        try:
            url = self.imagem.url
        except:
            url = ''
        return url

class Autor(models.Model):
    nome = models.CharField(max_length=200)
    obras = models.CharField(max_length=500)
    descricao = models.TextField()

    def __str__(self):
        return self.nome
    

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    concluido = models.BooleanField(default=False, null=True, blank=True)
    codigo_transacao = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'Pedido'
        ordering = ['-data_pedido']

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        itemspedido = self.itempedido_set.all()
        for i in itemspedido:
            shipping = True
        return shipping

    @property
    def get_cart_total(self):
        itemspedido = self.itempedido_set.all()
        total = sum([item.get_total for item in itemspedido])
        return total

    @property
    def get_cart_items(self):
        itemspedido = self.itempedido_set.all()
        total = sum([item.quantidade for item in itemspedido])
        return total


class ItemPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    quantidade = models.IntegerField(default=0, null=True, blank=True)
   # preco = models.DecimalField(max_digits=10, decimal_places=2)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ItemPedido'
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Items Pedido'

    def __str__(self):
        return self.produto.nome

    @property
    def get_total(self):
        total = self.produto.preco * self.quantidade
        return total


class EnderecoEntrega(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    endereco = models.CharField(max_length=200, null=False)
    cidade = models.CharField(choices=CIDADES, max_length=10)
    bairro = models.CharField(max_length=200)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=200)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Enderecos de entrega'

    def __str__(self):
        return self.endereco
    