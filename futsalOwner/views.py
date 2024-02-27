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
        print("Hello bivek")
        if form.is_valid():
            # phone = request.POST.get("phone")  # Use phone instead of email
            # password = request.POST.get("password")
            email = form.cleaned_data['email']  # Use phone instead of email
            password = form.cleaned_data['password']
            captcha = form.cleaned_data['captcha']
            print("Good")
            # Perform reCAPTCHA validation

            if captcha:
                c_user = User.objects.get(email=email)
                owner = FutsalOwner.objects.get(email=email)
                try:
                    if c_user:
                        # if password == user.password:
                        if not owner.status:
                            messages.error(request, "Account is not Activated!")
                        else:
                            username = User.objects.get(email=email)

                            user = authenticate(username=username, password=password)

                            login(request, user)
                            messages.success(request, 'Login successful. Welcome!')
                            owner_profile = FutsalOwner.objects.get(email=email)
                            request.session['owner_id'] = owner_profile.owner_id
                            return redirect("/authentication/consumer_dashboard")

                    else:
                        messages.error(request, "Invalid Credentials!")
                except User.DoesNotExist:
                    messages.error(request, 'User does not exist')

            else:
                messages.error(request, "Invalid recaptcha")
    else:
        form = OwnerLoginForm()
        # print("invalid form")
    # form = AuthenticationForm()
    return render(request, "futsalOwner/Ownerlogin.html", {"login_form": form})