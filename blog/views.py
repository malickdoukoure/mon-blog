from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Article, Category
from .forms import RegisterForm, ArticleForm, CommentForm

def article_list(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    return render(request, 'blog/article_list.html', {
        'articles': articles,
        'categories': categories,
    })

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.save()
            return redirect('article_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comment_form': comment_form,
        'categories': categories,
    })

def category_articles(request, pk):
    category = get_object_or_404(Category, pk=pk)
    articles = Article.objects.filter(category=category)
    return render(request, 'blog/article_list.html', {
        'articles': articles,
        'categories': Category.objects.all(),
        'current_category': category,
    })

def register(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('article_list')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {
        'form': form,
        'categories': categories,
    })

@login_required
def article_create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {
        'form': form,
        'categories': categories,
    })

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {
        'form': form,
        'categories': categories,
    })

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'blog/article_confirm_delete.html', {
        'article': article,
        'categories': Category.objects.all(),
    })