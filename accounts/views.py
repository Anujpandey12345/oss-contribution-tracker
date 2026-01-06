import requests # Used to make HTTP requests (GET, POST) to GitHub API
from django.conf import settings
from django.contrib.auth import login, logout  # Imports Django’s built-in login, Logout system
from django.contrib.auth.models import User  #Imports Django’s default User model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from contributions.models import Repository, PullRequest, Issue


"""GitHub Login View"""
def github_login(request):
    github_auth_url = (
        "https://github.com/login/oauth/authorize" # This is Official Github OAuth authorization endpoint.
        f"?client_id={settings.GITHUB_CLIENT_ID}" # this tell GITHUB: “Hey GitHub, this login request belongs to MY app”
    )
    return redirect(github_auth_url)


# For LogOut
def logout_view(request):
    logout(request)
    return redirect("/")





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
    request.session["github_token"] = access_token   #Why session? - > Secure & Automatically cleared on logout


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


@login_required
def fetch_repositories(request):
    token = request.session.get("github_token")

    # Condition if Token Not Available then we Redirect on the page
    if not token:
        return redirect("/")
    
    response = requests.get(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
        },
    )

    repos = response.json()  # Converts JSON → Python list of dictionaries


    for repo in repos:
        Repository.objects.update_or_create(
            github_id = repo["id"],
            defaults={
                "user": request.user,
                "name": repo["name"],
                "full_name": repo["full_name"],
                "html_url": repo["html_url"],
                "description": repo.get("description") or "",
                "language": repo.get("language") or "",
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
            },
        )
    return redirect("/")

@login_required
def fetch_global_pull_requests(request):
    token = request.session.get("github_token")

    if not token:
        return redirect("/")
    
    username = request.user.username
    search_url = (
        f"https://api.github.com/search/issues"
        f"?q=author:{username}+type:pr"
    )
    response = requests.get(
            search_url,
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github+json",
            },
        )

    data = response.json()
    pull_requests = data.get("items", [])


    for pr in pull_requests:
        repo_full_name = pr["repository_url"].split("repos/")[-1]
        repo, created = Repository.objects.get_or_create(
            full_name = repo_full_name,
            defaults={
                "user": request.user,
                "name": repo_full_name.split("/")[-1],
                "html_url": f"https://github.com/{repo_full_name}",
            },
        )
        if repo.user is None:
            repo.user = request.user
            repo.save()
        PullRequest.objects.update_or_create(
            repository=repo,
            number=pr["number"],
            defaults={
                "title": pr["title"],
                "state": pr["state"],
                "html_url": pr["html_url"],
                "created_at": pr["created_at"],
                "merged": pr.get("pull_request", {}).get("merged_at") is not None
            },
        )
    return redirect("/accounts/dashboard/")


@login_required
def fetch_global_issues(request):
    token = request.session.get("github_token")   # Reads GitHub access token stored during login

    if not token:
        return redirect("/")
    
    username = request.user.username
    search_url = (
        f"https://api.github.com/search/issues"
        f"?q=involves:{username}+type:pr"        #Invloves is use for Any issue or pull request where the user is involved in ANY way
    )
    response = requests.get(
        search_url,
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
        },
    )
    dataI = response.json()
    items = dataI.get("items", [])


    for issue in items:
        repo_full_name = issue["repository_url"].split("repos/")[-1]
        repo, created = Repository.objects.get_or_create(
            full_name = repo_full_name,
            defaults={
                "user": request.user,
                "name": repo_full_name.split("/")[-1],
                "html_url": f"https://github.com/{repo_full_name}",
            },
        )
        if repo.user is None:
            repo.user = request.user
            repo.save()
        Issue.objects.update_or_create(
            repository = repo,
            number = issue["number"],
            defaults = {
                "title": issue["title"],
                "state": issue["state"],
                "html_url": issue["html_url"],
                "created_at": issue["created_at"],
            },
        )
    return redirect("/accounts/dashboard/")





@login_required
def dashboard(request):
    repositories = Repository.objects.all().prefetch_related("issues", "pull_requests")
    

    #stats
    repo_count = repositories.count()
    pr_total = PullRequest.objects.filter(repository__user = request.user).count()
    pr_merged = PullRequest.objects.filter(repository__user = request.user, merged=True).count()
    issue_total = Issue.objects.filter(repository__user = request.user).count()
    issue_closed = Issue.objects.filter(repository__user = request.user, state="closed").count()

    context = {
        "repositories": repositories,
        "repo_count": repo_count,
        "pr_total": pr_total,
        "pr_merged": pr_merged,
        "issue_total": issue_total,
        "issue_closed": issue_closed,
    }

    return render(request,"dashboard.html", context)

    



