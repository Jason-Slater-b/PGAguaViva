from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name','phone','email','city','order_total']
    list_filter = ['status','is_ordered']
    search_filter = ['order_number','first_name','last_name','phone','email']
    list_perf_page = 20



admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)