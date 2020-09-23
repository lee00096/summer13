from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post, Comment, User

def new(request):
    return render(request, 'posts/new.html')


def create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user = request.user)
        return redirect('posts:main')
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})

    # if request.method == "POST":
    #     title = request.POST.get('title')
    #     content = request.POST.get('content')
    #     image = request.FILES.get('image')
    #     user = request.user
    #     Post.objects.create(title=title, content=content, image=image, user=user)
    #     return redirect('posts:main')


def main(request):
    posts = Post.objects.all()
    return render(request, 'posts/main.html', {'posts': posts})


def show(request, id):
    post = Post.objects.get(pk=id)
    post.view_count +=1
    post.save()
    all_comments = post.comments.all().order_by('-created_at')
    return render(request, 'posts/show.html', {'post': post, 'comments': all_comments})


def update(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.image = request.FILES.get('image')
        post.save()
        return redirect('posts:show', post.id)
    return render(request, 'posts/update.html', {'post': post})


def delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect("posts:main")


def create_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404 (Post, pk=post_id)
        current_user = request.user
        comment_content = request.POST.get('content')
        Comment.objects.create(content=comment_content, user=current_user, post=post)
    return redirect('posts:show', post.pk)