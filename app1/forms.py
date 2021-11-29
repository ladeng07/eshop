from app1.models import Customer, Seller
from django import forms


class Customer_loginForm(forms.Form):
    name = forms.CharField(max_length=10, min_length=4,
                               error_messages={"max_length": "太长了", "min_length": "太短了", "required": "用户名不能为空",})
    password = forms.CharField(max_length=50, min_length=6, error_messages={"max_length": "太长了", "min_length": "太短了", "required": "密码不能为空",})

    def clean(self):
        cleaned_data = super().clean()
        CHECK_LIST = "@#$%^&*()?\/"
        ret=0
        name = cleaned_data.get("name")
        password = cleaned_data.get("password")
        print(name,password)
        for i in CHECK_LIST:
            if name and i in name:
                ret=1
                break
            elif password and i in password:
                ret=2
                break
        if ret == 1:
            raise forms.ValidationError(u"账号中含非法字符",code='password_invalid')
        elif ret == 2:
            raise forms.ValidationError(u"密码中含非法字符",code='password_invalid')
        else:
            return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Customer.objects.filter(name=name).exists():
            raise forms.ValidationError('该用户名已被注册',code="name_invalid")
        else:
            return name

class Seller_loginForm(forms.Form):
    name = forms.CharField(max_length=10, min_length=4,
                               error_messages={"max_length": "太长了", "min_length": "太短了", "required": "用户名不能为空",})
    password = forms.CharField(max_length=50, min_length=6, error_messages={"max_length": "太长了", "min_length": "太短了", "required": "密码不能为空",})

    def clean(self):
        cleaned_data = super().clean()
        CHECK_LIST = "@#$%^&*()?\/"
        ret=0
        name = cleaned_data.get("name")
        password = cleaned_data.get("password")
        print(name,password)
        for i in CHECK_LIST:
            if name and i in name:
                ret=1
                break
            elif password and i in password:
                ret=2
                break
        if ret == 1:
            raise forms.ValidationError(u"账号中含非法字符",code='password_invalid')
        elif ret == 2:
            raise forms.ValidationError(u"密码中含非法字符",code='password_invalid')
        else:
            return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Seller.objects.filter(name=name).exists():
            raise forms.ValidationError('该用户名已被注册',code="name_invalid")
        else:
            return name


