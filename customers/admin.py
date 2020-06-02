from django.contrib import admin

from customers.models import Customer, ContactPerson

admin.site.register(Customer)
admin.site.register(ContactPerson)
