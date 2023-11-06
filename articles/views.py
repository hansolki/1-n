from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

# Create your views here.
def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)

def detail(request, id):
    article = Article.objects.get(id=id)
    form = CommentForm()

    # comment 목록 조회
    # 첫번째 방법
    # comments = Comment.objects.filter(article=article)

    # 두번째 방법
    # comments = article.comment_set.all()
    #=> views에서 실행하고 변수에 결과를 담아서 html코드에서 실행

    # 세번째방법
    # html 코드에서 article.comment_set.all 사용
    #=> 애초에 html코드에서 실행 

    context = {
        'article': article,
        'form': form,
        # 'comments': comments,

    }

    return render(request, 'detail.html', context)

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', id=article.id)
    else:
        form = ArticleForm()
        
    context = {
        'form': form,
    }

    return render(request, 'form.html', context)

def comment_create(request, article_id):
    form = CommentForm(request.POST)

    if form.is_valid():
        # form을 저장 => 추가로 넣어야 하는 데이터를 넣기 위해서 저장 멈춰!.!
        comment = form.save(commit=False)

        # # 첫번째 방법(객체를 저장하는 방법)
        # # article_id를 기준으로 article object 가져오기
        # article = Article.objects.get(id=article_id)
        # # article 컬럼에 추가
        # comment.article = article
        # comment.save()

        # 두번째 방법(integer를 저장하는 방법)
        comment.article_id = article_id
        comment.save()

        return redirect('articles:detail', id=article_id)

def comment_delete(request, article_id, id):
    comment = Comment.objects.get(id=id)
    comment.delete()    

    return redirect('articles:detail', id=article_id)