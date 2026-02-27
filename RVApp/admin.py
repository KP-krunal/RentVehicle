from calendar import month


from django.contrib import admin
from RVApp.models import *
from RVApp.views import contact_page


# Register your models here.

class showRegister(admin.ModelAdmin):
    list_display = ["u_name", "u_email", "u_phone", "u_address", "u_password","role", "status","pic"]

admin.site.register(registermodel, showRegister)

class showVehicleData(admin.ModelAdmin):
    list_display = ["v_name", "description","make", "seats", "vehicle_type", "stock_no", "doors", "year", "mileage", "color" ,"VIN", "price", "status","vehicle_pic"]

admin.site.register(cars, showVehicleData)

class showMaintainanceData(admin.ModelAdmin):
    list_display = ["car_id", "emp_id", "battery_health", "charging_history", "mileage", "tire_condition", "brake_system", "service_history", "inspection_date"]

admin.site.register(maintenancemodel, showMaintainanceData)

class showbooking(admin.ModelAdmin):
    list_display = ["user_id", "u_email",  "vehicle_id", "rental_date", "pickup_loc", "drop_loc", "return_date", "total_cost", "status"]

admin.site.register(BookingModel, showbooking)

class showcontact(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "message", "created_at"]

admin.site.register(Contact, showcontact)





class showgallery(admin.ModelAdmin):
    list_display = ["gallery_pic", "g_name"]

admin.site.register(gallery, showgallery)


class showpayment(admin.ModelAdmin):
    list_display = ["booking", "razorpay_order_id", "razorpay_payment_id", "razorpay_signature", "amount", "is_paid"]

admin.site.register(Payment, showpayment)



class showfeedreviews(admin.ModelAdmin):
    list_display = ["booking", "user", "vehicleid", "rating", "message"]

admin.site.register(feedReview, showfeedreviews)