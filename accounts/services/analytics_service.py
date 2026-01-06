from django.db.models import Count
from django.db.models.functions import TruncMonth
from  contributions.models import PullRequest, Issue 



def get_monthly_issue(user):
    print("SERVICE: get_monthly_issue called")
    return list(
            Issue.objects.filter(repository__user = user).annotate(month=TruncMonth("created_at")).values("month").annotate(count=Count("id")).order_by("month")
        )


def get_monthly_prs(user):
    print("SERVICE: get_monthly_prs called")
    return list(
            PullRequest.objects.filter(repository__user = user).annotate(month=TruncMonth("created_at")).values("month").annotate(count=Count("id")).order_by("month")
        )