from itertools import chain
from  django . shortcuts  import  get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from . models import  Followers, LikePost, Post, Profile
from django.db.models import Q
from  . models import  Post, LikePost , Profile 



# Create your views here.

def signup(request):
 try:
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('emailid')
        pwd=request.POST.get('pwd')
        print(fnm,emailid,pwd)
        my_user=User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        user_model = User.objects.get(username=fnm)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        if my_user is not None:
            login(request,my_user)
            return redirect('/')
        return redirect('/loginn')
    
        
 except:
        invalid="User already exists"
        return render(request, 'signup.html',{'invalid':invalid})
  
    
 return render(request, 'signup.html')

def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(fnm,pwd)
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request,userr)
            return redirect('/')
        
        invalid = "invaild Credentials"
        return render(request , 'login.html',{'invalid' : invalid})
    
    return render(request , 'loginn.html')

def logoutt(request):
    logout(request)
    return redirect('/loginn/')

def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        Post.objects.create(
            user=user,
            image=image,
            caption=caption
        )

        return redirect('/')

    return redirect('/')


def home(request):
    post = Post.objects.all().order_by('-create_at')

    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

    context = {
        'post': post,
        'profile': profile
    }

    return render(request, 'main.html', context)

def likes(request, id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post, id=id)

        like_filter = LikePost.objects.filter(post_id=id, username=username).first()

        if like_filter is None:
            new_like = LikePost.objects.create(post_id=id, username=username)
            post.no_of_likes = post.no_of_likes + 1
        else:
            like_filter.delete()
            post.no_of_likes = post.no_of_likes - 1

        post.save()

        # Generate the URL for the current post's detail page
        print(post.id)

        # Redirect back to the post's detail page
        return redirect('/#'+id)
    
def home_post(request,id):
    post=Post.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    context={
        'post':post,
        'profile':profile
    }
    return render(request, 'main.html',context)
    

