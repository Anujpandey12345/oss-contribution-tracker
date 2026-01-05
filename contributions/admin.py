from django.contrib import admin
from .models import Repository, PullRequest, Issue
# Register your models here.


admin.site.register(Repository)
admin.site.register(PullRequest)
admin.site.register(Issue)