from django.db.models import Count, Avg, Sum, Q
from .models import MembershipPlan, Subscription, Attendance, Feedback, Payment


def generate_membership_report():
    """
    Returns total subscriptions per plan.
    """
    data = Subscription.objects.values("plan__name").annotate(total=Count("id"))
    return list(data)


def generate_attendance_report():
    """
    Returns total attendance per class.
    """
    data = Attendance.objects.values("booking__fitness_class__title").annotate(
        present_count=Count("id", filter=Q(present=True)),
        absent_count=Count("id", filter=Q(present=False)),
    )
    return list(data)


def generate_feedback_report():
    """
    Returns average rating per class.
    """
    data = Feedback.objects.values("fitness_class__title").annotate(
        avg_rating=Avg("rating"),
        total_reviews=Count("id"),
    )
    return list(data)


def generate_revenue_report():
    """
    Returns total revenue and payments count.
    """
    data = Payment.objects.aggregate(
        total_revenue=Sum("amount"),
        total_payments=Count("id"),
    )
    return data
