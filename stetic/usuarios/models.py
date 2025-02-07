from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UsuarioPersonalizado(AbstractUser):
    bio = models.TextField(blank=True, null=True)

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class Procedimento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    

class Agendamento(models.Model):

    STATUS_CHOICE = [
        ('Marcado', 'Marcado'),
        ('Realizado', 'Realizado'),
        ('Pago', 'Pago'),
        ('Cancelado', 'Cancelado'), 
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='agendamentos')
    procedimento = models.ForeignKey(Procedimento, on_delete=models.CASCADE)
    data_horario = models.DateTimeField(null=True, blank=True)  # Permite valores nulos
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='Marcado')

    def __str__(self):
        return f"{self.procedimento.nome} - {self.paciente.nome} em {self.data_horario.strftime('%d/%m/%Y %H:%M') if self.data_horario else 'Sem data' ({self.get_status_display()})}"

    