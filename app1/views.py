from django.shortcuts import render, redirect, HttpResponse
from app1.forms import *
from app1.models import Customer, Seller, Goods
from captcha.captcha import captcha
from django.core.cache import cache
import base64


# Create your views here.


def index(request):
    goods = Goods.objects.all()
    data = {"goods": goods}
    if request.session.get("is_login") == 1:
        user = Customer.objects.filter(id=request.session.get("id"))[0]
        data["is_login"] = request.session.get("is_login")
        data["name"] = user.name
        data["id"] = request.session.get("id")
    elif request.session.get("is_login") == 2:
        seller = Seller.objects.filter(id=request.session.get("id"))[0]
        data["is_login"] = request.session.get("is_login")
        data["name"] = seller.name
        data["id"] = request.session.get("id")
    return render(request, "index.html", data)


def buyer_register(request):
    if request.method == "GET":
        return render(request, "buyer_register.html")
    else:
        form = Customer_registerForm(request.POST)
        if Customer.objects.filter(email=request.POST.get("email")):
            return HttpResponse("<script>alert('该邮箱已被注册！');window.history.back(-1);</script>")
        if Customer.objects.filter(name=request.POST.get("name")):
            return HttpResponse("<script>alert('该邮箱已被注册！');window.history.back(-1);</script>")
        if form.is_valid():
            print("LLLL")
            name = request.POST.get("name")
            password = request.POST.get("password")
            email = request.POST.get("email")
            sex = request.POST.get("sex")
            Customer.objects.create(name=name, password=password, email=email, sex=sex)
            return HttpResponse("<script>alert('注册成功！');window.location.href='/index/';</script>")
        else:
            print(form.errors)
            data = {"form": form}
            return render(request, "buyer_register.html", data)


def seller_register(request):
    if request.method == "GET":
        return render(request, "seller_register.html")
    else:
        form = Seller_registerForm(request.POST)
        if Seller.objects.filter(email=request.POST.get("email")):
            return HttpResponse("<script>alert('该邮箱已被注册！');window.history.back(-1);</script>")
        if Seller.objects.filter(name=request.POST.get("name")):
            return HttpResponse("<script>alert('该用户名已被注册！');window.history.back(-1);</script>")
        if form.is_valid():
            name = request.POST.get("name")
            password = request.POST.get("password")
            email = request.POST.get("email")
            sex = request.POST.get("sex")
            Seller.objects.create(name=name, password=password, email=email, sex=sex)
            return HttpResponse("<script>alert('注册成功！');window.location.href='/index/';</script>")
        else:
            print(form.errors)
            data = {"form": form}
            return render(request, "seller_register.html", data)


def buyer_login(request):
    if request.method == "GET":
        text, image = captcha.generate_captcha()
        number = 0
        while cache.has_key("k%d" % number):
            number += 1
        cache.set("k%d" % number, text, 3000)
        image = base64.b64encode(image).decode()
        data = {"k": number, "image": image}
        return render(request, "buyer_login.html", data)

    else:
        form = Customer_loginForm(request.POST)
        k = "k" + request.POST.get("k")
        if not cache.has_key(k):
            return HttpResponse("<script>alert('验证码已过期！');window.location.href='/buyer_login/';</script>")
        if form.is_valid():
            v_code = cache.get(k)
            if v_code != request.POST.get("verify_code").upper():
                cache.delete(k)
                return HttpResponse("<script>alert('验证码错误！');window.location.href='/buyer_login/';</script>")
            name = request.POST.get("name")
            password = request.POST.get("password")
            user = Customer.objects.filter(name=name)
            if user:
                user = Customer.objects.filter(name=name, password=password)
                if user:
                    cache.delete(k)
                    request.session['is_login'] = 1
                    request.session["id"] = user[0].id
                    return redirect("/index/")
                else:
                    return HttpResponse("<script>alert('密码错误嗷！');window.location.href='/buyer_login/';</script>")
            else:
                return HttpResponse("<script>alert('该用户名尚未注册！');window.location.href='/buyer_login/';</script>")
        else:
            print(form.errors.as_json)
            data = {"form": form}
            return render(request, "buyer_login.html", data)


def seller_login(request):
    if request.method == "GET":
        text, image = captcha.generate_captcha()
        number = 0
        while cache.has_key("k%d" % number):
            number += 1
        cache.set("k%d" % number, text, 3000)
        image = base64.b64encode(image).decode()
        data = {"k": number, "image": image}
        return render(request, "seller_login.html", data)

    else:
        form = Seller_loginForm(request.POST)
        k = "k" + request.POST.get("k")
        if not cache.has_key(k):
            return HttpResponse("<script>alert('验证码已过期！');window.location.href='/seller_login/';</script>")
        if form.is_valid():
            v_code = cache.get(k)
            if v_code != request.POST.get("verify_code").upper():
                cache.delete(k)
                return HttpResponse("<script>alert('验证码错误！');window.location.href='/seller_login/';</script>")
            name = request.POST.get("name")
            password = request.POST.get("password")
            user = Seller.objects.filter(name=name)
            if user:

                user = Seller.objects.filter(name=name, password=password)
                if user:
                    cache.delete(k)
                    request.session['is_login'] = 2
                    request.session["id"] = user[0].id
                    return redirect("/index/")
                else:
                    return HttpResponse("<script>alert('密码错误嗷！');window.location.href='/seller_login/';</script>")
            else:
                return HttpResponse("<script>alert('该用户名尚未注册！');window.location.href='/seller_login/';</script>")
        else:
            print(form.errors.as_json)
            data = {"form": form}
            return render(request, "seller_login.html", data)


def customer_info(request):
    if request.method == "GET":
        form = Customer.objects.last()
        return render(request, "customer_info.html", {"form": form})
    else:
        return render(request, "customer_info.html")


def seller_info(request):
    if request.method == "GET":
        form = Seller.objects.filter(id=request.session.get("id"))[0]
        return render(request, "seller_info.html",{'form':form})
    else:
        return render(request, "seller_info.html")


def good_info(request, id):
    good = Goods.objects.filter(id=id)[0]
    if not good:
        return HttpResponse("<script>alert('该商品不存在！');window.location.href='/index/';</script>")
    return render(request, "good_info.html", {"good": good})

def logout(request):
    if request.session.get("is_login"):
        request.session.flush()
        return redirect('/index/')
    else:
        return HttpResponse("<script>alert('请先登录!');window.location.href='/login/';</script>")

def create_good(request):
     if request.method == "GET":
        return render(request,"create_good.html")
     else:
         image = request.POST.get("item_img")
         item_name = request.POST.get("item_name")
         item_introdcution = request.POST.get("item_introduction")
         item_price = request.POST.get("item_price")
         number = request.POST.get("number")
         category_id = request.POST.get("category_id")
         print(image)
         if not item_name:
             return HttpResponse("<script>alert('请输入商品名');window.history.back(-1)</script>")
         if not image:
             return HttpResponse("<script>alert('请上传图片');window.history.back(-1)</script>")
         if not item_introdcution:
             return HttpResponse("<script>alert('请输入商品介绍！');window.history.back(-1)</script>")
         if not category_id:
             return HttpResponse("<script>alert('请选择分类标签！');window.history.back(-1)</script>")
         if not number:
             return HttpResponse("<script>alert('请输入库存！');window.history.back(-1)</script>")

         Goods.objects.create(item_name=item_name,item_introdcution=item_introdcution,seller_id=request.session.get("id"),item_price=item_price)
         return render(request, "create_good.html")
