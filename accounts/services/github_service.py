import requests


def github_get(url, token):
    headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    return requests.get(url, headers=headers)