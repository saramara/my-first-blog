from django.shortcuts import render
from .models import Post, Utente
from .forms import PostForm, UserForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


@login_required
def post_list(request):
    user = request.user
    posts = Post.objects.filter(published_date__lte=timezone.now(), author=user).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if isinstance(request.user, User):
                post.author = request.user
            else:
                try:
                    user_exists = User.objects.get(username = 'autore_temp')
                except user.DoesNotExists:
                    autore_temp =  User.objects.create_user('autore_temp', 'aut@ciao.it','autore_temp')
                    autore_temp.save()
                    user_exists = autore_temp
                post.author = user_exists
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_draft_list(request):
    posts_no_pub = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts_no_pub': posts_no_pub})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def register(request):
    utente = UserForm(request.POST)
    return render(request, 'blog/user_register.html', {'utente' : utente})

def save_register(request):
    if request.method == "POST":
        diz_valori = dict(request.POST)
        utente =  User.objects.create_user(diz_valori['nome_utente'][0], 'aut@ciao.it',diz_valori['password'][0])
        utente.save()
        user = authenticate(username=diz_valori['nome_utente'][0], password=diz_valori['password'][0])
        if user is not None:
            login(request, user)
            return redirect('post_list')
        else:
            return render(request, 'blog/register.html')
    else:
        utente = UserForm(request.POST)
        return render(request, 'blog/register.html')


def registrazione_effettuata(request):
    return render(request, 'blog/registrazione_effettuata.html')
