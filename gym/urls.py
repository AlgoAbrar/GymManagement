from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MembershipPlanViewSet, SubscriptionViewSet, FitnessClassViewSet,
    BookingViewSet, AttendanceViewSet, OrderViewSet, PaymentViewSet,
    FeedbackViewSet, initiate_payment, payment_success, payment_fail,
    payment_cancel, membership_report, attendance_report,
    feedback_report, revenue_report
)

router = DefaultRouter()
router.register(r"plans", MembershipPlanViewSet, basename="membership-plan")
router.register(r"subscriptions", SubscriptionViewSet, basename="subscription")
router.register(r"classes", FitnessClassViewSet, basename="fitness-class")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"attendance", AttendanceViewSet, basename="attendance")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"feedback", FeedbackViewSet, basename="feedback")

urlpatterns = [
    
    path("", include(router.urls)),

    path("payment/initiate/", initiate_payment, name="initiate-payment"),
    path("payment/success/", payment_success, name="payment-success"),
    path("payment/fail/", payment_fail, name="payment-fail"),
    path("payment/cancel/", payment_cancel, name="payment-cancel"),

    path("reports/membership/", membership_report, name="membership-report"),
    path("reports/attendance/", attendance_report, name="attendance-report"),
    path("reports/feedback/", feedback_report, name="feedback-report"),
    path("reports/revenue/", revenue_report, name="revenue-report"),
]
