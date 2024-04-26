from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from urls.forms import URLForm
from urls.models import URL


def register_user(request):
    if request.user.is_authenticated:
        return redirect("urls:home")
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            return redirect("urls:home")
        return render(
            request=request,
            template_name="urls/sign_up.html",
            context={"form": form},
            status=403,
        )

    return render(
        request=request,
        template_name="urls/sign_up.html",
        context={
            "form": UserCreationForm(),
        },
    )


def login_user(request):
    if request.user.is_authenticated:
        return redirect("urls:home")
    elif request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("urls:home")
        return render(
            request=request,
            template_name="urls/login.html",
            context={"form": form},
            status=403,
        )
    return render(
        request=request,
        template_name="urls/login.html",
        context={"form": AuthenticationForm()},
    )


@login_required
def home(request):
    return render(
        request=request,
        template_name="urls/home.html",
        context={"form": URLForm(), "url": request.user.urls.last()},
    )


@login_required
def create_short_url(request):
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            url = URL(
                url=form.cleaned_data["url"],
                user=request.user,
            )
            url.save()
            print(url)
    return redirect("urls:home")


def redirect_view(request, hash):
    url = get_object_or_404(URL, hash=hash)
    url.visits_count += 1
    url.save()
    return HttpResponseRedirect(url.url)


@login_required
def urls_list(request):
    urls = request.user.urls.all()
    return render(
        request=request,
        template_name="urls/urls_list.html",
        context={"urls": urls},
    )
