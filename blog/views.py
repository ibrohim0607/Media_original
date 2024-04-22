from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Post, Follow, Comment, Like, Settings
from authentication.models import MyUser
from django.contrib.auth.decorators import login_required


@login_required(login_url='/auth/login')
def index_view(request):
    posts = Post.objects.filter(is_published=True)
    users = MyUser.objects.all()[:4]
    user = MyUser.objects.filter(user=request.user).first()
    comments = Comment.objects.all()
    foll = [i.following for i in Follow.objects.filter(follower=request.user.id)]

    for post in posts:
        post.comments = comments.filter(post_id=post.id)

    d = {
        'posts': posts,
        'users': users,
        'user': user,
        'foll': foll,
    }
    if request.method == 'POST':
        data = request.POST
        obj = Comment.objects.create(author=user, message=data['message'], post_id=data['post_id'])
        obj.save()
        return redirect(f"/#{data['post_id']}")

    return render(request, 'index.html', context=d)


def profile_view(request):
    profiles = MyUser.objects.filter(user=request.user)
    context = {
        'profiles': profiles
    }
    return render(request, 'profile.html', context=context)


def profile_settings_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return redirect('/', pk=user.pk)
    else:
        return render(request, 'setting.html', {'user': user})


@login_required(login_url='auth/login')
def like(request):
    author = MyUser.objects.filter(user=request.user).first()
    post_id = request.GET.get('post_id')
    post = Post.objects.filter(id=post_id).first()

    if not post:
        return redirect('/')

    like_obj, created = Like.objects.get_or_create(author=author, post=post)

    if not created:
        like_obj.delete()
    else:
        like_obj.save()

    return redirect(f'/#{post_id}')


@login_required(login_url='auth/login')
def follow(request):
    follower = MyUser.objects.filter(user=request.user).first()
    following = MyUser.objects.filter(id=request.GET.get('follow')).first()

    if not following:
        return redirect('/')

    follow_obj, created = Follow.objects.get_or_create(follower=follower, following=following)

    if not created:
        follow_obj.delete()
    else:
        follow_obj.save()
    return redirect(f'/#{follow}')


def upload_view(request):
    if request.method == 'POST':
        my_user = MyUser.objects.filter(user=request.user).first()
        post = Post.objects.create(picture=request.FILES['picture'], author=my_user)
        post.save()
        return redirect('/')
    return redirect('/')


def search_view(request):
    query = request.GET.get('q')

    if query is '':
        return redirect('/')

    posts = Post.objects.filter(is_published=True, author=query).order_by('-created_at')

    context = {
        'posts': posts,
    }

    return render(request, 'index.html', context)
