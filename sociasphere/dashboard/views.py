from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import PostForm, ProfilePicForm, SignUpForm
from .models import Post, Profile


def safe_redirect(request: HttpRequest, fallback: str = 'home') -> HttpResponse:
    """Redirect only to a same-host referrer; never trust an arbitrary URL."""
    referrer = request.META.get('HTTP_REFERER')
    if referrer and url_has_allowed_host_and_scheme(
        referrer,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(referrer)
    return redirect(fallback)


def handle_post_form(request, post):
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, "Your Post Has Been Updated!")
        return redirect('home')
    return form


def home(request):
    form = None
    if request.user.is_authenticated:
        form = PostForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Your Post Has Been Posted!")
            return redirect('home')

    posts = Post.objects.select_related('user', 'user__profile').prefetch_related('likes').order_by("-created_at")
    context = {"posts": posts}
    if form is not None:
        context["form"] = form
    return render(request, 'home.html', context)


def profile_list(request):
    if not request.user.is_authenticated:
        messages.info(request, "You Must Be Logged In To View This Page.")
        return redirect('home')
    profiles = Profile.objects.exclude(user=request.user).select_related('user')
    return render(request, 'profile_list.html', {"profiles": profiles})


def handle_follow_action(request, pk, action):
    if request.method != "POST":
        return HttpResponse(status=405)
    profile = get_object_or_404(Profile, user_id=pk)
    current_profile = request.user.profile
    if action == "unfollow":
        current_profile.follows.remove(profile)
        messages.success(request, f"You Have Successfully Unfollowed {profile.user.username}")
    elif action == "follow":
        if profile.pk != current_profile.pk:
            current_profile.follows.add(profile)
            messages.success(request, f"You Have Successfully Followed {profile.user.username}")
    else:
        return HttpResponse(status=400)
    return safe_redirect(request)


def unfollow(request, pk):
    if not request.user.is_authenticated:
        messages.info(request, "You Must Be Logged In To View This Page.")
        return redirect('home')
    return handle_follow_action(request, pk, "unfollow")


def follow(request, pk):
    if not request.user.is_authenticated:
        messages.info(request, "You Must Be Logged In To View This Page.")
        return redirect('home')
    return handle_follow_action(request, pk, "follow")


def profile(request, pk):
    if not request.user.is_authenticated:
        messages.info(request, "You Must Be Logged In To View This Page.")
        return redirect('home')

    profile_obj = get_object_or_404(Profile.objects.select_related('user'), user_id=pk)
    posts = (
        Post.objects.filter(user_id=pk)
        .select_related('user', 'user__profile')
        .prefetch_related('likes')
        .order_by("-created_at")
    )

    if request.method == "POST":
        action = request.POST.get('follow')
        if action == "unfollow":
            request.user.profile.follows.remove(profile_obj)
        elif action == "follow" and profile_obj.pk != request.user.profile.pk:
            request.user.profile.follows.add(profile_obj)
        else:
            return HttpResponse(status=400)
        request.user.profile.save()
        return redirect('profile', pk=pk)

    return render(request, "profile.html", {"profile": profile_obj, "posts": posts})


def handle_follow_view(request, pk, view_name):
    if request.user.id != pk:
        messages.info(request, "That's Not Your Profile Page.")
        return redirect('home')
    profile_obj = get_object_or_404(Profile, user_id=pk)
    return render(request, f'{view_name}.html', {"profiles": profile_obj})


def followers(request, pk):
    if not request.user.is_authenticated:
        messages.info(request, "You Must Be Logged In To View This Page.")
        return redirect('home')
    return handle_follow_view(request, pk, 'followers')


def follows(request, pk):
    if not request.user.is_authenticated:
        messages.info(request, "You Must Be Logged In To View This Page.")
        return redirect('home')
    return handle_follow_view(request, pk, 'follows')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "You Have Been Logged In! Post Something!")
        return redirect('home')
    return render(request, "login.html", {"form": form})


def logout_user(request):
    if request.method != "POST":
        return HttpResponse(status=405)
    logout(request)
    messages.success(request, "You Have Been Logged Out.")
    return redirect('home')


def register_user(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "You have successfully registered! Welcome!")
        return redirect('home')
    return render(request, "register.html", {'form': form})


def handle_user_forms(request, current_user, profile_user):
    user_form = SignUpForm(
        request.POST or None,
        request.FILES or None,
        instance=current_user,
    )
    profile_form = ProfilePicForm(
        request.POST or None,
        request.FILES or None,
        instance=profile_user,
    )
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        login(request, current_user)
        messages.success(request, "Your Profile Has Been Updated!")
        return redirect('home')
    return user_form, profile_form


def update_user(request):
    if not request.user.is_authenticated:
        messages.info(request, "You Must Be Logged In To View That Page.")
        return redirect('home')
    current_user = get_object_or_404(User, id=request.user.id)
    profile_user = get_object_or_404(Profile, user_id=request.user.id)
    user_form, profile_form = handle_user_forms(request, current_user, profile_user)
    return render(request, "update_user.html", {'user_form': user_form, 'profile_form': profile_form})


def post_like(request, pk):
    if not request.user.is_authenticated:
        messages.info(request, "You Must Be Logged In To View This Page.")
        return redirect('home')
    if request.method != "POST":
        return HttpResponse(status=405)
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return safe_redirect(request)


def post_show(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, "show_post.html", {'post': post})


def delete_post(request, pk):
    if not request.user.is_authenticated:
        messages.info(request, "Please Log In To Continue.")
        return redirect('home')
    if request.method != "POST":
        return HttpResponse(status=405)
    post = get_object_or_404(Post, id=pk)
    if post.user_id != request.user.id:
        messages.error(request, "You Don't Own That Post.")
        return redirect('home')
    post.delete()
    messages.success(request, "The Post Has Been Deleted!")
    return safe_redirect(request)


def edit_post(request, pk):
    if not request.user.is_authenticated:
        messages.info(request, "Please Log In To Continue.")
        return redirect('home')
    post = get_object_or_404(Post, id=pk)
    if post.user_id != request.user.id:
        messages.error(request, "You Don't Own That Post.")
        return redirect('home')
    form = handle_post_form(request, post)
    return render(request, "edit_post.html", {'form': form, 'post': post})


def search(request):
    if request.method == "POST":
        search_term = request.POST.get('search', '').strip()
        if not search_term:
            return render(request, 'search.html', {'search': '', 'searched': Post.objects.none()})
        searched = (
            Post.objects.filter(body__icontains=search_term)
            .select_related('user', 'user__profile')
            .prefetch_related('likes')[:100]
        )
        return render(request, 'search.html', {'search': search_term, 'searched': searched})
    return render(request, 'search.html', {})


def search_user(request):
    if request.method == "POST":
        search_term = request.POST.get('search', '').strip()
        if not search_term:
            return render(request, 'search_user.html', {'search': '', 'searched': User.objects.none()})
        searched = User.objects.filter(username__icontains=search_term)[:100]
        return render(request, 'search_user.html', {'search': search_term, 'searched': searched})
    return render(request, 'search_user.html', {})


def share_post(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Authentication required'}, status=401)
    if request.method != "POST":
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    post = get_object_or_404(Post, id=pk)
    post_url = request.build_absolute_uri(reverse('post_show', args=[post.pk]))
    return JsonResponse({'url': post_url})
