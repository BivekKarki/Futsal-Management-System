import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

from FutsalManagementSystem import settings
from authentication.forms import LoginForm
from authentication.models import Consumer
from django_recaptcha.fields import ReCaptchaField


# Create your views here.
def consumer_login_view(request):
    # print("Welllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")
    if request.method == "POST":
        form = LoginForm(request.POST)
        print(form.is_valid())
        print("Hello bivek")
        if form.is_valid():
            # phone = request.POST.get("phone")  # Use phone instead of email
            # password = request.POST.get("password")
            phone = form.cleaned_data['phone']  # Use phone instead of email
            password = form.cleaned_data['password']
            captcha = form.cleaned_data['captcha']
            # print(captcha)
            # Perform reCAPTCHA validation
            if captcha:

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
                        consumer_profile = Consumer.objects.get(phone=phone)
                        request.session['consumer_id'] = consumer_profile.consumer_id
                        # print("lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")
                        return redirect("/authentication/consumer_dashboard")
                    else:
                        print("no user")
                        messages.error(request, "Invalid phone or password.")
                except User.DoesNotExist:
                    messages.error(request, 'User does not exist')

            else:
                messages.error(request, "Invalid recaptcha")
    else:
        form = LoginForm()
        # print("invalid form")
    # form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def consumer_dashboardview(request):
    success_message = messages.get_messages(request)
    consumer_id = request.session.get('consumer_id')
    # print(consumer_id)
    consumerr = Consumer.objects.get(consumer_id=consumer_id)
    # consumer = Consumer.objects.all()
    # print(consumerr.name)
    context = {
        'success_message': success_message,
        'consumers': consumerr,
    }
    print("Dashboard")
    return render(request, 'userDashboard.html', context)


def consumer_update_view(request, consumer_id):
    consumer_details = Consumer.objects.get(consumer_id=consumer_id)
    print(consumer_details.consumer_id)
    print(consumer_details.name)
    context = {
        'consumers': consumer_details,
    }
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        user_id = request.POST.get('user_id')

        consumer = Consumer(
            consumer_id=consumer_id,
            user_id=user_id,
            name=name,
            phone=phone,
            email=email,
            password=password,
            address=address
        )
        consumer.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect("consumer_dashboardview")

    return render(request, 'userUpdateForm.html',context)


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
        elif Consumer.objects.filter(phone=phone).exists():
            messages.error(request, "This phone number is already exist!")
            return render(request, "userSignupForm.html")
        elif Consumer.objects.filter(email=email).exists():
            messages.error(request, "This email address is already exist!")
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
    otp = random.randint(11111, 99999)
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
        message = EmailMessage(subject, html_message, email_from, email_to)
        message.send()
        messages.success(request, "Your one time password Send To Your Email")
        return redirect('authentication:enter_otp')
    else:
        error_message = "Invalid Email, Please Enter Correct Email"
        return render(request, 'forgot_password.html', {"error_message": error_message})


# ======================= Enter OTP ========================================
def enter_otp_view(request):
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
                return redirect('authentication:password_reset')
        return render(request, 'enter_otp.html', {'error_message': error_message})
    else:
        return render(request, 'forgot_password.html')


# =========================== Change Password ===================================
def password_reset_view(request):
    error_message = None
    if request.session.has_key('email'):
        email = request.session['email']
        user = Consumer.objects.get(email=email)
        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            if not new_password:
                error_message = "Please enter the password"
            elif not confirm_new_password:
                error_message = "Please enter the confirm password"
            elif new_password != confirm_new_password:
                error_message = "Password Mismatched"
            elif new_password == user.password:
                error_message = "Cannot use old password, try new password"
            elif not error_message:
                user.password = new_password
                user.save()
                messages.success(request, "Password Changed Successfully")
                return redirect("authentication:consumer_login")

    return render(request, 'password_reset.html', {"error_message": error_message})
