from django.urls import path

from urls.views import (
    create_short_url,
    home,
    login_user,
    redirect_view,
    register_user,
    urls_list,
)

urlpatterns = [
    path("sign_up/", register_user, name="sign_up"),
    path("login", login_user, name="login"),
    path("", home, name="home"),
    path("create_url/", create_short_url, name="create_url"),
    path("urls/", urls_list, name="urls_list"),
    path("<str:hash>", redirect_view, name="redirect_view"),
]
