from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ
from . import reports


from .models import (
    MembershipPlan, Subscription, FitnessClass,
    Booking, Attendance, Order, Payment, Feedback
)
from .serializers import (
    MembershipPlanSerializer, SubscriptionSerializer, FitnessClassSerializer,
    BookingSerializer, AttendanceSerializer, OrderSerializer,
    PaymentSerializer, FeedbackSerializer
)
from .permissions import IsAdmin, IsStaff, IsMember


# ---------- MEMBERSHIP ----------
class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]  
        return [IsStaff(), IsAdmin()]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]   # Only members can subscribe
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAdmin()]   # Admin controls subscriptions
        return [IsAuthenticated()]


# ---------- CLASSES ----------
class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]   # Everyone can see schedules
        return [IsStaff(), IsAdmin()]   # Staff manage classes


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]   # Members can book
        elif self.action == "destroy":
            return [IsMember(), IsAdmin()]   # Members cancel, Admin override
        return [IsAuthenticated()]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [IsStaff(), IsAdmin()]   # Staff mark attendance
        return [IsAuthenticated()]


# ---------- ORDERS & PAYMENTS ----------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]   
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAdmin()]   
        return [IsAuthenticated()]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]   


# ---------- FEEDBACK ----------
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsMember()]   
        elif self.action == "destroy":
            return [IsAdmin()]    
        return [IsAuthenticated()]


# ---------- PAYMENT GATEWAY (SSLCOMMERZ) ----------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    user = request.user
    amount = request.data.get("amount")
    order_id = request.data.get("orderId")
    num_items = request.data.get("numItems", 1) 

    settings = {
        "store_id": "algoa68c171ec6ed0f",
        "store_pass": "algoa68c171ec6ed0f@ssl",
        "issandbox": True,
    }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = "12345"
    post_body['success_url'] = "your success url"
    post_body['fail_url'] = "your fail url"
    post_body['cancel_url'] = "your cancel url"
    post_body['emi_option'] = 0
    post_body['cus_name'] = "test"
    post_body['cus_email'] = "test@test.com"
    post_body['cus_phone'] = "01700000000"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body)
    if response.get("status") == "SUCCESS":
        return Response({"payment_url": response["GatewayPageURL"]})
    return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def payment_success(request):
    return Response({"status": "success", "message": "Payment completed successfully"})


@api_view(["POST"])
def payment_fail(request):
    return Response({"status": "failed", "message": "Payment failed"})


@api_view(["POST"])
def payment_cancel(request):
    return Response({"status": "cancelled", "message": "Payment was cancelled"})


# ---------- REPORTS ----------
@api_view(["GET"])
@permission_classes([IsAdmin])
def membership_report(request):
    return Response({"membership_report": reports.generate_membership_report()})


@api_view(["GET"])
@permission_classes([IsAdmin])
def attendance_report(request):
    return Response({"attendance_report": reports.generate_attendance_report()})


@api_view(["GET"])
@permission_classes([IsAdmin])
def feedback_report(request):
    return Response({"feedback_report": reports.generate_feedback_report()})


@api_view(["GET"])
@permission_classes([IsAdmin])
def revenue_report(request):
    return Response({"revenue_report": reports.generate_revenue_report()})
