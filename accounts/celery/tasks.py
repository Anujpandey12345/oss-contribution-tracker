from celery import shared_task
from django.contrib.auth.models import User
from contributions.models import Repository
from accounts.services.github_service import github_get


@shared_task
def fetch_repos(user_id, token):
    user = User.objects.get(id=user_id)


    response = github_get(
        "https://api.github.com/user/repos", token
    )

    for repo in response.json():
        Repository.objects.get_or_create(
            github_id = repo["id"],
            defaults={
                "user": user,
                "name": repo["name"],
                "full_name": repo["full_name"],
                "html_url": repo["html_url"],
            },
        )
