from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Followers, LikePost, Post, Profile


# ---------------------------------------------------------------------------
# Auth views
# ---------------------------------------------------------------------------

def signup(request):
    """Register a new user and immediately log them in."""
    if request.method == 'POST':
        username = request.POST.get('fnm', '').strip()
        email    = request.POST.get('emailid', '').strip()
        password = request.POST.get('pwd', '')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
            return render(request, 'signup.html')

        user = User.objects.create_user(username, email, password)
        Profile.objects.create(user=user, id_user=user.id)

        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')


def loginn(request):
    """Authenticate an existing user."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('fnm', '').strip()
        password = request.POST.get('pwd', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid username or password.')
        return render(request, 'loginn.html')

    return render(request, 'loginn.html')


@login_required(login_url='/loginn/')
def logoutt(request):
    """Log the current user out."""
    logout(request)
    return redirect('loginn')


# ---------------------------------------------------------------------------
# Feed / home
# ---------------------------------------------------------------------------

@login_required(login_url='/loginn/')
def home(request):
    """Show posts from the logged-in user and everyone they follow."""
    # Auto-create profile if missing (handles existing users / data migration gaps)
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'id_user': request.user.id},
    )

    following_users = Followers.objects.filter(
        follower=request.user.username
    ).values_list('user', flat=True)

    posts = Post.objects.filter(
        Q(user=request.user.username) | Q(user__in=following_users)
    ).order_by('-created_at')

    # Build username->profile map so each post shows the correct author avatar
    post_usernames  = set(p.user for p in posts)
    author_profiles = {
        ap.user.username: ap
        for ap in Profile.objects.filter(
            user__username__in=post_usernames
        ).select_related('user')
    }

    # Attach each post's author avatar URL directly on the post object
    for p in posts:
        author = author_profiles.get(p.user)
        p.author_avatar = author.profileimg.url if author else profile.profileimg.url

    return render(request, 'main.html', {
        'post':    posts,
        'profile': profile,
    })


# ---------------------------------------------------------------------------
# Posts
# ---------------------------------------------------------------------------

@login_required(login_url='/loginn/')
def upload(request):
    """Create a new post."""
    if request.method == 'POST':
        image   = request.FILES.get('image_upload')
        caption = request.POST.get('caption', '').strip()

        if not image:
            messages.error(request, 'Please select an image to upload.')
            return redirect('home')

        Post.objects.create(
            user=request.user.username,
            image=image,
            caption=caption,
        )
        messages.success(request, 'Post uploaded successfully.')
        return redirect('home')

    return redirect('home')


@login_required(login_url='/loginn/')
def delete(request, id):
    """Delete a post (only the owner can delete)."""
    post = get_object_or_404(Post, id=id)

    if post.user != request.user.username:
        messages.error(request, 'You are not allowed to delete this post.')
        return redirect('home')

    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('profile', id_user=request.user.username)


# ---------------------------------------------------------------------------
# Likes
# ---------------------------------------------------------------------------

@login_required(login_url='/loginn/')
def likes(request, id):
    """Toggle like/unlike on a post."""
    post     = get_object_or_404(Post, id=id)
    username = request.user.username

    existing = LikePost.objects.filter(post_id=id, username=username).first()

    if existing:
        existing.delete()
        post.no_of_likes = max(post.no_of_likes - 1, 0)   # guard against negatives
    else:
        LikePost.objects.create(post_id=id, username=username)
        post.no_of_likes += 1

    post.save()
    return redirect('home')


# ---------------------------------------------------------------------------
# Explore
# ---------------------------------------------------------------------------

@login_required(login_url='/loginn/')
def explore(request):
    """Show all posts, newest first."""
    posts           = Post.objects.all().order_by('-created_at')
    profile, _      = Profile.objects.get_or_create(
        user=request.user,
        defaults={'id_user': request.user.id},
    )

    return render(request, 'explore.html', {'post': posts, 'profile': profile})


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------

@login_required(login_url='/loginn/')
def profile(request, id_user):
    """View (and optionally edit) a user's profile."""
    user_object      = get_object_or_404(User, username=id_user)
    user_profile     = get_object_or_404(Profile, user=user_object)
    my_profile, _    = Profile.objects.get_or_create(
        user=request.user,
        defaults={'id_user': request.user.id},
    )

    user_posts       = Post.objects.filter(user=id_user).order_by('-created_at')
    user_post_length = user_posts.count()

    user_followers = Followers.objects.filter(user=id_user).count()
    user_following = Followers.objects.filter(follower=id_user).count()

    is_own_profile = (request.user.username == id_user)
    follow_unfollow = None

    if not is_own_profile:
        follow_unfollow = (
            'Unfollow'
            if Followers.objects.filter(follower=request.user.username, user=id_user).exists()
            else 'Follow'
        )

    # Handle profile edit (only the owner)
    if is_own_profile and request.method == 'POST':
        bio      = request.POST.get('bio', '').strip()
        location = request.POST.get('location', '').strip()
        image    = request.FILES.get('image')

        user_profile.bio      = bio
        user_profile.location = location
        if image:
            user_profile.profileimg = image
        user_profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile', id_user=id_user)

    context = {
        'user_object':       user_object,
        'user_profile':      user_profile,
        'user_posts':        user_posts,
        'user_post_length':  user_post_length,
        'profile':           my_profile,
        'follow_unfollow':   follow_unfollow,
        'user_followers':    user_followers,
        'user_following':    user_following,
        'is_own_profile':    is_own_profile,
    }
    return render(request, 'profile.html', context)


# ---------------------------------------------------------------------------
# Follow / Unfollow
# ---------------------------------------------------------------------------

@login_required(login_url='/loginn/')
def follow(request):
    """Follow or unfollow another user."""
    if request.method == 'POST':
        follower = request.POST.get('follower', '').strip()
        user     = request.POST.get('user', '').strip()

        # Prevent self-follow
        if follower == user:
            messages.error(request, "You can't follow yourself.")
            return redirect('profile', id_user=user)

        obj = Followers.objects.filter(follower=follower, user=user).first()
        if obj:
            obj.delete()
        else:
            Followers.objects.create(follower=follower, user=user)

        return redirect('profile', id_user=user)

    return redirect('home')


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

@login_required(login_url='/loginn/')
def search_results(request):
    """Search users by username and posts by caption."""
    query = request.GET.get('q', '').strip()

    users = Profile.objects.filter(
        user__username__icontains=query
    ).select_related('user') if query else Profile.objects.none()

    posts = Post.objects.filter(
        caption__icontains=query
    ).order_by('-created_at') if query else Post.objects.none()

    return render(request, 'search_user.html', {
        'query': query,
        'users': users,
        'posts': posts,
    })