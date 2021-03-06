# blog - views.py

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, loader, RequestContext
from django.http import HttpResponse

from models import Post
from forms import PostForm


# helper functions

def encode_url(url):
    return url.replace(' ', '_')


def popular_context():
    popular_posts = Post.objects.order_by('-views')[:5]
    return popular_posts


# view functions

def index(request):
    latest_posts = Post.objects.all().order_by('-created_at')
    t = loader.get_template('blog/index.html')
    context_dict = {
        'latest_posts': latest_posts,
        'popular_posts': popular_context(),
    }
    c = Context(context_dict)
    return HttpResponse(t.render(c))


def post(request, slug):
    single_post = get_object_or_404(Post, slug=slug)
    single_post.views += 1
    single_post.save()
    t = loader.get_template('blog/post.html')
    context_dict = {
        'single_post': single_post,
        'popular_posts': popular_context(),
    }
    c = Context(context_dict)
    return HttpResponse(t.render(c))


def add_post(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect(index)
        else:
            print form.errors
    else:
        form = PostForm()
    return render_to_response('blog/add_post.html', {'form': form}, context)
