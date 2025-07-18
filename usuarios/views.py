from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate #verifica na base de dados ver se o usuario existe
from django.contrib.auth import login as login_django, logout as logout_django #faz o login do usuario e logout do usuario
from .models import Nota #importa o modelo Nota
from django.urls import reverse #importa o reverse para redirecionar para a página de visualização

def login(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')#renderiza a página de login
    else:
        username = request.POST.get('email') #campo nome email do html
        senha = request.POST.get('senha')

        user = authenticate(username = username, password = senha) #verifica se o usuario existe na base de dados
        if user is not None:
            login_django(request, user) #faz o login do usuario
            return render(request, 'usuarios/home.html') #redireciona para a página home após o login
        else:
            return HttpResponse('Login ou senha inválidos!') #retorna uma mensagem de erro
        
def logout(request):
    if request.user.is_authenticated:
        logout_django(request)
        return render(request, 'usuarios/login.html')
    else:
        return HttpResponse('Você não acessou a sua conta ainda!')
    
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html') #renderiza a página de cadastro
    else:
        username = request.POST.get('email') #campo nome email do html
        email = request.POST.get('email')
        password = request.POST.get('senha')
        first_name = request.POST.get('nome')

        user = User.objects.filter(username=username).first() #verifica se o usuario já existe na base de dados

        if user is not None:
            return HttpResponse('Usuario já existe!') #retorna uma mensagem de erro
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name) #cria o usuario na base de dados
            user.save() #salva o usuario na base de dados
            return render(request, 'usuarios/login.html') #redireciona para a página de login após o cadastro

def home(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/home.html') #renderiza a página home
    else:
        return render(request, 'usuarios/login.html')
    
def lancar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'usuarios/lancar.html')
        else:
            return render(request, 'usuarios/login.html')
    else:
        nota = Nota()
        nota.nome_aluno = request.user.first_name  # Obtém o primeiro nome do usuário autenticado
        nota.disciplina = request.POST.get('disciplina')#pegando o nome da disciplina do html
        nota.nota_atividade = request.POST.get('nota_atividade')
        nota.nota_trabalho = request.POST.get('nota_trabalho')
        nota.nota_prova = request.POST.get('nota_prova')
        nota.media = int(nota.nota_atividade) + int(nota.nota_trabalho) + int(nota.nota_prova)#convertendo as notas para inteiro pq html retorna string
        nota_verificada = Nota.objects.filter(disciplina=nota.disciplina).first() #existe a disciplina no banco de dados

        if nota_verificada:
            return HttpResponse('Nota já lançada para essa disciplina!')
        # Verifica se já existe uma nota lançada para a disciplina
        else:
            nota.save()  # Salva no banco
            return render(request, 'usuarios/home.html')

def alterar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            lista_notas = Nota.objects.all()
            dicionario_notas = {'lista_notas': lista_notas}
            return render(request,'usuarios/alterar.html', dicionario_notas)
        else:
            return render(request, 'usuarios/login.html')
    
def visualizar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            lista_notas = Nota.objects.all()
            dicionario_notas = {'lista_notas': lista_notas}
            return render(request,'usuarios/visualizar.html', dicionario_notas)
        else:
            return render(request, 'usuarios/login.html')
    else:
        disciplina = request.POST.get('disciplina')
        if disciplina == "Todas as disciplinas":
            lista_notas = Nota.objects.all()
            dicionario_notas = {'lista_notas': lista_notas}
            return render(request,'usuarios/visualizar.html', dicionario_notas)
        else:
            lista_notas = Nota.objects.filter(disciplina=disciplina)#se tem disciclina no banco
            dicionario_notas_filtradas = {'lista_notas': lista_notas}
            return render(request,'usuarios/visualizar.html', dicionario_notas_filtradas)
        
def excluir_verificacao(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            lista_notas = Nota.objects.get(pk=pk)  # Obtém a nota específica pelo chave primaria
            dicionario_notas = {'lista_notas': lista_notas}
            return render(request, 'usuarios/excluir.html', dicionario_notas)
        else:
            return HttpResponse('Faça o login para acessar!')

def excluir(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            disciplina_selecionada = Nota.objects.get(pk=pk)  # Obtém a nota específica pelo chave primaria
            disciplina_selecionada.delete() # Exclui a nota da base de dados
            return HttpResponseRedirect(reverse('alterar'))  # Redireciona para a página de visualização
    else:
        return HttpResponse('Faça o login para acessar!')

def editar_verificacao(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            lista_notas = Nota.objects.get(pk=pk)  # Obtém a nota específica pelo chave primaria
            dicionario_notas = {'lista_notas': lista_notas}
            return render(request, 'usuarios/editar.html', dicionario_notas)
        else:
            return HttpResponse('Faça o login para acessar!')
        
def editar(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            nome_aluno = request.user.first_name
            disciplina = request.POST.get('disciplina')
            nota_atividade = request.POST.get('nota_atividade')
            nota_trabalho = request.POST.get('nota_trabalho')
            nota_prova = request.POST.get('nota_prova')
            media = int(nota_atividade) + int(nota_trabalho) + int(nota_prova)
            nota = Nota.objects.filter(pk=pk).update(nome_aluno=nome_aluno,disciplina=disciplina,nota_atividade=nota_atividade,nota_trabalho=nota_trabalho,nota_prova=nota_prova,media=media)
            return HttpResponseRedirect(reverse('alterar'))
    else:
        return HttpResponse('Faça o login para acessar!')   