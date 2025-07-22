from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.urls import reverse
from .models import ItemCardapio
from django.shortcuts import render, redirect

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
            return render(request, 'usuarios/login.html', {'erro': 'Login ou senha inválidos!'})

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
            return render(request, 'usuarios/cadastro.html', {'erro': 'Usuário já existe.'})
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
            user.save()
            return render(request, 'usuarios/login.html')

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'usuarios/login.html', {'erro': 'Você precisa estar logado para acessar essa página.'})
    else:
        return render(request, 'usuarios/home.html')

def lancar(request):
    if not request.user.is_authenticated:
        return render(request, 'usuarios/login.html', {'erro': 'Você precisa estar logado para acessar essa página.'})
    elif request.method == 'GET':
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
    if not request.user.is_authenticated:
        return render(request, 'usuarios/login.html', {'erro': 'Você precisa estar logado para acessar essa página.'})
    elif request.method == 'GET':
        if request.user.is_authenticated:
            lista_itens = ItemCardapio.objects.all()
            return render(request, 'usuarios/alterar.html', {'lista_itens': lista_itens})


def excluir_verificacao(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'usuarios/login.html', {'erro': 'Você precisa estar logado para acessar essa página.'})
    elif request.user.is_authenticated:
        item = ItemCardapio.objects.get(pk=pk)
        return render(request, 'usuarios/excluir.html', {'item': item})

def excluir(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'usuarios/login.html', {'erro': 'Você precisa estar logado para acessar essa página.'})
    elif request.user.is_authenticated:
        item = ItemCardapio.objects.get(pk=pk)
        item.delete()
        return HttpResponseRedirect(reverse('alterar'))

def editar_verificacao(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'usuarios/login.html', {'erro': 'Você precisa estar logado para acessar essa página.'})
    elif request.user.is_authenticated:
        item = ItemCardapio.objects.get(pk=pk)
        return render(request, 'usuarios/editar.html', {'item': item})

def editar(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'usuarios/login.html', {
            'erro': 'Você precisa estar logado para acessar essa página.'
        })

    elif request.method == 'POST':
        item = ItemCardapio.objects.get(pk=pk)
        item.titulo = request.POST.get('titulo')
        item.descricao = request.POST.get('descricao')
        item.valor = request.POST.get('valor')

        if 'foto' in request.FILES:
            item.foto = request.FILES['foto']

        item.save()
        return HttpResponseRedirect(reverse('alterar'))

def editar_sem_id(request):
    return render(request, 'usuarios/login.html', {
        'erro': 'Você precisa estar logado para acessar essa página.'
    })

def visualizar(request):
    if not request.user.is_authenticated:
        return render(request, 'usuarios/login.html', {'erro': 'Você precisa estar logado para acessar essa página.'})
    elif request.user.is_authenticated:
        ordenacao = request.GET.get('ordenar', '')

        if ordenacao == 'titulo':
            lista_itens = ItemCardapio.objects.order_by('titulo')
        elif ordenacao == 'preco_menor':
            lista_itens = ItemCardapio.objects.order_by('valor')
        elif ordenacao == 'preco_maior':
            lista_itens = ItemCardapio.objects.order_by('-valor')
        else:
            lista_itens = ItemCardapio.objects.all()

        return render(request, 'usuarios/visualizar.html', {'lista_itens': lista_itens})

def sobre(request):
    if not request.user.is_authenticated:
        return render(request, 'usuarios/login.html', {'erro': 'Você precisa estar logado para acessar essa página.'})
    else:
        return render(request, 'usuarios/sobre.html')

def contato(request):
    if not request.user.is_authenticated:
        return render(request, 'usuarios/login.html', {'erro': 'Você precisa estar logado para acessar essa página.'})
    else:
        return render(request, 'usuarios/contato.html')

def logout(request):
    if request.user.is_authenticated:
        logout_django(request)
        return render(request, 'usuarios/login.html')
    else:
       return render(request, 'usuarios/login.html', {'erro': 'Você ainda não acessou sua conta!'})
