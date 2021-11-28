from django.shortcuts import render


# Create your views here.

def index(requests):
    return render(requests, "index.html")


def buyer_register(requests):
    if requests.method == "GET":
        return render(requests, "buyer_register.html")


def seller_register(requests):
    if requests.method == "GET":
        return render(requests, "seller_register.html")


def buyer_login(requests):
    if requests.method == "GET":
        return render(requests, "buyer_login.html")
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = request.POST.get("user_name")
            user_password = request.POST.get("user_password")
            try:
                User.objects.get(user_name=user_name)
            except User.DoesNotExist:
                data = {"errmsg": "该用户名未注册，请注册！"}
                return render(request, "login.html", data)

            user = User.objects.filter(user_name=user_name, user_password=user_password)
            if user:
                request.session['is_login'] = True
                request.session["id"] = user[0].id
                return redirect("/index/")
            else:
                data = {"errmsg": "密码错误嗷！", "form": form}
                return render(request, "login.html", data)
        else:
            data = {"form": form}
            return render(request, "login.html", data)


def seller_login(requests):
    if requests.method == "GET":
        return render(requests, "seller_login.html")
