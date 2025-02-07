from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .models import Agendamento, Paciente, Procedimento
from .forms import AgendamentoForm, ProcedimentoForm, RegistroForm, PacienteForm

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo, {username}!")
                return redirect('listar_agendamentos')
        messages.error(request, "Usuário ou senha inválidos")
    else:
        form = AuthenticationForm

    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu da conta.")
    return redirect('login')

def home(request):
    return render(request, 'usuarios/home.html')

@login_required
def listar_pacientes(request):
    pacientes = Paciente.objects.filter(usuario=request.user)
    return render(request, 'usuarios/listar_pacientes.html', {'pacientes': pacientes})

@login_required
def cadastrar_paciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.usuario = request.user
            paciente.save()
            return redirect('listar_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'usuarios/cadastrar_paciente.html', {'form':form})

@login_required
def listar_procedimentos(request):
    procedimentos = Procedimento.objects.filter(usuario=request.user)
    return render(request, 'usuarios/listar_procedimentos.html', {'procedimentos':procedimentos})


@login_required
def cadastrar_procedimento(request):
    if request.method == 'POST':
        form = ProcedimentoForm(request.POST)
        if form.is_valid():
            procedimento = form.save(commit=False)  # Não salva ainda no banco
            procedimento.usuario = request.user  # Define o usuário logado
            procedimento.save()  # Agora salva no banco
            return redirect('listar_procedimentos')  # Redireciona para a listagem
    else:
        form = ProcedimentoForm()

    return render(request, 'usuarios/cadastrar_procedimento.html', {'form': form})

@login_required
def listar_agendamentos(request):
    agendamentos = Agendamento.objects.filter(usuario=request.user)  # Filtra pelo usuário logado
    return render(request, 'usuarios/listar_agendamentos.html', {'agendamentos': agendamentos})

@login_required
def agendar_procedimento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, usuario=request.user)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.usuario = request.user  # Associa o agendamento ao usuário logado
            agendamento.save()
            return redirect('listar_agendamentos')
    else:
        form = AgendamentoForm(usuario=request.user)  # Passa o usuário para filtrar os pacientes

    return render(request, 'usuarios/agendar_procedimento.html', {'form': form})

@login_required
def meu_cadastro(request):
    return render(request, 'usuarios/meu_cadastro.html')

@login_required
def editar_procedimento(request, pk):
    procedimento = get_object_or_404(Procedimento, pk=pk)
    if request.method == 'POST':
        form = ProcedimentoForm(request.POST, instance=procedimento)
        if form.is_valid():
            form.save()
            return redirect('listar_procedimentos')
    else:
        form = ProcedimentoForm(instance=procedimento)
    return render(request, 'usuarios/editar_procedimento.html', {'form': form})

@login_required
def excluir_procedimento(request, pk):
    procedimento = get_object_or_404(Procedimento, pk=pk)
    if request.method == 'POST':
        procedimento.delete()
        return redirect('listar_procedimentos')
    return render(request, 'usuarios/excluir_procedimento.html', {'procedimento': procedimento})

@login_required
def editar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento, usuario=request.user)
        if form.is_valid():
            form.save()
            return redirect('listar_agendamentos')
    else:
        form = AgendamentoForm(instance=agendamento, usuario=request.user)

    return render(request, 'usuarios/editar_agendamento.html', {'form':form})