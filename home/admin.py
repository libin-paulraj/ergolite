from django.contrib import admin
from .models import Chairs, CartModel
from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
admin.site.unregister(User)

class ChairsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'order']
    list_filter = ['category']

admin.site.register(Chairs, ChairsAdmin)
admin.site.register(CartModel)  # ✅ Proper model name
