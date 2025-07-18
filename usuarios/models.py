from django.db import models

class ItemCardapio(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    foto = models.ImageField(upload_to='cardapio/')

    def __str__(self):
        return self.titulo
