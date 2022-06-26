from django import forms

from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    subscribe = forms.BooleanField(required=False)

    class Meta:
        model = Subscriber
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        email = email.lower().strip()
        return email

    def save(self, commit=True):
        subscriber = super().save(commit=False)
        if self.cleaned_data['subscribe'] is True:
            existing = Subscriber.objects.filter(email=subscriber.email)
            if existing.exists():
                subscriber = existing.first()
            if commit:
                subscriber.save()
        else:
            subscriber = Subscriber.objects.filter(email=subscriber.email).delete()
        return subscriber
