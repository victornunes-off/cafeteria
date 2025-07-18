from django.db import models

# Create your models here.

class Nota(models.Model):
    nome_aluno = models.CharField(max_length=100)#catacter tipo texto
    disciplina = models.CharField(max_length=100)
    nota_atividade = models.IntegerField(default=0)  # 
    nota_trabalho = models.IntegerField(default=0)  # 
    nota_prova = models.IntegerField(default=0)
    media = models.FloatField(blank = True, default = 0)  # float tipo decimalx