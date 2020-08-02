from datetime import date, timedelta

from projects.models import Project


def get_most_recent_events(company):
    # This includes last two week
    # Projects
    # Products
    # Materials
    # Customers
    events = []

    two_weeks_ago = date.today() - timedelta(days=14)
    projects = Project.objects.filter(updated_at__gte=two_weeks_ago)
