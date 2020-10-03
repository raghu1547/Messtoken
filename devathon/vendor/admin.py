from django.contrib import admin
from .models import Token, ExtraItems, Transaction
# Register your models here.
admin.site.register(Token)
admin.site.register(ExtraItems)
admin.site.register(Transaction)
