from app1.models import Customer, Seller
from django import forms



class Customer_loginForm(forms.Form):
    name = forms.CharField(max_length=10, min_length=4,
                           error_messages={"max_length": "太长了", "min_length": "太短了", "required": "用户名不能为空", })
    password = forms.CharField(max_length=50, min_length=6,
                               error_messages={"max_length": "太长了", "min_length": "太短了", "required": "密码不能为空", })

    def clean(self):
        cleaned_data = super().clean()
        CHECK_LIST = "@#$%^&*()?\/"
        ret = 0
        name = cleaned_data.get("name")
        password = cleaned_data.get("password")
        print(cleaned_data)
        for i in CHECK_LIST:
            if name and name.isalnum() and i in name:
                ret = 1
                break
            elif password and i in password:
                ret = 2
                break
        if ret == 1:
            raise forms.ValidationError(u"账号中含非法字符", code='password_invalid')
        elif ret == 2:
            raise forms.ValidationError(u"密码中含非法字符", code='password_invalid')
        else:
            return cleaned_data




class Seller_loginForm(forms.Form):
    name = forms.CharField(max_length=10, min_length=4,
                           error_messages={"max_length": "太长了", "min_length": "太短了", "required": "用户名不能为空", })
    password = forms.CharField(max_length=50, min_length=6,
                               error_messages={"max_length": "太长了", "min_length": "太短了", "required": "密码不能为空", })

    def clean(self):
        cleaned_data = super().clean()
        CHECK_LIST = "@#$%^&*()?\/"
        ret = 0
        name = cleaned_data.get("name")
        password = cleaned_data.get("password")
        print(name, password)
        for i in CHECK_LIST:
            if name and name.isalnum() and i in name:
                ret = 1
                break
            elif password and i in password:
                ret = 2
                break
        if ret == 1:
            raise forms.ValidationError(u"账号中含非法字符", code='password_invalid')
        elif ret == 2:
            raise forms.ValidationError(u"密码中含非法字符", code='password_invalid')
        else:
            return cleaned_data


class Customer_registerForm(forms.Form):
    name = forms.CharField(max_length=10, min_length=4,
                           error_messages={"max_length": "太长了", "min_length": "太短了", "required": "用户名不能为空", })
    password = forms.CharField(max_length=50, min_length=6,
                               error_messages={"max_length": "太长了", "min_length": "太短了", "required": "密码不能为空", })
    password2 = forms.CharField(max_length=50, min_length=6,
                                error_messages={"max_length": "太长了", "min_length": "太短了", "required": "确认密码不能为空", })

    email = forms.EmailField(error_messages={"invalid":"请输入有效的邮箱地址！","required":"邮箱不能为空！"})

    def clean(self):
        cleaned_data = super().clean()
        CHECK_LIST = "@#$%^&*()?\/"
        ret = 0
        name = cleaned_data.get("name")
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password2 != password:
            ret = 3
        for i in CHECK_LIST:
            if name and name.isalnum() and i in name:
                ret = 1
                break
            elif (password and i in password) or (password2 and i in password2):
                ret = 2
                break
        if ret == 1:
            raise forms.ValidationError(u"账号中含非法字符", code='name_invalid')
        elif ret == 2:
            raise forms.ValidationError(u"密码中含非法字符", code='password_invalid')
        elif ret == 3:
            raise forms.ValidationError(u"两次输入密码不同，请检查", code='password_invalid')
        else:
            return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册', code="email_invalid")
        else:
            return email

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Customer.objects.filter(name=name).exists():
            raise forms.ValidationError('该用户名已被注册', code="name_invalid")
        else:
            return name

class Seller_registerForm(forms.Form):
    name = forms.CharField(max_length=10, min_length=4,
                           error_messages={"max_length": "太长了", "min_length": "太短了", "required": "用户名不能为空", })
    password = forms.CharField(max_length=50, min_length=6,
                               error_messages={"max_length": "太长了", "min_length": "太短了", "required": "密码不能为空", })
    password2 = forms.CharField(max_length=50, min_length=6,
                                error_messages={"max_length": "太长了", "min_length": "太短了", "required": "确认密码不能为空", })

    email = forms.EmailField(error_messages={"invalid":"请输入有效的邮箱地址！","required":"邮箱不能为空！"})

    def clean(self):
        cleaned_data = super().clean()
        CHECK_LIST = "@#$%^&*()?\/"
        ret = 0
        name = cleaned_data.get("name")
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password2 != password:
            ret = 3
        for i in CHECK_LIST:
            if name and not name.isalnum() and i in name:
                ret = 1
                break
            elif (password and i in password) or (password2 and i in password2):
                ret = 2
                break

        if ret == 1:
            raise forms.ValidationError(u"账号中含非法字符", code='name_invalid')
        elif ret == 2:
            raise forms.ValidationError(u"密码中含非法字符", code='password_invalid')
        elif ret == 3:
            raise forms.ValidationError(u"两次输入密码不同，请检查", code='password_invalid')
        else:
            return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Seller.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册', code="email_invalid")
        else:
            return email

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Seller.objects.filter(name=name).exists():
            raise forms.ValidationError('该用户名已被注册', code="name_invalid")
        else:
            return name



