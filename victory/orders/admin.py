from django.contrib import admin

from .models import Order, WorkCost, Comment

admin.site.register(Order)
admin.site.register(WorkCost)
admin.site.register(Comment)
