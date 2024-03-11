from django.contrib import admin
from cart_app.models import Cart, CartItem, Payment



admin.site.register(Cart)

admin.site.register(Payment)
admin.site.register(CartItem)