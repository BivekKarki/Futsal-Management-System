from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from futsalOwner.models import FutsalOwner
from futsalOwner.forms import OwnerLoginForm


# Create your views here.
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
                                consumer_profile = FutsalOwner.objects.get(email=email)
                                request.session['consumer_id'] = consumer_profile.consumer_id
                                return redirect("/authentication/consumer_dashboard")

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