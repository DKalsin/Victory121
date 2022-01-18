from django.forms import ModelForm
from django.core.exceptions import ValidationError
from phonenumbers import parse as parse_phone, format_number, PhoneNumberFormat

from .models import Order, User


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('title', 'description', 'assignee', 'status')


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name')

    def clean_username(self):
        try:
            phone = parse_phone(self.cleaned_data['username'])
        except Exception as e:
            raise ValidationError("Phone number is not valid") from e
        self.cleaned_data['username'] = format_number(phone, PhoneNumberFormat.E164)
