from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from .models import ItemCardapio
from django.urls import reverse

def login(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')
    else:
        username = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)
        if user is not None:
            login_django(request, user)
            return render(request, 'usuarios/home.html')
        else:
            return HttpResponse('Login ou senha inválidos!')

def logout(request):
    if request.user.is_authenticated:
        logout_django(request)
        return render(request, 'usuarios/login.html')
    else:
        return HttpResponse('Você não acessou a sua conta ainda!')

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html')
    else:
        username = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        first_name = request.POST.get('nome')

        user = User.objects.filter(username=username).first()

        if user is not None:
            return HttpResponse('Usuário já existe!')
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
            user.save()
            return render(request, 'usuarios/login.html')

def home(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/home.html')
    else:
        return render(request, 'usuarios/login.html')

def lancar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'usuarios/lancar.html')
        else:
            return render(request, 'usuarios/login.html')
    else:
        if request.user.is_authenticated:
            item = ItemCardapio()
            item.titulo = request.POST.get('titulo')
            item.descricao = request.POST.get('descricao')
            item.valor = request.POST.get('valor')
            item.foto = request.FILES.get('foto')
            item.save()
            return render(request, 'usuarios/home.html')
        else:
            return render(request, 'usuarios/login.html')

def alterar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            lista_itens = ItemCardapio.objects.all()
            return render(request, 'usuarios/alterar.html', {'lista_itens': lista_itens})
        else:
            return render(request, 'usuarios/login.html')

def visualizar(request):
    if request.user.is_authenticated:
        lista_itens = ItemCardapio.objects.all()
        return render(request, 'usuarios/visualizar.html', {'lista_itens': lista_itens})
    else:
        return render(request, 'usuarios/login.html')

def excluir_verificacao(request, pk):
    if request.user.is_authenticated:
        item = ItemCardapio.objects.get(pk=pk)
        return render(request, 'usuarios/excluir.html', {'item': item})
    else:
        return HttpResponse('Faça o login para acessar!')

def excluir(request, pk):
    if request.user.is_authenticated:
        item = ItemCardapio.objects.get(pk=pk)
        item.delete()
        return HttpResponseRedirect(reverse('alterar'))
    else:
        return render(request, 'usuarios/login.html')

def editar_verificacao(request, pk):
    if request.user.is_authenticated:
        item = ItemCardapio.objects.get(pk=pk)
        return render(request, 'usuarios/editar.html', {'item': item})
    else:
        return HttpResponse('Faça o login para acessar!')

def editar(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            item = ItemCardapio.objects.get(pk=pk)
            item.titulo = request.POST.get('titulo')
            item.descricao = request.POST.get('descricao')
            item.valor = request.POST.get('valor')

            if 'foto' in request.FILES:
                item.foto = request.FILES['foto']

            item.save()
            return HttpResponseRedirect(reverse('alterar'))
    else:
        return HttpResponse('Faça o login para acessar!')
