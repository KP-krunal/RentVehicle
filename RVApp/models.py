from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone


# Helper function for default date values
def current_date():
    return timezone.now().date()


class registermodel(models.Model):
    u_name = models.CharField(max_length=30, null=True)
    u_email = models.EmailField()
    u_phone = models.BigIntegerField()
    u_address = models.TextField()
    u_password = models.CharField(max_length=8, null=True)

    ROLE = [
        ("Employee", "Employee"),
        ("User", "User"),
    ]
    role = models.CharField(max_length=10, choices=ROLE, default='User')

    STATUS = [
        ("0", "unapproved"),
        ("1", "approved")
    ]
    status = models.CharField(max_length=10, choices=STATUS, default='0')

    id_proof = models.FileField(upload_to='id_proofs/', null=True, blank=True)

    def pic(self):
        return mark_safe(f'<img src="{self.id_proof.url}" width="100">')

    pic.allow_tags = True

    def __str__(self):
        return self.u_name


class cars(models.Model):
    vehicle_image = models.ImageField(upload_to='Cars/', null=True, blank=True)
    v_name = models.TextField()

    Seats = [
        ("0", "4"),
        ("1", "5"),
        ("2", "7")
    ]
    seats = models.CharField(max_length=10, choices=Seats, default="1")  # Default to "5 seats"

    V_Type = [
        ("SUVs", "SUVs"),
        ("Sedans", "Sedans"),
        ("Crossovers", "Crossovers"),
        ("Coupes", "Coupes"),
        ("Hatchbacks", "Hatchbacks"),
    ]
    vehicle_type = models.CharField(max_length=50, choices=V_Type, default="1")  # Default to "Sedans"
    stock_no = models.TextField(unique=True)
    doors = models.IntegerField()
    year = models.IntegerField()
    mileage = models.IntegerField(default=0)
    color = models.CharField(max_length=50)
    VIN = models.TextField(unique=True)
    price = models.FloatField(default=0.0)
    description = models.TextField(null=True)
    make = models.CharField(max_length=50, null=True)

    V_status = [
        ("0", "Unavailable"),
        ("1", "Available")
    ]
    status = models.CharField(max_length=10, choices=V_status, default="1")  # Default to "Available"

    def __str__(self):
        return self.v_name
    
    def vehicle_pic(self):
        return mark_safe(f'<img src="{self.vehicle_image.url}" width="100">')
    


class maintenancemodel(models.Model):
    car_id = models.ForeignKey(cars, on_delete=models.CASCADE)
    emp_id = models.ForeignKey(registermodel, on_delete=models.CASCADE)

    BATTERY_HEALTH_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor'),
    ]
    TIRE_CONDITION_CHOICES = [
        ('New', 'New'),
        ('Good', 'Good'),
        ('Worn', 'Worn'),
        ('Replace', 'Replace'),
    ]
    BRAKE_SYSTEM_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor'),
    ]
    battery_health = models.CharField(max_length=100, choices=BATTERY_HEALTH_CHOICES, default='Good')
    charging_history = models.TextField(default="No records yet")
    mileage = models.IntegerField(default=0)
    tire_condition = models.CharField(max_length=100, choices=TIRE_CONDITION_CHOICES, default='Good')
    brake_system = models.CharField(max_length=100, choices=BRAKE_SYSTEM_CHOICES, default='Good')
    service_history = models.TextField(default="No service history")
    inspection_date = models.DateField(default=current_date)


class BookingModel(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    user_id = models.ForeignKey(registermodel, on_delete=models.CASCADE)
    u_email = models.EmailField(default=None)
    vehicle_id = models.ForeignKey(cars, on_delete=models.CASCADE)
    rental_date = models.DateField(default=current_date)
    pickup_loc = models.CharField(max_length=255, default="Not specified", null=False)
    drop_loc = models.CharField(max_length=255, default="Not specified", null=False)
    return_date = models.DateField(default=current_date)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Booking #{self.user_id.u_name}"


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp

class review(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp

class gallery(models.Model):
    g_img = models.ImageField(upload_to='gallery/', null=True, blank=True)
    g_name = models.TextField()

    def gallery_pic(self):
        return mark_safe(f'<img src="{self.g_img.url}" width="100">')
    

class Payment(models.Model):
    booking = models.OneToOneField(BookingModel, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id}"
    


class feedReview(models.Model):
    booking = models.ForeignKey(BookingModel, on_delete=models.CASCADE)
    user = models.ForeignKey(registermodel, on_delete=models.CASCADE)
    vehicleid = models.ForeignKey(cars, on_delete=models.CASCADE)
    rating = models.IntegerField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.u_name} - {self.rating} Stars"