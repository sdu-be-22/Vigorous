from django.shortcuts import render, redirect
from .forms import MessageForm
from .models import Message, Profile


def dashboard(request):
    if request.method == "POST":
        form = MessageForm(request.POST or None)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return redirect("sending:dashboard")
    form = MessageForm()
    
    return render(request, "sending/dashboard.html", {"form": form})

    followed_messages = Message.objects.filter(user__profile__in=request.user.profile.follows.all()).order_by("-created_at")

    return render(request, "sending/dashboard.html",{"form": form, "messages" : followed_messages}, )

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "sending/profile_list.html", {"profiles": profiles})


def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
        
    return render(request, "sending/profile.html", {"profile": profile})
