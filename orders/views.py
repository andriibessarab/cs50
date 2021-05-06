from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail

from django.contrib.auth.models import User
from .models import RegularPizza, SicilianPizza, Topping, Sub, Pasta, Salad, DinnerPlatter, Order

import ast
# Create your views here.

message = None

def index(request):
    if request.user.is_authenticated == True:
        if request.user.is_staff == True:
            ordersQS = Order.objects.all()
            orders = []
            for o in ordersQS:
                order = {}
                order["id"] = o.ID
                order["user"] = o.user
                order["total"] = o.total
                order["order"] = ast.literal_eval(o.order)
                orders.append(order)
            context = {
                "admin": True,
                "authorized": False,
                "allOrders": orders,
            }
            return render(request, "orders/main.html", context)
        else:
            context = {
                "authorized": True,
                "user": request.user,
                "RegularPizza": RegularPizza.objects.all(),
                "SicilianPizza": SicilianPizza.objects.all(),
                "Toppings": Topping.objects.all(),
                "Subs": Sub.objects.all(),
                "Pasta": Pasta.objects.all(),
                "Salads": Salad.objects.all(),
                "DinnerPlatters": DinnerPlatter.objects.all(),
            }
            return render(request, "orders/main.html", context)
    else:
        global message
        context = {
            "authorized": False,
            "message": message,
        }
        message = None
        return render(request, "orders/main.html", context)


def registerProcess(request):
    if request.method == "GET":
        return HttpResponseRedirect("/")
    else:
        global message
        try:
            username = request.POST["username"]
            email = request.POST["email"]
            firstName = request.POST["firstName"]
            lastName = request.POST["lastName"]
            password = request.POST["password"]
            user = User.objects.create_user(
                username, email, password, first_name=firstName, last_name=lastName)
            user.save()
            send_mail('Welcome to Crusty Pizza!', f"Thank you for regeistering in our application. From now on, you can order the best pizza(and not only) as many times as you want to!\nHere are your credentials:\nUsername: {username}\nPassword:{password}\nDont loose them!", 'andrii.bessarab@fcae.ca', [f'{str(email)}'], fail_silently=True)
            return HttpResponseRedirect("/")
        except IntegrityError:
            message = "This username is already taken! Try a different one!"
            return HttpResponseRedirect("/")


def loginProcess(request):
    if request.method == "GET":
        return HttpResponseRedirect("/")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            global message
            message = "No such user has been found. Try again!"
            return HttpResponseRedirect("/")


def logoutProcess(request):
    if request.method == "GET":
        return HttpResponseRedirect("/")
    else:
        logout(request)
    return HttpResponseRedirect("/")


def placeOrder(request):
    if request.method == "GET":
        return HttpResponseRedirect("/")
    else:
        cart = request.POST["cart"]
        total = float(request.POST["total"])
        f = Order(user=request.user, order=cart, total=total)
        f.save()
        orderStr = ""
        order = ast.literal_eval(f.order)
        for i in order:
            name = i["name"]
            size = i["size"]
            toppings = str(i["toppings"]).replace("'", "")
            price = i["price"]
            item = f"{name} {size} {toppings} ${price}".replace("[]", "").replace("   ", " ").replace("   ", " ")
            orderStr = orderStr + item + "\n"
        send_mail('Order Confirmation', f"We recieved your order and we'll deliver it to you a.s.a.p!\nYour order number is #{f.ID}\nYour order: {orderStr}Total: ${total}\nThank you!", 'andrii.bessarab@fcae.ca', [f'{request.user.email}'], fail_silently=True)
        return HttpResponseRedirect("/")
