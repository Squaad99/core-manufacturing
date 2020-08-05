import datetime
from datetime import date, timedelta

from django.utils import timezone

from customers.models import Customer
from materials.models import Material
from products.models import Product
from projects.models import Project


def get_event_type(object_input):
    event = 'Uppdaterad'
    if object_input.created_at == object_input.updated_at:
        event = 'Skapad'
    return event


def add_events_from_object_list(object_list, event_list, event_type, url):
    for current_object in object_list:
        event_list.append({'type': event_type,
                           'name': current_object.title,
                           'date': current_object.updated_at,
                           'event': get_event_type(current_object),
                           'by': current_object.created_by,
                           'id': current_object.id,
                           'url': url
                           })


def get_most_recent_events(company):
    # This includes last one week
    two_weeks_ago = datetime.datetime.now(tz=timezone.utc) - timedelta(days=7)
    events = []
    # Projects
    projects = list(Project.objects.filter(updated_at__gt=two_weeks_ago, company=company))
    add_events_from_object_list(projects, events, 'Projekt', 'project-detail')
    # Products
    products = list(Product.objects.filter(updated_at__gt=two_weeks_ago, company=company))
    add_events_from_object_list(products, events, 'Produkt', 'product-detail')
    # Materials
    materials = list(Material.objects.filter(updated_at__gt=two_weeks_ago, company=company))
    add_events_from_object_list(materials, events, 'Material', 'material-detail')
    # Customers
    customers = list(Customer.objects.filter(updated_at__gt=two_weeks_ago, company=company))
    add_events_from_object_list(customers, events, 'Kund', 'customer-detail')

    events.sort(key=lambda x: x['date'], reverse=True)

    return events
