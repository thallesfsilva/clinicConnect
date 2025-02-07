from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Agendamento, Procedimento, UsuarioPersonalizado, Paciente

class RegistroForm(UserCreationForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2']

class PacienteForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type':'date'})
    )

    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento', 'telefone', 'endereco']

class ProcedimentoForm(forms.ModelForm):
    class Meta:
        model = Procedimento
        fields = ['nome', 'descricao', 'preco']

class AgendamentoForm(forms.ModelForm):
    data_horario = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Agendamento
        fields = ['paciente','procedimento', 'data_horario', 'status']

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)  # Pegamos o usuário logado
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields['paciente'].queryset = Paciente.objects.filter(usuario=usuario)  # Filtra pacientes do usuário logado
            self.fields['procedimento'].queryset = Procedimento.objects.filter(usuario=usuario)  # Filtra procedimentos do usuário
