from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Post
from .forms import PostForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
import pyperclip


# Helper function to handle form validation and saving for edit_post

def handle_post_form(request, post):
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, ("Your Post Has Been Updated!"))
        return redirect('home')
    return form


def home(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, ("Your Post Has Been Posted!"))
                return redirect('home')

        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"posts": posts, "form": form})
    else:
        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"posts": posts})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(
            request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')


# Helper function to handle follow/unfollow actions

def handle_follow_action(request, pk, action):
    profile = Profile.objects.get(user_id=pk)
    if action == "unfollow":
        request.user.profile.follows.remove(profile)
        messages.success(
            request, ("You Have Successfully Unfollowed {}"
                      .format(profile.user.username)))
    elif action == "follow":
        request.user.profile.follows.add(profile)
        messages.success(
            request, ("You Have Successfully Followed {}"
                      .format(profile.user.username)))
    request.user.profile.save()
    return redirect(request.META.get("HTTP_REFERER"))


def unfollow(request, pk):
    if request.user.is_authenticated:
        return handle_follow_action(request, pk, "unfollow")
    else:
        messages.success(
            request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')


def follow(request, pk):
    if request.user.is_authenticated:
        return handle_follow_action(request, pk, "follow")
    else:
        messages.success(
            request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        posts = Post.objects.filter(user_id=pk).order_by("-created_at")

        # Post Form logic
        if request.method == "POST":
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # Save the profile
            current_user_profile.save()

        return render(request, "profile.html", {"profile": profile,
                                                "posts": posts})
    else:
        messages.success(
            request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')


# Helper function to handle followers/follows views

def handle_follow_view(request, pk, view_name):
    if request.user.id == pk:
        profiles = Profile.objects.get(user_id=pk)
        return render(request, '{}.html'.format(view_name),
                      {"profiles": profiles})
    else:
        messages.success(request, ("That's Not Your Profile Page..."))
        return redirect('home')


def followers(request, pk):
    if request.user.is_authenticated:
        return handle_follow_view(request, pk, 'followers')
    else:
        messages.success(
            request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')


def follows(request, pk):
    if request.user.is_authenticated:
        return handle_follow_view(request, pk, 'follows')
    else:
        messages.success(
            request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, ("You Have Been Logged In! Post Something!"))
            return redirect('home')
        else:
            messages.success(
                request, ("There was an error logging in. Please Try Again..."))
            return redirect('login')

    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(
        request, ("You Have Been Logged Out."))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # second_name = form.cleaned_data['second_name']
            # email = form.cleaned_data['email']
            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, ("You have successfully registered! Welcome!"))
            return redirect('home')

    return render(request, "register.html", {'form': form})


# Helper function to handle form validation and saving for update_user

def handle_user_forms(request, current_user, profile_user):
    user_form = SignUpForm(request.POST or None,
                           request.FILES or None, instance=current_user)
    profile_form = ProfilePicForm(
        request.POST or None, request.FILES or None, instance=profile_user)
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        login(request, current_user)
        messages.success(request, ("Your Profile Has Been Updated!"))
        return redirect('home')
    return user_form, profile_form


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form, profile_form = handle_user_forms(
            request, current_user, profile_user)
        return render(request, "update_user.html", {'user_form': user_form,
                                                    'profile_form': profile_form})
    else:
        messages.success(
            request, ("You Must Be Logged In To View That Page..."))
        return redirect('home')


def post_like(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(
            request, ("You Must Be Logged In To View That Page..."))
        return redirect('home')


def post_show(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post:
        return render(request, "show_post.html", {'post': post})
    else:
        messages.success(request, ("That Post Does Not Exist..."))
        return redirect('home')


def delete_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        # Check to see if you own the post
        if request.user.username == post.user.username:
            # Delete The Post
            post.delete()

            messages.success(request, ("The Post Has Been Deleted!"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("You Don't Own That Post!!"))
            return redirect('home')

    else:
        messages.success(request, ("Please Log In To Continue..."))
        return redirect(request.META.get("HTTP_REFERER"))


def edit_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if request.user.username == post.user.username:
            form = handle_post_form(request, post)
            return render(request, "edit_post.html", {'form': form,
                                                      'post': post})
        else:
            messages.success(request, ("You Don't Own That Post!!"))
            return redirect('home')
    else:
        messages.success(request, ("Please Log In To Continue..."))
        return redirect('home')


def search(request):
    if request.method == "POST":
        # Grab the form field input
        search = request.POST['search']
        # Search the database
        searched = Post.objects.filter(body__contains=search)

        return render(request, 'search.html', {'search': search,
                                               'searched': searched})
    else:
        return render(request, 'search.html', {})


def search_user(request):
    if request.method == "POST":
        # Grab the form field input
        search = request.POST['search']
        # Search the database
        searched = User.objects.filter(username__contains=search)

        return render(request, 'search_user.html', {'search': search,
                                                    'searched': searched})
    else:
        return render(request, 'search_user.html', {})


def share_post(request, pk):
    if request.user.is_authenticated:
        post_url = request.build_absolute_uri(reverse('post_show', args=[pk]))

        pyperclip.copy(post_url)
        messages.success(
            request, ("The URL has been copied to the clipboard!"))
        return JsonResponse({'message': 'URL copied to clipboard'})
    else:
        messages.success(request, ("You Must Be Logged In To Share Posts..."))
        return redirect('home')
