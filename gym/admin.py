from django.contrib import admin
from .models import (
    MembershipPlan, Subscription, FitnessClass,
    Booking, Attendance, Order, Payment, Feedback
)


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration_days")
    search_fields = ("name",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("member", "plan", "start_date", "end_date")
    list_filter = ("plan",)


@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ("title", "instructor", "start_time", "duration_minutes")
    search_fields = ("title", "instructor__username")
    list_filter = ("start_time",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("member", "fitness_class", "booked_at")
    list_filter = ("fitness_class",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("booking", "present", "marked_at")
    list_filter = ("present",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("member", "total_price", "status", "created_at")
    list_filter = ("status",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "amount", "transaction_id", "status", "created_at")
    list_filter = ("status",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("member", "fitness_class", "rating", "created_at")
    list_filter = ("rating", "fitness_class")
