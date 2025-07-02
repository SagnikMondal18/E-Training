from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.conf import settings
from django.template.defaulttags import register
from django.views.decorators.csrf import csrf_exempt
import razorpay

from .models import Course, Enrollment, Payment, Video
from .forms import CustomerRegistrationForm

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Home Page View
def home(request):
    return render(request, "app/home.html")

# About Page View
def about(request):
    return render(request, "app/about.html")

# Course List View (with Login Required)
@method_decorator(login_required(login_url='login'), name='dispatch')
class CourseView(View):
    def get(self, request):
        courses = Course.objects.filter(active=True)  # Fetch only active courses
        return render(request, "app/courses.html", {'courses': courses})

# Course Detail View (with Login Required)
class CourseDetailView(View):
    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        lectures = Video.objects.filter(course=course)
        enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
        trainer = course.trainer  # Correctly fetching the trainer

        context = {
            'course': course,
            'lectures': lectures,
            'enrolled': enrolled,
            'trainer': trainer,  # Passing the trainer to the template
        }
        return render(request, "app/course_details.html", context)

# Enroll View (Handles Payment Creation and Enrollment)
@method_decorator(login_required(login_url='login'), name='dispatch')
class EnrollView(View):
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

        if created:
            amount = course.price * 100  # Razorpay uses the smallest currency unit (paise)
            razorpay_order = razorpay_client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": 1
            })

            # Save the payment information
            Payment.objects.create(
                order_id=razorpay_order['id'],
                user=request.user,
                course=course,
                status=False
            )

            context = {
                'course': course,
                'order_id': razorpay_order['id'],
                'amount': amount,
                'razorpay_key': settings.RAZORPAY_KEY_ID,
            }
            return render(request, 'app/payment.html', context)
        else:
            messages.warning(request, f"You are already enrolled in {course.name}.")
            return redirect('course_details', id=course.id)

# Payment Verification View
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        payment_data = request.POST
        order_id = payment_data.get('order_id')
        payment_id = payment_data.get('razorpay_payment_id')

        payment = get_object_or_404(Payment, order_id=order_id)
        try:
            # Verify Razorpay payment signature
            razorpay_client.utility.verify_payment_signature(payment_data)

            # Update payment details on successful verification
            payment.payment_id = payment_id
            payment.status = True
            payment.save()

            messages.success(request, "Payment successful!")
            return redirect('course_details', id=payment.course.id)
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed!")
            return redirect('course_details', id=payment.course.id)

# User Registration View
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", {'form': form})
        
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been registered successfully.")
            return redirect("login")
        else:
            messages.warning(request, "Please correct the errors below.")
        return render(request, "app/customerregistration.html", {'form': form})

# User Login View
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('courses')
        form = AuthenticationForm()
        return render(request, "app/login.html", {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("courses")
        else:
            messages.error(request, "Invalid username or password.")
        return render(request, "app/login.html", {'form': form})

# User Logout View
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('login')
    




# Custom template filter
@register.filter
def multiply(value, arg):
    return value * arg
