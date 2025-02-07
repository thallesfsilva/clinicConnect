from django.urls import path
from django.contrib.auth.views import LoginView
from .views import editar_agendamento, editar_procedimento, excluir_procedimento, listar_procedimentos, meu_cadastro, registro, login_view, logout_view, home, listar_pacientes, cadastrar_paciente, cadastrar_procedimento, listar_agendamentos, agendar_procedimento

urlpatterns = [
    path('', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('pacientes/', listar_pacientes, name='listar_pacientes'),
    path('pacientes/cadastrar/', cadastrar_paciente, name='cadastrar_paciente'),
    path('procedimentos/', listar_procedimentos, name='listar_procedimentos'),
    path('procedimentos/cadastrar/', cadastrar_procedimento, name='cadastrar_procedimento'),
    path('agendamentos/', listar_agendamentos, name='listar_agendamentos'),
    path('agendamentos/cadastrar/', agendar_procedimento, name='agendar_procedimento'),
    path('meu_cadastro/', meu_cadastro, name='meu_cadastro'),
    path('<int:pk>/editar/', editar_procedimento, name='editar_procedimento'),
    path('<int:pk>/excluir/', excluir_procedimento, name='excluir_procedimento'),
    path('<int:pk>/editar_agendamento/', editar_agendamento, name='editar_agendamento')
]