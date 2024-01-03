from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from authentication.models import Consumer


# Create your views here.
def consumer_login_view(request):
    if request.method == "POST":
        print("Hello bivek")
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = authenticate(phone=phone, password=password)
        if user is not None:
            login(request, user)
            # messages.info(request, f"You are now logged in as {username}.")
            return redirect("/authentication/consumer_dashboard")
        else:
            print("no user")
            messages.error(request, "Invalid phone or password.")

        # try:
        #     consumer = Consumer.objects.filter(phone=phone, password=password)
        #     print(consumer)
        #     return redirect("/authentication/consumer_dashboard")
        # except:
        #     print("error")
        #     return render(request=request, template_name="login.html")

    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def consumer_dashboardview(request):
    # get the logged-in consumer
    # id = request.session.get('id')
    # consumer = Consumer.objects.get(id=id)

    success_message = request.session.pop('success_message', None)

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

        print(id)

        Consumer.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address,
            password=password
        )
        # print("user created!")
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect("/authentication/consumer_login")

    return render(request, "userSignupForm.html")
