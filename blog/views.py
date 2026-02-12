from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article, Category
from .forms import RegisterForm, ArticleForm, CommentForm

ARTICLES_PER_PAGE = 6

def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'blog/article_list.html', {
        'articles': articles,
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.save()
            return redirect('article_detail', slug=article.slug)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comment_form': comment_form,
    })

def category_articles(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category)
    paginator = Paginator(articles, ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'blog/article_list.html', {
        'articles': articles,
        'current_category': category,
    })

def search(request):
    query = request.GET.get('q', '').strip()
    articles = []
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )[:10]
    return render(request, 'blog/search_results.html', {
        'articles': articles,
    })

@login_required
def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.article = article
        comment.save()
        comment_form = CommentForm()
    return render(request, 'blog/comments_section.html', {
        'article': article,
        'comment_form': comment_form,
    })

def register(request):
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
    })

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {
        'form': form,
    })

@login_required
def article_edit(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {
        'form': form,
    })

@login_required
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'blog/article_confirm_delete.html', {
        'article': article,
    })
