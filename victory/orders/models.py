from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile')
    phone_regex = RegexValidator(
        regex=r'^\+?\d{9,15}$',
        message="Phone number must be entered in the format: '+77071234567'")
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=False,
        unique=True)


class Order(models.Model):

    class Status(models.IntegerChoices):
        NEW = 0, _('New')
        IN_PROGRESS = 1, _('InProgress')
        WAIT_FOR_DETAILS = 2, _('WaitForDetails')
        WAIT_FOR_CLIENT = 3, _('WaitForClient')
        READY = 4, _('Ready')
        FIXED = 5, _('Fixed')

    title = models.CharField('title', max_length=500)
    description = models.TextField('description', max_length=1000)
    created = models.DateTimeField('created', auto_now_add=True)
    updated = models.DateTimeField('updated', auto_now=True)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_orders'
    )
    status = models.IntegerField(choices=Status.choices)
    client = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='orders'
    )

    def get_absolute_url(self):
        return reverse('orders:update_order', args=[self.id])

    def total_price(self):
        return sum(self.works.values('price'))

    def __str__(self):
        return self.title


class Comment(models.Model):
    created = models.DateTimeField('created', auto_now_add=True)
    text = models.TextField(max_length=1000)
    # author = user or client
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return self.order.get_absolute_url()


class WorkCost(models.Model):
    work = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='works'
    )

    def __str__(self):
        return self.work
