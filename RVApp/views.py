from django.shortcuts import render
from .models import *
from datetime import datetime,date,timedelta
import json
import razorpay
from django.conf import settings


# Create your views here.
def checksession(request):
    uid = request.session.get('log_id')

    if not uid:
        return None

    try:
        userdata = registermodel.objects.get(id=uid)
        is_employee = userdata.role == "Employee"


        context = {
            'userdata': userdata,
            'is_employee': is_employee,
        }
        return context
    except registermodel.DoesNotExist:
        return None


def login_register_page(request):
    return render(request, "Login_Register.html")

# Registertion
from django.shortcuts import render, redirect
from .models import registermodel
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def fetchregister(request):
    if request.method == "POST":
        u_name = request.POST.get('u_name')
        u_email = request.POST.get('u_email')
        u_phone = request.POST.get('u_phone')
        u_address = request.POST.get('u_address')
        u_password = request.POST.get('u_password')
        role = request.POST.get('role')  # User or Employee

        user = registermodel(
            u_name=u_name,
            u_email=u_email,
            u_phone=u_phone,
            u_address=u_address,
            u_password=u_password,
            role=role,
        )

        if 'id_proof1' in request.FILES:
            id_proof = request.FILES['id_proof1']
            user.id_proof = id_proof

        # Save user based on their role
        if role == 'Employee':
            messages.info(request, 'Registration done successfully. Please wait for your profile approval. It will take around 2-3 days.')
        else:
            messages.success(request, 'Data inserted successfully. You can login now.')

        user.save()

        return redirect('/fetchregister')
    return render(request, "Login_register.html")

def login(request):
    if request.method == "POST":
        Email1 = request.POST['email2']
        Password1 = request.POST['password2']
        try:
            user = registermodel.objects.get(u_email=Email1, u_password=Password1)

        except registermodel.DoesNotExist:
            user = None

        if user is not None:
            if user.role == "Employee" and user.status == "0":
                print(user.role)
                print(user.status)
                messages.error(request, 'Your Profile is Under Approval Process. This may take upto 3 working days.')
            else:
                request.session['log_id'] = user.id
                request.session['log_name'] = user.u_name
                request.session['log_email'] = user.u_email
                request.session['log_role'] = user.role

                request.session.save()
                messages.success(request, 'Login successful...')
                return redirect('/')
        else:
            messages.error(request, 'Invalid Email Id and Password. Please try again.')
            return redirect('/login')

    return render(request,'Login_register.html')

def logout(request):
    try:
        del request.session['log_id']
        del request.session['log_name']
        del request.session['log_email']
        del request.session['log_role']

        messages.success(request,'your logout successfully.')
    except:
        pass
    return redirect("/")

def fetchvehicledata(request):

    vehicle_image = request.FILES["vehicle_image"]
    make = request.POST.get("make")
 
    v_name = request.POST.get("v_name")
    description = request.POST.get("description")
    seats = request.POST.get("seats")
    vehicle_type = request.POST.get("vehicle_type")
    stock_no = request.POST.get("stock_no")
    doors = request.POST.get("doors")
    year = request.POST.get("mileage")
    mileage = request.POST.get("mileage")
    color = request.POST.get("color")
    VIN = request.POST.get("VIN")
    price = request.POST.get("price")
    status = request.POST.get("status")

    insert_query = cars(vehicle_image=vehicle_image,make=make, v_name=v_name, description=description, seats=seats, vehicle_type=vehicle_type, stock_no=stock_no, doors=doors, year=year, mileage=mileage, color=color ,VIN=VIN, price=price, status=status )
    insert_query.save()
    messages.success(request, "Data Inserted Successdully!..")
    return render(request, "addcart.html")

def fetchmaintanancedata(request):
    car_id = request.POST.get("car_id")
    emp_id = request.session['log_id']
    battery_health = request.POST.get("battery_health")
    charging_history = request.POST.get("charging_history")
    mileage = request.POST.get("mileage")
    tire_condition = request.POST.get("tire_condition")
    brake_system = request.POST.get("brake_system")
    service_history = request.POST.get("service_history")
    inspection_date = request.POST.get("inspection_date")

    insert_query = maintenancemodel(
        car_id=cars(id=car_id),
        emp_id=registermodel(id=emp_id),
        battery_health=battery_health,
        charging_history=charging_history,
        mileage=mileage,
        tire_condition=tire_condition,
        brake_system=brake_system,
        service_history=service_history,
        inspection_date=inspection_date
    )
    insert_query.save()
    messages.success(request, "Data Inserted Successdully!..")
    return render(request, "Maintanace.html")

def fetchcontactdata(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    message = request.POST.get("message")

    insert_query = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
    insert_query.save()
    return render(request, "contact-us.html")

def index_page(request):
    return render(request, "index.html")

def car_list_page(request):
    all_cars = cars.objects.all()
    context = {
        "car" : all_cars
    }
    return render(request,"car-list.html", context)

def add_car_page(request):
    return render(request,"addcart.html")


def contact_page(request):
    return render(request, "contact-us.html")

def maintain_page(request):
    fetchdata = cars.objects.all()
    context  = {
        "mdata": fetchdata
    }
    return render(request, "Maintanace.html", context)

def single_car(request, id):
    singleCar = cars.objects.get(id=id)
    context ={
        "data": singleCar
    }
    return render(request, "listing-details.html", context)


def review(request):
    return render(request, "listing-details.html")

def fetchreview(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    text = request.POST.get("text")
    
    insert_query = review(
        name=name,
        email=email,
        text=text,
    )
    insert_query.save()
    return render(request, "listing-details.html")

def cargallery(request):
    fetchinfo = gallery.objects.all()
    context = {
        "gdata" : fetchinfo
    }
    return render(request, "gallery.html", context)

def fetchgallery(request):
    return render(request, "addgallery.html")


def fetchgallarydata(request):
    g_img = request.FILES["g_img"]
    g_name = request.POST.get("g_name")

    insert_query = gallery(
        g_img = g_img,
        g_name = g_name,
    )
    insert_query.save()
    return redirect("/cargallery")

def booking(request,bookid):
    fetchdata = cars.objects.get(id=bookid)
    uid = request.session["log_id"]
    user = registermodel.objects.get(id=uid)
    context = {
        "data": fetchdata,
        "userdata":user
    }
    return render(request, "booking.html",context)




def book_car_view(request):
    if request.method == "POST":
        try:
            
            user_id = request.POST.get("user_id")
            vehicle_id = request.POST.get("vehicle_id")
            rental_date_str = request.POST.get("rental_date")
            return_date_str = request.POST.get("return_date")
            pickup_loc = request.POST.get("pickup_loc")
            drop_loc = request.POST.get("drop_loc")

            rental_date = datetime.strptime(rental_date_str, "%Y-%m-%d").date()
            return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()

          
            tomorrow = date.today() + timedelta(days=1)
            if rental_date < tomorrow:
                messages.error(request, "Rental date must be at least tomorrow.")
                return redirect("booking")  

            if return_date <= rental_date:
                messages.error(request, "Return date must be after rental date.")
                return redirect("booking")

            user = registermodel.objects.get(id=user_id)
            vehicle = cars.objects.get(id=vehicle_id)

            existing_bookings = BookingModel.objects.filter(
            vehicle_id=vehicle_id,
            status__in=['Pending', 'Confirmed'],
            rental_date__lte=return_date,
            return_date__gte=rental_date
            )

            if existing_bookings.exists():
                messages.error(request, "This vehicle is already booked for the selected date(s). Please choose a different range.")
                return redirect('single_car', id=vehicle_id)
       
            rental_days = (return_date - rental_date).days
            total_cost = rental_days * float(vehicle.price)
            BookingModel.objects.create(
                user_id=user,
                u_email=user.u_email,
                vehicle_id=vehicle,
                rental_date=rental_date,
                return_date=return_date,
                pickup_loc=pickup_loc,
                drop_loc=drop_loc,
                total_cost=total_cost,
                status="Pending"
            )

            messages.success(request, "Booking successful!")
            return redirect(index_page)  

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect("booking")

    return render(request, "booking.html")



def my_bookings_view(request):
    user = request.session["log_id"]
    bookings = BookingModel.objects.filter(user_id__id=user)

    # Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Attach order_id for pending payments
    for booking in bookings:
        if booking.status == "Pending":
            amount = int(booking.total_cost * 100)  # in paise
            payment, created = Payment.objects.get_or_create(booking=booking, defaults={'amount': booking.total_cost})
            if created or not payment.razorpay_order_id:
                order = client.order.create({
                    "amount": amount,
                    "currency": "INR",
                    "payment_capture": "1"
                })
                payment.razorpay_order_id = order['id']
                payment.save()

    return render(request, "my_bookings.html", {
        "bookings": bookings,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })

def payment_success(request):
    if request.method == "POST":
        data = json.loads(request.body)
        booking_id = data.get("booking_id")
        booking = BookingModel.objects.get(id=booking_id)
        payment = Payment.objects.get(booking=booking)

        payment.razorpay_payment_id = data.get("razorpay_payment_id")
        payment.razorpay_order_id = data.get("razorpay_order_id")
        payment.razorpay_signature = data.get("razorpay_signature")
        payment.is_paid = True
        payment.save()

        booking.status = "Confirmed"
        booking.save()

        return redirect(my_bookings_view)
    

    

from django.shortcuts import render, redirect, get_object_or_404
# def leave_review(request, booking_id):
#     booking = get_object_or_404(BookingModel, id=booking_id)

#     # Optional: prevent duplicate review
#     if request.method == 'POST':
#         rating = request.POST.get('rating')
#         message = request.POST.get('message')
#         uid = request.session["log_id"]
#         user = registermodel.objects.get(id=uid)

#         if rating and message:
#             feedReview.objects.create(
#                 user=user,
#                 booking=booking,
#                 vehicleid=booking.vehicle_id,
#                 rating=int(rating),
#                 message=message
#             )
#             messages.success(request, "Thank you for your feedback!")
#             print(rating)
#             print(message)
#             print(user)
#             return redirect('my_bookings')
#         else:
#             messages.error(request, "All fields are required.")

#     return render(request, 'leave_review.html', {'booking': booking})


def leave_review(request, booking_id):
    booking = get_object_or_404(BookingModel, id=booking_id)

    uid = request.session.get("log_id")
    if not uid:
        messages.error(request, "You must be logged in to leave a review.")
        return redirect("user_login")

    user = get_object_or_404(registermodel, id=uid)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        message = request.POST.get('message')

        if rating and message:
            feedReview.objects.create(
                user=user,
                booking=booking,
                vehicleid=booking.vehicle_id,  # ensure this field name matches your model
                rating=int(rating),
                message=message
            )
            messages.success(request, "Thank you for your feedback!")
            return redirect('my_bookings')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'leave_review.html', {'booking': booking})


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        print("Email:", email)
        print("New password:", new_password)

        try:
            user = registermodel.objects.get(u_email=email)
            print("User found:", user)
            user.u_password = new_password
            user.save()
            print("Password saved")

            messages.success(request, "Password updated successfully! Please login.")
        except registermodel.DoesNotExist:
            print("User not found")
            messages.error(request, "User does not exist with the provided email.")

        return redirect('/')