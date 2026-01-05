from django.db import models
from django.contrib.auth.models import User


"""Important line -> "I used ForeignKey to model one-to-many user-repository relationship"   """

class Repository(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, # If user deleted then delete their repo's
        related_name="repositories"
    )
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    github_id = models.IntegerField(unique=True, null=True, blank=False)
    html_url = models.URLField()
    description = models.TextField(blank=True)
    language = models.CharField(max_length=100, blank=True)
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.full_name
    

"""" I separated PRs and Issues because they have different lifecycle and attributes"""


class PullRequest(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="pull_requests"
    )
    title = models.CharField(max_length=255)
    number = models.IntegerField()
    state = models.CharField(max_length=20)
    html_url = models.URLField()
    created_at = models.DateTimeField()
    merged = models.BooleanField(default=False)

    def __str__(self):
        return f"PR #{self.number} - {self.title}"
    

class Issue(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="issues"
    )
    title = models.CharField(max_length=255)
    number = models.IntegerField()
    state = models.CharField(max_length=20)
    html_url = models.URLField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Issue #{self.number} - {self.title}"
