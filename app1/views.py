from django.shortcuts import render, redirect, HttpResponse, Http404
from app1.forms import *
from app1.models import *
from captcha.captcha import captcha
from django.core.cache import cache
from eshop.settings import MEDIA_ROOT
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.utils import timezone
from app1.tasks import send_email
import base64
import random, os


# Create your views here.
def is_number(s):
    try:
        s = str(float(s))
    except:
        return False
    num = float(s)
    print(len(s.split('.')[1]))
    if num > 0 and len(s.split('.')[1]) < 3:
        return True
    else:
        return False


def index(request):
    if request.method == "GET":
        data = {}
        if request.session.get("is_login") == 1:
            user = Customer.objects.filter(id=request.session.get("id")).first()
            data["is_login"] = request.session.get("is_login")
            data["name"] = user.name
            data["id"] = request.session.get("id")
        elif request.session.get("is_login") == 2:
            seller = Seller.objects.filter(id=request.session.get("id")).first()
            data["is_login"] = request.session.get("is_login")
            data["name"] = seller.name
            data["id"] = request.session.get("id")
        goods = Goods.objects.filter(status=True).order_by("-id")
        paginator = Paginator(goods, 3)
        page_num = request.GET.get('page', 1)
        data["page_obj"] = paginator.get_page(page_num)
        is_paginated = True if paginator.num_pages > 1 else False
        data["is_paginated"] = is_paginated
        try:
            return render(request, "index.html", data)
        except:
            raise Http404()


def buyer_register(request):
    if request.method == "GET" and not request.session.get("is_login"):
        return render(request, "buyer_register.html")
    elif request.session.get("is_login"):
        raise Http404()
    else:
        if request.is_ajax():
            email = request.POST.get("email")
            if not request.POST.get('email'):
                return HttpResponse("??????????????????")
            if Customer.objects.filter(email=email):
                return HttpResponse("?????????????????????")
            if cache.has_key(email):
                return HttpResponse("????????????????????????2???????????????")
            verify_code = str(random.randint(1000, 120))
            cache.set(email, verify_code, 180)
            send_email(request.POST.get("email"), verify_code)
            return HttpResponse("????????????????????????")
        else:
            form = Customer_registerForm(request.POST)
            if Customer.objects.filter(email=request.POST.get("email")):
                return HttpResponse("<script>alert('????????????????????????');window.history.back(-1);</script>")
            if Customer.objects.filter(name=request.POST.get("name")):
                return HttpResponse("<script>alert('????????????????????????');window.history.back(-1);</script>")
            if form.is_valid():
                name = request.POST.get("name")
                password = request.POST.get("password")
                email = request.POST.get("email")
                sex = request.POST.get("sex")
                check_number = request.POST.get("check_number")
                verify_code = cache.get(email)
                if verify_code != check_number:
                    return HttpResponse("<script>alert('?????????????????????');window.history.back(-1);</script>")
                Customer.objects.create(name=name, password=password, email=email, sex=sex)
                return HttpResponse("<script>alert('???????????????');window.location.href='/index/';</script>")
            else:
                print(form.errors)
                data = {"form": form}
                return render(request, "buyer_register.html", data)


def seller_register(request):
    if request.method == "GET" and not request.session.get("is_login"):
        return render(request, "seller_register.html")
    elif request.session.get("is_login"):
        raise Http404()
    else:
        if request.is_ajax():
            email = request.POST.get("email")
            if not request.POST.get('email'):
                return HttpResponse("??????????????????")
            if Seller.objects.filter(email=email):
                return HttpResponse("?????????????????????")
            if cache.has_key("seller" + email):
                return HttpResponse("????????????????????????5???????????????")
            verify_code = str(random.randint(1000, 10000))
            cache.set("seller" + email, verify_code, 180)
            send_email(request.POST.get("email"), verify_code)
            return HttpResponse("????????????????????????")
        else:

            form = Seller_registerForm(request.POST)
            if Seller.objects.filter(email=request.POST.get("email")):
                return HttpResponse("<script>alert('????????????????????????');window.history.back(-1);</script>")
            if Seller.objects.filter(name=request.POST.get("name")):
                return HttpResponse("<script>alert('???????????????????????????');window.history.back(-1);</script>")
            if form.is_valid():
                name = request.POST.get("name")
                password = request.POST.get("password")
                email = request.POST.get("email")
                sex = request.POST.get("sex")
                check_number = request.POST.get("check_number")
                verify_code = cache.get("seller" + email)
                if verify_code != check_number:
                    return HttpResponse("<script>alert('?????????????????????');window.history.back(-1);</script>")
                Seller.objects.create(name=name, password=password, email=email, sex=sex)
                cache.delete("seller" + email)
                return HttpResponse("<script>alert('???????????????');window.location.href='/index/';</script>")
            else:
                print(form.errors)
                data = {"form": form}
                return render(request, "seller_register.html", data)


def buyer_login(request):
    if request.method == "GET" and not request.session.get("is_login"):
        text, image = captcha.generate_captcha()
        number = 0
        while cache.has_key("k%d" % number):
            number += 1
        cache.set("k%d" % number, text, 3000)
        image = base64.b64encode(image).decode()
        data = {"k": number, "image": image}
        return render(request, "buyer_login.html", data)
    elif request.session.get("is_login"):
        raise Http404()
    else:
        form = Customer_loginForm(request.POST)
        k = "k" + request.POST.get("k")
        if not cache.has_key(k):
            return HttpResponse("<script>alert('?????????????????????');window.location.href='/buyer_login/';</script>")
        if form.is_valid():
            v_code = cache.get(k)
            if v_code != request.POST.get("verify_code").upper():
                cache.delete(k)
                return HttpResponse("<script>alert('??????????????????');window.location.href='/buyer_login/';</script>")
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
                    return HttpResponse("<script>alert('??????????????????');window.location.href='/buyer_login/';</script>")
            else:
                return HttpResponse("<script>alert('???????????????????????????');window.location.href='/buyer_login/';</script>")
        else:
            print(form.errors.as_json)
            data = {"form": form}
            return render(request, "buyer_login.html", data)


def seller_login(request):
    if request.method == "GET" and not request.session.get("is_login"):
        text, image = captcha.generate_captcha()
        number = 0
        while cache.has_key("k%d" % number):
            number += 1
        cache.set("k%d" % number, text, 3000)
        image = base64.b64encode(image).decode()
        data = {"k": number, "image": image}
        return render(request, "seller_login.html", data)
    elif request.session.get("is_login"):
        raise Http404()
    else:
        form = Seller_loginForm(request.POST)
        k = "k" + request.POST.get("k")
        if not cache.has_key(k):
            return HttpResponse("<script>alert('?????????????????????');window.location.href='/seller_login/';</script>")
        if form.is_valid():
            v_code = cache.get(k)
            if v_code != request.POST.get("verify_code").upper():
                cache.delete(k)
                return HttpResponse("<script>alert('??????????????????');window.location.href='/seller_login/';</script>")
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
                    return HttpResponse("<script>alert('??????????????????');window.location.href='/seller_login/';</script>")
            else:
                return HttpResponse("<script>alert('???????????????????????????');window.location.href='/seller_login/';</script>")
        else:
            print(form.errors.as_json)
            data = {"form": form}
            return render(request, "seller_login.html", data)


def customer_info(request):
    if request.method == "GET" and request.session.get("is_login") == 1:
        id = request.session.get("id")
        form = Customer.objects.filter(id=id).first()
        address_set = Address.objects.filter(customer_id=id)
        return render(request, "customer_info.html", {"form": form, "address_set": address_set})
    elif request.method == "POST" and request.session.get("is_login") == 1:
        name = request.POST.get('name')
        email = request.POST.get('email')
        sex = request.POST.get('sex')
        money = request.POST.get('money')
        avatar = request.FILES.get("avatar", None)
        if not 3 < len(name) < 12:
            return HttpResponse("<script>alert('??????????????????????????????');window.history.back(-1);</script>")
        if not email or (Customer.objects.filter(email=email) and Customer.objects.filter(email=email).first().id != request.session.get("id")):
            return HttpResponse("<script>alert('???????????????????????????');window.history.back(-1);</script>")
        if not sex or sex not in ['1', '2', '0']:
            return HttpResponse("<script>alert('?????????????????????????????????');window.history.back(-1);</script>")
        if not money or not is_number(money):
            return HttpResponse("<script>alert('?????????????????????????????????');window.history.back(-1);</script>")
        customer = Customer.objects.filter(id=request.session.get('id'))
        if avatar:
            img_list = avatar.name.split(".")
            if str(customer.first().avatar) != 'customer_avatar/default.jpg':
                os.remove(MEDIA_ROOT + '/' + str(customer.first().avatar))
            item_img = "customer_avatar/{}.{}".format(request.session.get("id"), img_list[1])
            i = 0
            while os.path.exists(MEDIA_ROOT + "/" + item_img):
                i += 1
                item_img = "customer_avatar/{}({}).{}".format(request.session.get("id"), i, img_list[1])
            default_storage.save(MEDIA_ROOT + "/" + item_img, ContentFile(avatar.read()))
            customer.update(name=name, email=email, sex=sex, avatar=item_img)
            return HttpResponse("<script>alert('????????????!');window.location.href='/customer_info/';</script>")

        customer.update(name=name, email=email, sex=sex, money=money)
        return HttpResponse("<script>alert('????????????!');window.location.href='/customer_info/';</script>")


def seller_info(request):
    if request.method == "GET" and request.session.get("is_login") == 2:
        form = Seller.objects.filter(id=request.session.get("id")).first()
        return render(request, "seller_info.html", {'form': form})
    elif request.method == "POST" and request.session.get("is_login") == 2:
        name = request.POST.get('name')
        email = request.POST.get('email')
        sex = request.POST.get('sex')
        avatar = request.FILES.get("avatar", None)
        if not 3 < len(name) < 12:
            return HttpResponse("<script>alert('??????????????????????????????');window.history.back(-1);</script>")
        if not email or (Seller.objects.filter(email=email) and Seller.objects.filter(email=email).first().id != request.session.get("id")):
            return HttpResponse("<script>alert('???????????????????????????');window.history.back(-1);</script>")
        if not sex or sex not in ['1', '2', '0']:
            return HttpResponse("<script>alert('?????????????????????????????????');window.history.back(-1);</script>")
        seller = Seller.objects.filter(id=request.session.get('id'))
        if avatar:
            img_list = avatar.name.split(".")
            if str(seller.first().avatar) != 'seller_avatar/default.jpg':
                os.remove(MEDIA_ROOT+'/'+ str(seller.first().avatar))
            item_img = "seller_avatar/{}.{}".format(request.session.get("id"), img_list[1])
            i = 0
            while os.path.exists(MEDIA_ROOT + "/" + item_img):
                i += 1
                item_img = "seller_avatar/{}({}).{}".format(request.session.get("id"), i, img_list[1])
            default_storage.save(MEDIA_ROOT + "/" + item_img, ContentFile(avatar.read()))
            seller.update(name=name, email=email, sex=sex,avatar=item_img)
            return HttpResponse("<script>alert('????????????!');window.location.href='/seller_info/';</script>")

        seller.update(name=name, email=email, sex=sex)
        return HttpResponse("<script>alert('????????????!');window.location.href='/seller_info/';</script>")


def good_info(request, id):
    if request.session.get("id") == 1:
        good = Goods.objects.filter(id=id, status=True).first()
        if not good:
            return HttpResponse("<script>alert('?????????????????????????????????');window.location.href='/index/';</script>")
        comments = Comment.objects.filter(item_id=id, status=True)
        customer = Customer.objects.filter(id=request.session.get("id")).first()
        return render(request, "good_info.html", {"good": good, "comment": comments, "customer": customer})
    else:
        good = Goods.objects.filter(id=id).first()
        if not good:
            return HttpResponse("<script>alert('?????????????????????');window.location.href='/index/';</script>")
        comments = Comment.objects.filter(item_id=id, status=True)
        return render(request, "good_info.html", {"good": good, "comment": comments, })


def logout(request):
    if request.session.get("is_login"):
        request.session.flush()
        return redirect('/index/')
    else:
        return HttpResponse("<script>alert('????????????!');window.location.href='/login/';</script>")


def create_good(request):
    if request.method == "GET" and request.session.get("is_login") == 2:
        return render(request, "create_good.html")
    elif request.method == "POST" and request.session.get("is_login") == 2:
        if request.POST.get("item_id") == '-1':
            image = request.FILES.get("item_img", None)
            item_name = request.POST.get("item_name")
            item_introdcution = request.POST.get("item_introduction")
            item_price = request.POST.get("item_price")
            number = request.POST.get("number")
            category_id = request.POST.get("category_id")
            if not item_name:
                return HttpResponse("<script>alert('??????????????????');window.history.back(-1)</script>")
            if not image:
                return HttpResponse("<script>alert('???????????????');window.history.back(-1)</script>")
            if not item_introdcution:
                return HttpResponse("<script>alert('????????????????????????');window.history.back(-1)</script>")
            if not category_id:
                return HttpResponse("<script>alert('????????????????????????');window.history.back(-1)</script>")
            if not item_price or not is_number(item_price.strip()):
                return HttpResponse("<script>alert('???????????????????????????');window.history.back(-1)</script>")
            if not number or not number.strip().isdecimal():
                return HttpResponse("<script>alert('??????????????????');window.history.back(-1)</script>")
            img_list = image.name.split(".")
            item_img = "item_img/{}.{}".format(request.session.get("id"), img_list[1])
            i = 0
            print(MEDIA_ROOT + "/" + item_img)
            while os.path.exists(MEDIA_ROOT + "/" + item_img):
                i += 1
                item_img = "item_img/{}({}).{}".format(request.session.get("id"), i, img_list[1])
            default_storage.save(MEDIA_ROOT + "/" + item_img, ContentFile(image.read()))

            Goods.objects.create(item_name=item_name, item_introduction=item_introdcution,
                                 seller_id=request.session.get("id"), item_price=item_price, item_img=item_img,
                                 number=number)
            return HttpResponse("<script>alert('?????????????????????');window.location.href='/index/'</script>")
        elif request.POST.get("item_id"):
            item_id = int(request.POST.get("item_id"))
            good = Goods.objects.filter(id=item_id, status=False)
            item_name = request.POST.get("item_name")
            number = request.POST.get("number")
            item_price = request.POST.get("item_price")
            item_img = request.POST.get("item_img")
            category_id = request.POST.get("category_id")
            item_introduction = request.POST.get("item_introduction")

            if not good:
                return HttpResponse("<script>alert('?????????????????????????????????');window.history.back(-1)</script>")
            if not request.POST.get("item_name"):
                return HttpResponse("<script>alert('?????????????????????');window.history.back(-1)</script>")
            if not request.POST.get("number") or not number.strip().isdecimal():
                return HttpResponse("<script>alert('???????????????????????????');window.history.back(-1)</script>")
            if not request.POST.get("item_price") or not is_number(item_price.strip()):
                return HttpResponse("<script>alert('???????????????????????????');window.history.back(-1)</script>")

            if not request.POST.get("item_img"):
                good.update(item_name=item_name, number=int(number), item_price=float(item_price),
                            category_id=int(category_id), item_introduction=item_introduction,
                            create_time=timezone.now())
                return HttpResponse("<script>alert('????????????');window.location.href='/deal_good/';</script>")
            if not request.POST.get("item_introduction"):
                good.update(item_name=item_name, number=int(number), item_price=float(item_price),
                            category_id=int(category_id), item_img=item_img, create_time=timezone.now())
                return HttpResponse("<script>alert('????????????');window.location.href='/deal_good/';</script>")
            good.update(item_name=item_name, number=int(number), item_price=float(item_price),
                        category_id=int(category_id), item_introduction=item_introduction, item_img=item_img,
                        create_time=timezone.now())
            return HttpResponse("<script>alert('????????????');window.location.href='/deal_good/';</script>")
        else:
            item_id = int(request.POST.get("id"))
            good = Goods.objects.filter(id=item_id).first()
            data = {"good": good}
            return render(request, "create_good.html", data)
    else:
        raise Http404()


def cart(request):
    if request.method == "GET" and request.session.get("is_login") == 1:
        order = Cart.objects.filter(buyer_id=request.session.get("id"), status=0)
        data = {"order": order}
        return render(request, "cart.html", data)
    elif request.method == "POST" and request.session.get("is_login") == 1:
        number = request.POST.get("number")
        item_id = request.POST.get("item_id")
        buyer_id = request.session.get("id")
        item = Goods.objects.filter(id=item_id).first()
        customer = Customer.objects.filter(id=buyer_id).first()
        if not number.isdigit() or number == "0":
            return HttpResponse("<script>alert('???????????????????????????');window.history.back(-1);</script>")
        elif int(number) > item.number:
            return HttpResponse("<script>alert('????????????');window.history.back(-1);</script>")
        price = int(number) * item.item_price
        Cart.objects.create(item=item, seller_id=item.seller_id, buyer_id=buyer_id, number=int(number),
                            sum_price=price, status=0)
        return HttpResponse("<script>alert('????????????????????????');window.location.href='/cart/'</script>")
    else:
        raise Http404()


def order(request):
    if request.method == "POST" and request.session.get("is_login") == 1:
        buy_id = request.session.get("id")
        customer = Customer.objects.filter(id=buy_id).first()
        if request.POST.getlist("item_id_set") and request.POST.get("status") == "1":
            item_id_set = list(map(int, request.POST.getlist("item_id_set")))
            item_set = Cart.objects.filter(id__in=item_id_set)
            data = {"item_set": item_set, "customer": customer}
            return render(request, "order.html", data)
        elif request.POST.get("status") == "1":
            return HttpResponse("<script>alert('???????????????????????????');window.history.back(-1);</script>")
        number = request.POST.get("number")
        item_id = request.POST.get("item_id")
        item = Goods.objects.filter(id=item_id).first()
        address = request.POST.getlist("address")
        if request.POST.get("status") == "0":
            if not Customer.objects.filter(id=request.session.get("id")).first().status:
                return HttpResponse("<script>alert('??????????????????????????????');window.history.back(-1);</script>")
            if not address:
                return HttpResponse("<script>alert('????????????????????????');window.history.back(-1);</script>")
            number = request.POST.getlist("number")
            item_id = request.POST.getlist("item_id")
            for i in range(len(item_id)):
                item = Goods.objects.filter(id=item_id[i]).first()
                Order.objects.create(number=int(number[i]), sum_price=int(number[i]) * item.item_price, buyer_id=buy_id,
                                     status=0,
                                     item_id=item_id[i], address=Address.objects.filter(id=address[i]).first().content)
                money = customer.money
                item.number -= int(number[i])
                customer.money -= int(number[i]) * item.item_price
                customer.save()
                item.save()
            Cart.objects.filter(item_id__in=item_id).update(status=1)
            return HttpResponse("<script>alert('????????????');window.location.href='/index/';</script>")

        else:
            if not number.isdigit() or number == "0":
                return HttpResponse("<script>alert('???????????????????????????');window.history.back(-1);</script>")
            if int(number) > item.number:
                return HttpResponse("<script>alert('????????????');window.history.back(-1);</script>")
            elif customer.money < int(number) * item.item_price:
                return HttpResponse("<script>alert('????????????');window.history.back(-1);</script>")
            price = int(number) * item.item_price
            data = {"item": item, "customer": customer, "number": number, "price": price}
            return render(request, "order.html", data)
    else:
        raise Http404()


def order_info(request):
    if request.method == "GET" and request.session.get("is_login") == 1:
        id = request.session.get("id")
        order = Customer.objects.filter(id=id).first().order_set.all()
        order_list1 = order.filter(status=0)
        order_list2 = order.filter(status=1)
        order_list3 = order.filter(status=3)
        order_list4 = order.filter(status__in=[2, 4])
        data = {"order": order, "order_list1": order_list1, "order_list2": order_list2, "order_list3": order_list3,
                "order_list4": order_list4, }
        return render(request, "order_info.html", data)
    elif request.method == "POST" and request.session.get("is_login") == 1:
        order_id = request.POST.get("id")
        Order.objects.filter(id=order_id).update(status=4)
        return HttpResponse("<script>alert('????????????');window.location.href='/order_info/';</script>")
    else:
        raise Http404()


def comment(request):
    if request.method == "POST" and request.session.get("is_login") == 1:
        content = request.POST.get("content")
        if not content:
            return HttpResponse("<script>alert('??????????????????');window.history.back(-1)</script>")
        if Comment.objects.filter(commenter_id=int(request.POST.get("id"))):
            return HttpResponse("<script>alert('?????????????????????????????????');window.history.back(-1)</script>")
        Comment.objects.create(content=content, commenter_id=int(request.session.get("id")),
                               item_id=int(request.POST.get("item_id")))
        return HttpResponse("<script>alert('????????????');window.location.href='/good_info/{}/'</script>".format(
            int(request.POST.get("item_id"))))
    else:
        return HttpResponse("<script>alert('?????????????????????');window.history.back(-1);</script>")


def address(request):
    address_id = request.POST.get("address_id")
    if request.method == "POST" and request.session.get("is_login") == 1:
        if address_id == '-1':  # ??????????????????
            address = request.POST.get("address")
            if address:
                customer = Customer.objects.filter(id=request.session.get("id")).first()
                if customer.address_set.filter(content=address):
                    return HttpResponse("<script>alert('?????????????????????');window.history.back(-1)</script>")
                else:
                    Address.objects.create(content=address, customer_id=request.session.get("id"))
                    return HttpResponse("<script>alert('??????????????????');window.location.href='/customer_info/'</script>")
            else:
                return HttpResponse("<script>alert('??????????????????');window.history.back(-1)</script>")
        elif request.POST.get("address"):
            Address.objects.filter(id=address_id).update(content=request.POST.get("address"))
            return HttpResponse("<script>alert('??????????????????');window.location.href='/customer_info/'</script>")
        else:
            id = request.session.get("id")
            form = Customer.objects.filter(id=id).first()
            address_set = Address.objects.filter(customer_id=id)
            return render(request, "customer_info.html", {"form": form, "address_set": address_set,
                                                          "address": Address.objects.filter(
                                                              id=request.POST.get("address_id")).first()})
    else:
        raise Http404()


def edit_password(request):
    if request.method == "GET":
        return render(request, "edit_password.html")
    else:
        if request.is_ajax():
            email = request.POST.get("email")
            if not request.POST.get('email'):
                return HttpResponse("??????????????????")
            if not Customer.objects.filter(email=email):
                return HttpResponse("?????????????????????")
            if cache.has_key("find" + email):
                return HttpResponse("????????????????????????1???????????????")
            verify_code = str(random.randint(1000, 10000))
            cache.set("find" + email, verify_code, 60)
            send_email(request.POST.get("email"), verify_code)
            return HttpResponse("????????????????????????")
        elif request.POST.get("password"):
            password = request.POST.get("password").strip()
            password2 = request.POST.get("password2").strip()
            customer = Customer.objects.filter(email=request.POST.get("email"))
            if password != password2:
                return HttpResponse("<script>alert('??????????????????????????????');window.history.back(-1);</script>")
            if len(password) < 6 or len(password2) < 6:
                return HttpResponse("<script>alert('????????????????????????');window.history.back(-1);</script>")
            if password == customer.first().password:
                return HttpResponse("<script>alert('???????????????????????????????????????');window.history.back(-1);</script>")
            customer.update(password=password)
            cache.delete("find" + request.POST.get("email"))
            return HttpResponse("<script>alert('????????????');window.location.href='/buyer_login/';</script>")
        else:
            if request.POST.get("check_number") == cache.get("find" + request.POST.get("email")):
                data = {"status": 1, "email": request.POST.get("email")}
                return render(request, "edit_password.html", data)
            elif not cache.get("find" + request.POST.get("email")):
                return HttpResponse("<script>alert('??????????????????');window.history.back(-1);</script>")
            else:
                return HttpResponse("<script>alert('??????????????????');window.history.back(-1);</script>")


def deal_order(request):
    if request.method == "GET" and request.session.get("is_login") == 2:
        order = Order.objects.filter(
            item_id__in=Seller.objects.filter(id=request.session.get("id")).first().goods_set.all())
        order_list1 = order.filter(status=0)
        order_list2 = order.filter(status=3)
        order_list3 = order.filter(status__in=[1, 2, 4])
        data = {"order_list1": order_list1, "order_list2": order_list2, "order_list3": order_list3}
        return render(request, "deal_order.html", data)
    elif request.method == "POST" and request.session.get("is_login") == 2:
        if not Seller.objects.filter(id=request.session.get("id")).first().status:
            return HttpResponse("<script>alert('???????????????????????????????????????');window.history.back(-1);</script>")
        order_id = int(request.POST.get("id"))
        order = Order.objects.filter(id=order_id).first()
        good = Goods.objects.filter(id=order.item_id).first()
        number = order.number
        if good.number < number:
            return HttpResponse("<script>alert('???????????????????????????');window.history.back(-1);</script>")
        good.number -= number
        good.save()
        Order.objects.filter(id=order_id).update(status=3)
        return HttpResponse("<script>alert('????????????');window.location.href='/deal_order/';</script>")


def reject_order(request):
    if request.method == "POST" and request.session.get("is_login") == 2:
        if not Seller.objects.filter(id=request.session.get("id")).first().status:
            return HttpResponse("<script>alert('???????????????,??????????????????');window.history.back(-1);</script>")
        item_id = int(request.POST.get("id"))
        order = Order.objects.filter(id=item_id)
        item = Goods.objects.filter(id=order.first().item_id)
        order.update(status=2)
        customer = Customer.objects.filter(id=order.first().buyer_id)
        money = customer.first().money
        money += order.first().sum_price
        number = item.first().number
        number += order.first().number
        customer.update(money=money)
        item.update(number=number)
        return HttpResponse("<script>alert('????????????');window.location.href='/deal_order/';</script>")
    else:
        raise Http404()


def delete_comment(request):
    if request.method == "POST" and request.session.get("is_login") == 1:
        comment = Comment.objects.filter(commenter_id=int(request.POST.get("id")),
                                         item_id=int(request.POST.get("item_id")), status=True)
        if not comment:
            return HttpResponse("<script>alert('??????????????????');window.history.back(-1);</script>")
        comment.update(status=False)
        return HttpResponse("<script>alert('??????????????????');window.location.href='/order_info/';</script>")
    elif request.method == "POST" and request.session.get("is_login") == 2:
        pass


def deal_comment(request):
    if request.method == "GET" and request.session.get("is_login") == 2:
        item_id = Goods.objects.filter(seller_id=request.session.get("id")).values_list('id', flat=True)
        comment = Comment.objects.filter(item_id__in=item_id, status=True)
        data = {"comment": comment}
        return render(request, "deal_comment.html", data)
    elif request.method == "POST" and request.session.get("is_login") == 2:
        content = request.POST.get("content")
        if not content:
            return HttpResponse("<script>alert('??????????????????');window.history.back(-1)</script>")
        if ReComment.objects.filter(commenter_id=int(request.POST.get("id"))):
            return HttpResponse("<script>alert('?????????????????????????????????');window.history.back(-1)</script>")
        ReComment.objects.create(content=content, commenter_id=int(request.POST.get("commenter_id")),
                                 comment_id=int(request.POST.get("id")))
        return HttpResponse("<script>alert('????????????');window.location.href='/good_info/{}/'</script>".format(
            int(request.POST.get("item_id"))))
    else:
        raise Http404()


def deal_good(request):
    if request.method == "GET" and request.session.get("is_login") == 2:
        good = Goods.objects.filter(seller_id=request.session.get("id"))
        data = {"good": good}
        return render(request, "deal_good.html", data)
    elif request.method == "POST" and request.session.get("is_login") == 2:
        item_id = int(request.POST.get("id"))
        good = Goods.objects.filter(id=item_id)
        status = good.first().status
        if not Seller.objects.filter(id=request.session.get("id")).first().status and not status:
            return HttpResponse("<script>alert('????????????????????????????????????');window.history.back(-1);</script>")
        good.update(status=bool(1 - status))
        return HttpResponse("<script>alert('???????????????');window.location.href='/deal_good/';</script>")
    else:
        raise Http404()


def search(request):
    if request.method == "GET":
        q = request.GET.get("q")
        if not q:
            return HttpResponse("<script>alert('????????????????????????');window.history.back(-1);</script>")
        good = Goods.objects.filter(item_name__icontains=q)
        data = {"good": good, "q": q, "number": len(good)}
        return render(request, "search.html", data)
    else:
        raise Http404()


def delete_good(request):
    if request.method == "POST" and request.session.get("is_login") == 2:
        item_id = request.POST.get("id")
        if not Goods.objects.filter(id=item_id):
            return HttpResponse("<script>alert('?????????????????????');window.history.back(-1);</script>")
        good = Goods.objects.filter(id=item_id).first()
        os.remove(MEDIA_ROOT + '/' + str(good.item_img))
        good.delete()
        return HttpResponse("<script>alert('????????????');window.location.href='/deal_good/';</script>")
