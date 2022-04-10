from django.shortcuts import render
from .forms import MessageForm
from .models import Profile


def dashboard(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
    form = MessageForm()
    return render(request, "sending/dashboard.html", {"form": form})


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "sending/profile_list.html", {"profiles": profiles})


def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    return render(request, "sending/profile_list.html", {"profile": profile})

