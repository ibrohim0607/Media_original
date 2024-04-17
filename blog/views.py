from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Post, Follow, Like, Comment
from authentication.models import MyUser
from django.contrib.auth.decorators import login_required


@login_required(login_url='/auth/login')
def index_view(request):
    posts = Post.objects.filter(is_published=True)
    users = MyUser.objects.all()[:4]
    user = MyUser.objects.filter(user=request.user).first()
    comments = Comment.objects.all()
    for post in posts:
        post.comments = comments.filter(post_id=post.id),
    d = {
        'posts': posts,
        'users': users,
        'user': user
    }
    if request.method == 'POST':
        data = request.POST
        obj = Comment.objects.create(author=user, message=data['message'], post_id=data['post_id'])
        obj.save()
        return redirect(f"/#{data['post_id']}")
    return render(request, 'index.html', context=d)


@login_required(login_url='/auth/login')
def follow(request):
    follower = MyUser.objects.filter(user=request.user).first()
    following = MyUser.objects.filter(id=request.GET.get('follow_id')).first()
    obj = Follow.objects.create(follower=follower, following=following)
    obj.save()
    return redirect('/')


@login_required(login_url='/auth/login')
def unfollow(request):
    follower = MyUser.objects.filter(user=request.user).first()
    following = MyUser.objects.filter(id=request.GET.get('unfollow')).first()
    obj = Follow.objects.create(follower=follower, following=following)
    obj.delete()
    return redirect('/')


@login_required(login_url='/auth/login')
def like(request, pk):
    if request.user.is_authenticated:
        user = request.user
        my_user = MyUser.objects.get(id=user.id)
        post = get_object_or_404(Post, id=pk)
        if post.like.filter(id=my_user.id):
            post.like.remove(my_user)
        else:
            post.like.add(my_user)
        return redirect('/')
    else:
        return HttpResponse('You Must Be Logged In')


def profile_view(request):
    user = MyUser.objects.all()
    d = {
        'user': user
    }
    """
    there
    """
    return render(request, 'profile.html', context=d)
