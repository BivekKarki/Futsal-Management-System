import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from FutsalManagementSystem import settings
from authentication.tokens import account_activation_token

from futsalOwner.models import FutsalOwner
from futsalOwner.forms import OwnerLoginForm


# Create your views here.
def owner_registration_formview(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        password = request.POST.get("password")
        c_password = request.POST.get("c_password")

        if password != c_password:
            messages.error(request, "Password mismatched!")
            return render(request, "userSignupForm.html", {"message": "password not matching"})
        elif FutsalOwner.objects.filter(phone=phone).exists():
            messages.error(request, "This phone number is already exist!")
            return render(request, "userSignupForm.html")
        elif FutsalOwner.objects.filter(email=email).exists():
            messages.error(request, "This email address is already exist!")
        elif User.objects.filter(username=phone).exists():
            messages.error(request, "This phone number is already exist!")
            return render(request, "userSignupForm.html")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "This email address is already exist!")
            return render(request, "userSignupForm.html")

        user = FutsalOwner(
            name=name,
            phone=phone,
            email=email,
            password=password
        )

        uidb64 = urlsafe_base64_encode(force_bytes(user.email))
        domain = get_current_site(request).domain
        link = reverse("futsalOwner:activate", kwargs={"uidb64": uidb64, "token": account_activation_token.make_token(user), })
        email_subject = "Activate your account"
        activate_url = "http://"+domain+link
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        mydict = {"username": user.name, "activate_url": activate_url}
        html_template = "account_activation.html"
        html_message = render_to_string(html_template, context=mydict)

        email_message = EmailMessage(email_subject, html_message, email_from, recipient_list)
        email_message.content_subtype = "html"
        email_message.send()

        owner = User.objects.create_user(username=phone, first_name=name, email=email, password=password)
        owner.first_name = name
        owner.phone = phone
        owner.save()

        FutsalOwner.objects.create(
            user=owner,
            name=name,
            phone=phone,
            email=email,
            address=address,
            password=password
        )

        messages.success(request, 'Registration successful! Please check your email to activate your account.')
        return redirect("/authentication/consumer_login")

    return render(request, "userSignupForm.html")


def verification_view(request, uidb64, token):
    try:
        email = force_str(urlsafe_base64_decode(uidb64))
        user = FutsalOwner.objects.get(email=email)
        if user.status:
            messages.success(request, 'Account Already Activated')
            return redirect("futsalOwner:owner_login")
        else:
            user.status = True
            user.save()
            messages.success(request, 'Account Activated Successfully!')
    except Exception as ex:
        pass
    return redirect("futsalOwner:owner_login")

def owner_login_view(request):
    # print("Welllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")
    if request.method == "POST":
        form = OwnerLoginForm(request.POST)
        print(form.is_valid())
        print("Hello Owner")
        if form.is_valid():
            # phone = request.POST.get("phone")  # Use phone instead of email
            # password = request.POST.get("password")
            email = form.cleaned_data['email']  # Use phone instead of email
            password = form.cleaned_data['password']
            captcha = form.cleaned_data['captcha']
            print("Good")
            # Perform reCAPTCHA validation

            if captcha:

                try:
                    c_user = User.objects.get(email=email)
                    print(c_user.check_password(password))
                    owner = FutsalOwner.objects.get(email=email)
                    if c_user:
                        # if password == user.password:
                        if not owner.status:
                            messages.error(request, "Account is not Activated!")
                        elif password == c_user.password:
                            messages.error(request, "Invalid Credentials!p")
                        else:
                            username = User.objects.get(email=email)

                            user = authenticate(username=username, password=password)
                            if not user:
                                messages.error(request, "Invalid Credentials! not")
                            else:
                                login(request, user)
                                messages.success(request, 'Login successful. Welcome!')
                                owner_profile = FutsalOwner.objects.get(email=email)
                                request.session['owner_id'] = owner_profile.owner_id
                                return redirect("/futsalOwner/owner_dashboard")

                    else:
                        messages.error(request, "Invalid Credentials!")
                except User.DoesNotExist:
                    messages.error(request, 'Invalid Credentials!2')

            else:
                messages.error(request, "Invalid recaptcha")
    else:
        form = OwnerLoginForm()
        # print("invalid form")
    # form = AuthenticationForm()
    return render(request, "futsalOwner/Ownerlogin.html", {"login_form": form})


@login_required()
def owner_dashboardview(request):
    success_message = messages.get_messages(request)
    consumer_id = request.session.get('consumer_id')

    owner = FutsalOwner.objects.get(consumer_id=consumer_id)
    context = {
        'success_message': success_message,
        'owner': owner,
    }
    print("Dashboard")
    return render(request, 'futsalOwner/ownerDashboard.html', context)