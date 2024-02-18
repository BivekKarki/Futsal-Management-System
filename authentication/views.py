import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

from FutsalManagementSystem import settings
from authentication.models import Consumer


# Create your views here.
def consumer_login_view(request):
    print("Welllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")
    if request.method == "POST":
        print("Hello bivek")
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=phone).exists():
                username = User.objects.get(username=phone)
                user = authenticate(username=username, password=password)
            else:
                messages.error(request, "User does not exist")
                return redirect("/authentication/consumer_login")
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful. Welcome!')
                return redirect("/authentication/consumer_dashboard")
            else:
                print("no user")
                messages.error(request, "Invalid phone or password.")
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def consumer_dashboardview(request):
    success_message = messages.get_messages(request)

    context = {
        'success_message': success_message,
    }

    return render(request, 'userDashboard.html', context)


def consumer_registration_formview(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        password = request.POST.get("password")
        c_password = request.POST.get("c_password")

        if password != c_password:
            return render(request, "userSignupForm.html", {"message": "password not matching"})
        if Consumer.objects.filter(phone=phone).exists():
            messages.error(request, "This phone number is already exist!")
            return render(request, "userSignupForm.html")

        consumer = User.objects.create_user(username=phone, first_name=name, email=email, password=password)
        consumer.first_name = name
        consumer.phone = phone
        consumer.save()

        Consumer.objects.create(
            user=consumer,
            name=name,
            phone=phone,
            email=email,
            address=address,
            password=password
        )
        # print("user created!")
        user = authenticate(request, username=phone, password=password)
        login(request, user)

        messages.success(request, 'Registration successful! You can now log in.')
        return redirect("/authentication/consumer_login")

    return render(request, "userSignupForm.html")


# ====================================== Forgot Password ====================================
def forgot_password_view(request):
    return render(request, 'forgot_password.html')

# ====================================== Send OTP ====================================
def send_otp_view(request):
    error_message = None
    otp = random.randint(11111,99999)
    email = request.POST.get('email')
    user_email = Consumer.objects.filter(email=email)
    if user_email:
        user = Consumer.objects.get(email=email)
        user.otp = otp
        user.save()
        request.session['email'] = request.POST['email']
        html_message = "Your one time password : - " + "" + str(otp)
        subject = "Welcome to Python World"
        email_from = settings.EMAIL_HOST_USER
        email_to = [email]
        message = EmailMessage(subject, html_message, email_from)
        message.send()
        messages.success(request, "Your one time password Send To Your Email")
        return render('enter_otp.html', {'error_message': error_message})
    else:
        error_message = "Invalid Email, Please Enter Correct Email"
        return render(request, 'forgot_password.html')

# ======================= Enter OTP ========================================
def enter_otp(request):
    error_message = None
    if request.session.has_key('email'):
        email = request.session['email']
        user = Consumer.objects.filter(email=email)
        for u in user:
            user_otp = u.otp
        if request.method == "POST":
            otp = request.POST.get('otp')
            if not otp:
                error_message = "OTP is Required"
            elif not user_otp == otp:
                error_message = "Invalid OTP"
            if not error_message:
                return redirect("password_reset")

        return render(request, 'enter_otp.html', {'error_message': error_message})
    else:
        return render(request, 'forgot_password.html')