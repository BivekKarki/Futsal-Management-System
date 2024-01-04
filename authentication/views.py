from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from authentication.models import Consumer


# Create your views here.
def consumer_login_view(request):
    if request.method == "POST":
        print("Hello bivek")
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = authenticate(username=phone, password=password)
        if user is not None:
            login(request, user)
            # messages.info(request, f"You are now logged in as {username}.")
            return redirect("/authentication/consumer_dashboard")
        else:
            print("no user")
            messages.error(request, "Invalid phone or password.")

        # print(f"Phone Number: {phone}")
        # try:
        #     user = Consumer.objects.get(phone=phone)
        #     print(type(user))
        #     if user.check_password(password):
        #         login(request, user)
        #         # Redirect to a success page or dashboard
        #         return redirect("/authentication/consumer_dashboard")
        #     else:
        #         # Incorrect password
        #         return render(request, 'login.html', {'error': 'Invalid password'})
        # except Consumer.DoesNotExist:
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
