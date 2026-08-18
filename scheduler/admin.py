from django.contrib import admin
from .models import Product, Appointment, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'date', 'time_slot', 'service_type', 'status')
    list_filter = ('status', 'date', 'service_type')
    search_fields = ('name', 'email', 'phone', 'service_type')
    ordering = ('date', 'time_slot')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'email', 'total_price', 'status', 'paid', 'created_at')
    list_filter = ('status', 'paid', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    inlines = [OrderItemInline]
