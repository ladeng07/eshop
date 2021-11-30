from django.shortcuts import render,redirect,HttpResponse
from app1.forms import Customer_loginForm,Seller_loginForm,Customer_registerForm
from app1.models import Customer,Seller

# Create your views here.

def index(request):
    return render(request, "index.html")


def buyer_register(request):
    if request.method == "GET":
        return render(request, "buyer_register.html")
    else:
        form = Customer_registerForm(request.POST)
        print(request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            password = request.POST.get("password")
            email = request.POST.get("email")
            sex = request.POST.get("sex")
            Customer.objects.create(name=name,password=password,email=email,sex=sex)
            return HttpResponse("<script>alert('注册成功！');window.location.href='/index/';</script>")
        else:
            print(form.errors)
            data = {"form": form}
            return render(request, "buyer_register.html", data)


def seller_register(request):
    if request.method == "GET":
        return render(request, "seller_register.html")


def buyer_login(request):
    if request.method == "GET":
        return render(request, "buyer_login.html")
    else:
        form = Customer_loginForm(request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            password = request.POST.get("password")
            user = Customer.objects.filter(name=name)
            if user:
                user = Customer.objects.filter(name=name, password=password)
                if user:
                    request.session['is_login'] = True
                    request.session["id"] = user[0].id
                    return redirect("/index/")
                else:
                    data = {"errmsg": "密码错误嗷！", "form": form}
                    return render(request, "buyer_login.html", data)
            else:
                data = {"errmsg": "该用户名尚未注册", "form": form}
                return render(request, "buyer_login.html", data)
        else:
            print(form.errors.as_json)
            data = {"form": form}
            return render(request, "buyer_login.html", data)


def seller_login(request):
    if request.method == "GET":
        return render(request, "seller_login.html")
    else:
        form = Seller_loginForm(request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            password = request.POST.get("password")
            user = Seller.objects.filter(name=name)
            if user:
                user = Seller.objects.filter(name=name,password=password)
                if user:
                    request.session['is_login'] = True
                    request.session["id"] = user[0].id
                    return redirect("/index/")
                else:
                    data = {"errmsg": "密码错误嗷！", "form": form}
                    return render(request, "seller_login.html", data)
            else:
                data = {"errmsg": "该用户名尚未注册", "form": form}
                return render(request, "seller_login.html", data)
        else:
            print(form.errors.as_json)
            data = {"form": form}
            return render(request, "seller_login.html", data)

def customer_info(request):
    if request.method == "GET":
        return render(request,"customer_info.html")
    else:
        return render(request,"customer_info.html")


def seller_info(request):
    if request.method == "GET":
        return render(request, "seller_info.html")
    else:
        return render(request, "seller_info.html")
