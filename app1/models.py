from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.


class Customer(models.Model):
    SEX_LIST = ((0, "男"), (1, "女"), (2, "其他"),)
    name = models.CharField(max_length=10, verbose_name="用户名")
    password = models.CharField(max_length=28, verbose_name="密码")
    email = models.EmailField(max_length=50, verbose_name="邮箱", unique=True)
    money = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="余额", default=0)
    sex = models.IntegerField(choices=SEX_LIST, verbose_name="性别", null=True, blank=True)
    avatar = models.ImageField(upload_to="user_avatar/", verbose_name="头像", default="customer_avatar/default.jpg")
    register_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    goods = models.ManyToManyField(to="Goods", through="Order")
    status = models.BooleanField(default=True, verbose_name="账户状态")


class Cart(models.Model):
    status_choice = ((0, "未下单"), (1, "已下单"))
    item = models.ForeignKey("Goods", on_delete=models.CASCADE, verbose_name="商品ID")
    seller_id = models.IntegerField(verbose_name="卖家ID")
    buyer_id = models.IntegerField(verbose_name="买家ID")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    number = models.IntegerField(default=0, verbose_name="数量")
    sum_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0, null=True, blank=True,
                                    verbose_name="总价")
    status = models.IntegerField(default=0, verbose_name="状态", choices=status_choice)  # 0是未下单，1是已下单


class Order(models.Model):
    status_choice = ((0, "下单未处理"), (1, "接受"), (2, "不接受"), (3, "运输中"), (4, "已收货"))
    item = models.ForeignKey(to="Goods", verbose_name="商品ID", on_delete=models.CASCADE)
    buyer = models.ForeignKey(to="Customer", verbose_name="买家ID", on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    number = models.IntegerField(default=0, verbose_name="数量")
    address = models.TextField(max_length=200, verbose_name="地址")
    sum_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0, null=True, blank=True,
                                    verbose_name="订单价格")
    status = models.IntegerField(choices=status_choice, default=0,
                                 verbose_name="订单状态")  # 0是下单未处理 1是接受 2是不接受 3是运输中 4是已收货


class Goods(models.Model):
    categories = ((0, "无分类"), (1, "生活用品"), (2, "体育用品"), (3, "学习用品"), (4, "小吃零食"), (5, "服装"), (6, "电子产品"))
    item_img = models.ImageField(upload_to="item_img/", null=True, blank=True, verbose_name="商品图片",
                                 default="item_img/default.jpg")
    item_name = models.CharField(max_length=100, default="NULL", null=True, blank=True, verbose_name="商品名")
    item_introduction = RichTextUploadingField(default="这是一个商品的介绍需要十五个字", verbose_name="商品介绍")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    seller = models.ForeignKey("Seller", on_delete=models.CASCADE, verbose_name="卖家ID")
    number = models.IntegerField(default=0, null=True, blank=True, verbose_name="库存")
    item_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0, null=True, blank=True,
                                     verbose_name="价格")
    category_id = models.IntegerField(choices=categories, default=0, verbose_name="商品分类")
    status = models.BooleanField(default=True, verbose_name="商品状态")


class Comment(models.Model):
    item_id = models.IntegerField(verbose_name="商品ID")
    commenter_id = models.IntegerField(verbose_name="评论者ID")
    content = models.TextField(max_length=1000, verbose_name="评论内容")
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    status = models.BooleanField(default=True, verbose_name="评论状态")


class Seller(models.Model):
    SEX_LIST = ((0, "男"), (1, "女"), (2, "其他"),)
    name = models.CharField(max_length=10, verbose_name="卖家昵称")
    password = models.CharField(max_length=28, verbose_name="密码")
    email = models.EmailField(max_length=50, verbose_name="邮箱", unique=True)
    register_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="注册时间")
    avatar = models.ImageField(upload_to="seller_avatar/", verbose_name="头像", default="seller_avatar/default.jpg")
    sex = models.IntegerField(choices=SEX_LIST,verbose_name="性别", default=0)
    status = models.BooleanField(default=True, verbose_name="账户状态")


class ReComment(models.Model):
    commenter_id = models.IntegerField(verbose_name="回复者ID")
    content = models.TextField(max_length=1000, verbose_name="回复内容")
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    status = models.BooleanField(default=True, verbose_name="状态")
    comment = models.OneToOneField('Comment', verbose_name="回复ID", on_delete=models.CASCADE, default=-1)


class Address(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, verbose_name="用户ID")
    content = models.TextField(max_length=200, verbose_name="地址")
