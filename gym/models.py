from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class MembershipPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.price} BDT)"


class Subscription(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return f"{self.member} - {self.plan}"


class FitnessClass(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="instructor_classes")
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)

    def __str__(self):
        return f"{self.title} ({self.start_time})"


class Booking(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} booked {self.fitness_class}"


class Attendance(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    marked_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="pending") 
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="initiated")  


class Feedback(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
