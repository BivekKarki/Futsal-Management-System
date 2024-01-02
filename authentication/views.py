from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from authentication.models import Consumer


# Create your views here.
def consumer_login_view(request):
    if request.method == "POST":
        return render(request, "login.html", context={"message": "invalid username or password"})

    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def consumer_dashboardview(request):
    # get the logged-in consumer
    id = request.session.get('id')
    consumer = Consumer.objects.get(id=id)

    success_message = request.session.pop('success_message', None)

    context = {
        'id': id,
        'consumer': consumer,
        'success_message': success_message,
    }

    return render(request, 'userDashboard.html', context)


def consumer_registration_formview(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")

        print(id)

        Consumer.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address
        )
        # print("user created!")
        request.session['success_message'] = "Task successful."
        return redirect("/home/homeview")

    return render(request, "consumer_registration_form.html")
