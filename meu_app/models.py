from django.db import models

class Ranking(models.Model):
    nome = models.CharField(max_length=50)
    nivel = models.CharField(max_length=20)
    tentativas = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.nivel} - {self.tentativas} tentativas"
