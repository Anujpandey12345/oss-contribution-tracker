import requests # Used to make HTTP requests (GET, POST) to GitHub API
from django.conf import settings
from django.contrib.auth import login  # Imports Django’s built-in login system
from django.contrib.auth.models import User  #Imports Django’s default User model
from django.shortcuts import render, redirect
from django.http import HttpResponse

"""GitHub Login View"""
def github_login(request):
    github_auth_url = (
        "https://github.com/login/oauth/authorize" # This is Official Github OAuth authorization endpoint.
        f"?client_id={settings.GITHUB_CLIENT_ID}" # this tell GITHUB: “Hey GitHub, this login request belongs to MY app”
    )
    return redirect(github_auth_url)


"""GitHub Callback Logic"""


def github_callback(request):
    code = request.GET.get("code") # A temporary authorization code which is send by github after user approves access

    token_response = requests.post(
        "https://github.com/login/oauth/access_token",  # This is GitHub’s token endpoint.
        headers={"Accept": "application/json"},
        data={
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        },
    )
    token_json = token_response.json() # Converts HTTP response → Python dictionary
    access_token = token_json.get("access_token") # Allows your app to access GitHub data on behalf of the user (A secret key)


    user_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"token {access_token}"},
    )


    github_user = user_response.json()  # GitHub response
    username = github_user["login"]
    email = github_user.get("email")
    if not email:
        email = f"{username}@users.noreply.github.com"

    user, created = User.objects.get_or_create(  # Why get_or_create? Prevents:- ❌ Duplicate users , ❌ Login errors
        username = username,
        defaults={"email":email}
    )
    login(request, user)
    return redirect("/")



