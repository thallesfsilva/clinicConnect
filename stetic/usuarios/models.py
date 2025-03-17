from datetime import date
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


class Fatura(models.Model):
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_de_emissao = models.DateField(default=date.today)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"Fatura #{self.id} para {self.paciente.nome} - Total: R$ {self.valor_total}"
    
class ItemFatura(models.Model):
    fatura = models.ForeignKey(Fatura, related_name='itens', on_delete=models.CASCADE)
    procedimento = models.ForeignKey(Procedimento, on_delete=models.SET_NULL, null=True)
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"
    
class Pagamento(models.Model):
    FORMA_PAGAMENTO_CHOICES = [
        ('Dinheiro', 'Dinheiro'),
        ('Cartão de Crédito', 'Cartão de Crédito'),
        ('Cartão de Débito', 'Cartão de Débito'),
        ('PIX', 'PIX'),
        ('Boleto Bancário', 'Boleto Bancário'),
        ('Transferência Bancária', 'Transferência Bancária'),
    ]

    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE, related_name='pagamentos')
    data_pagamento = models.DateField(default=date.today)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pagamento de R$ {self.valor_pago} em {self.get_forma_pagamento_display()} para Fatura #{self.fatura.id}"