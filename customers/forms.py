from django import forms


class CustomerForm(forms.ModelForm):
    title = forms.CharField(label="Titel")


class ContactPersonForm:
    pass