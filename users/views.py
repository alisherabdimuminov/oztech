import datetime
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import random
from django.shortcuts import redirect, render
from django.http import HttpRequest
from rest_framework import decorators
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db.models import Sum

from courses.models import Rating, Course, Lesson
from courses.serializers import RatingSerializer

from .models import User, Contact, VerificationCode, Date
from .serializers import UserSerializer


configuration = sib_api_v3_sdk.Configuration()

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
headers = {"Some-Custom-Name":"i-med-team-unique-id"}

@decorators.api_view(http_method_names=["POST"])
def login(request: HttpRequest):
    username = request.data.get("email")
    password = request.data.get("password")
    user = User.objects.filter(username=username)
    if not user:
        return Response({
            "status": "error",
            "code": "404",
            "data": {
                "error": "Foydalanuvchi topilmadi",
            },
        })
    user = user.first()

    if not user.is_active:
        return Response({
            "status": "error",
            "code": "402",
            "data": None
        })

    if not user.check_password(password):
        return Response({
            "status": "error",
            "code": "400",
            "data": {
                "error": "Parol xato",
            }
        })

    tokens = Token.objects.filter(user=user)
    tokens.delete()

    token = Token.objects.get_or_create(user=user)
    return Response({
        "status": "success",
        "code": "200",
        "data": {
            "token": token[0].key
        }
    })


@decorators.api_view(http_method_names=["POST"])
def signup(request: HttpRequest):
    print(request.method)
    username = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    middle_name = request.data.get("middle_name")
    city = request.data.get("city")
    town = request.data.get("town")
    profession = request.data.get("profession")
    password = request.data.get("password")

    user = User.objects.filter(username=username)
    if user:
        return Response({
            "status": "error",
            "code": "400",
            "data": {
                "error": "Bu email allaqachon ro'yxatdan o'tgan"
            }
        })
    
    user = User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        city=city,
        town=town,
        profession=profession,
    )
    user.set_password(password)
    user.save()
    code = VerificationCode.objects.create(user=user, code=random.randint(1000, 9999))
    code.save()

    html_content = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">
<head>
<title></title>
<meta charset="UTF-8" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<!--[if !mso]>-->
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<!--<![endif]-->
<meta name="x-apple-disable-message-reformatting" content="" />
<meta content="target-densitydpi=device-dpi" name="viewport" />
<meta content="true" name="HandheldFriendly" />
<meta content="width=device-width" name="viewport" />
<meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no" />
<style type="text/css">
table {
border-collapse: separate;
table-layout: fixed;
mso-table-lspace: 0pt;
mso-table-rspace: 0pt
}
table td {
border-collapse: collapse
}
.ExternalClass {
width: 100%
}
.ExternalClass,
.ExternalClass p,
.ExternalClass span,
.ExternalClass font,
.ExternalClass td,
.ExternalClass div {
line-height: 100%
}
body, a, li, p, h1, h2, h3 {
-ms-text-size-adjust: 100%;
-webkit-text-size-adjust: 100%;
}
html {
-webkit-text-size-adjust: none !important
}
body, #innerTable {
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale
}
#innerTable img+div {
display: none;
display: none !important
}
img {
Margin: 0;
padding: 0;
-ms-interpolation-mode: bicubic
}
h1, h2, h3, p, a {
line-height: inherit;
overflow-wrap: normal;
white-space: normal;
word-break: break-word
}
a {
text-decoration: none
}
h1, h2, h3, p {
min-width: 100%!important;
width: 100%!important;
max-width: 100%!important;
display: inline-block!important;
border: 0;
padding: 0;
margin: 0
}
a[x-apple-data-detectors] {
color: inherit !important;
text-decoration: none !important;
font-size: inherit !important;
font-family: inherit !important;
font-weight: inherit !important;
line-height: inherit !important
}
u + #body a {
color: inherit;
text-decoration: none;
font-size: inherit;
font-family: inherit;
font-weight: inherit;
line-height: inherit;
}
a[href^="mailto"],
a[href^="tel"],
a[href^="sms"] {
color: inherit;
text-decoration: none
}
</style>
<style type="text/css">
@media (min-width: 481px) {
.hd { display: none!important }
}
</style>
<style type="text/css">
@media (max-width: 480px) {
.hm { display: none!important }
}
</style>
<style type="text/css">
@media (max-width: 480px) {
.t29,.t34{mso-line-height-alt:0px!important;line-height:0!important;display:none!important}.t30{padding-top:43px!important}.t32{border:0!important;border-radius:0!important}.t27,.t9{width:320px!important}.t24{mso-line-height-alt:26px!important;line-height:26px!important}
}
</style>
<!--[if !mso]>-->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&amp;family=Albert+Sans:wght@500&amp;display=swap" rel="stylesheet" type="text/css" />
<!--<![endif]-->
<!--[if mso]>
<xml>
<o:OfficeDocumentSettings>
<o:AllowPNG/>
<o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings>
</xml>
<![endif]-->
</head>
<body id="body" class="t37" style="min-width:100%;Margin:0px;padding:0px;background-color:#F9F9F9;"><div class="t36" style="background-color:#F9F9F9;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td class="t35" style="font-size:0;line-height:0;mso-line-height-rule:exactly;background-color:#F9F9F9;background-image:none;background-repeat:repeat;background-size:auto;background-position:center top;" valign="top" align="center">
<!--[if mso]>
<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false">
<v:fill color="#F9F9F9"/>
</v:background>
<![endif]-->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" align="center" id="innerTable"><tr><td><div class="t29" style="mso-line-height-rule:exactly;mso-line-height-alt:70px;line-height:70px;font-size:1px;display:block;">&nbsp;&nbsp;</div></td></tr><tr><td align="center">
<table class="t33" role="presentation" cellpadding="0" cellspacing="0" style="Margin-left:auto;Margin-right:auto;"><tr>
<!--[if mso]>
<td width="400" class="t32" style="background-color:#FFFFFF;border:1px solid #CECECE;overflow:hidden;width:400px;border-radius:20px 20px 20px 20px;">
<![endif]-->
<!--[if !mso]>-->
<td class="t32" style="background-color:#FFFFFF;border:1px solid #CECECE;overflow:hidden;width:400px;border-radius:20px 20px 20px 20px;">
<!--<![endif]-->
<table class="t31" role="presentation" cellpadding="0" cellspacing="0" width="100%" style="width:100%;"><tr><td class="t30" style="padding:50px 40px 40px 40px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="width:100% !important;"><tr><td align="center">
<table class="t4" role="presentation" cellpadding="0" cellspacing="0" style="Margin-left:auto;Margin-right:auto;"><tr>
<!--[if mso]>
<td width="60" class="t3" style="width:60px;">
<![endif]-->
<!--[if !mso]>-->
<td class="t3" style="width:60px;">
<!--<![endif]-->
<table class="t2" role="presentation" cellpadding="0" cellspacing="0" width="100%" style="width:100%;"><tr><td class="t1"><a href="#" style="font-size:0px;" target="_blank"><img class="t0" style="display:block;border:0;height:auto;width:100%;Margin:0;max-width:100%;" width="60" height="60" alt="" src="https://4afeeb38-d624-4e69-a402-728d1e75b07e.b-cdn.net/e/ea5a0626-fa24-4976-9af0-68cc1940d537/fad37d1a-100d-4cb9-b93c-e41db2e4d942.png"/></a></td></tr></table>
</td></tr></table>
</td></tr><tr><td><div class="t5" style="mso-line-height-rule:exactly;mso-line-height-alt:40px;line-height:40px;font-size:1px;display:block;">&nbsp;&nbsp;</div></td></tr><tr><td align="center">
<table class="t10" role="presentation" cellpadding="0" cellspacing="0" style="Margin-left:auto;Margin-right:auto;"><tr>
<!--[if mso]>
<td width="318" class="t9" style="width:318px;">
<![endif]-->
<!--[if !mso]>-->
<td class="t9" style="width:318px;">
<!--<![endif]-->
<table class="t8" role="presentation" cellpadding="0" cellspacing="0" width="100%" style="width:100%;"><tr><td class="t7"><h1 class="t6" style="margin:0;Margin:0;font-family:Inter,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:28px;font-weight:600;font-style:normal;font-size:24px;text-decoration:none;text-transform:none;letter-spacing:-1.2px;direction:ltr;color:#111111;text-align:center;mso-line-height-rule:exactly;mso-text-raise:1px;">Emailingizni tasdiqlang 😀</h1></td></tr></table>
</td></tr></table>
</td></tr><tr><td><div class="t12" style="mso-line-height-rule:exactly;mso-line-height-alt:17px;line-height:17px;font-size:1px;display:block;">&nbsp;&nbsp;</div></td></tr><tr><td align="center">
<table class="t16" role="presentation" cellpadding="0" cellspacing="0" style="Margin-left:auto;Margin-right:auto;"><tr>
<!--[if mso]>
<td width="308" class="t15" style="width:308px;">
<![endif]-->
<!--[if !mso]>-->
<td class="t15" style="width:308px;">
<!--<![endif]-->
<table class="t14" role="presentation" cellpadding="0" cellspacing="0" width="100%" style="width:100%;"><tr><td class="t13"><p class="t11" style="margin:0;Margin:0;font-family:Inter,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:22px;font-weight:500;font-style:normal;font-size:15px;text-decoration:none;text-transform:none;letter-spacing:-0.6px;direction:ltr;color:#424040;text-align:center;mso-line-height-rule:exactly;mso-text-raise:2px;">Kodni IMedTeam ilovasi orqali tasdiqlang.</p></td></tr></table>
</td></tr></table>
</td></tr><tr><td><div class="t18" style="mso-line-height-rule:exactly;mso-line-height-alt:40px;line-height:40px;font-size:1px;display:block;">&nbsp;&nbsp;</div></td></tr><tr><td align="center">
<table class="t22" role="presentation" cellpadding="0" cellspacing="0" style="Margin-left:auto;Margin-right:auto;"><tr>
<!--[if mso]>
<td width="154" class="t21" style="background-color:#0057FF;overflow:hidden;width:154px;border-radius:8px 8px 8px 8px;">
<![endif]-->
<!--[if !mso]>-->
<td class="t21" style="background-color:#0057FF;overflow:hidden;width:154px;border-radius:8px 8px 8px 8px;">
<!--<![endif]-->
<table class="t20" role="presentation" cellpadding="0" cellspacing="0" width="100%" style="width:100%;"><tr><td class="t19" style="text-align:center;line-height:40px;mso-line-height-rule:exactly;mso-text-raise:8px;"><a class="t17" href="#" style="display:block;margin:0;Margin:0;font-family:Inter,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:40px;font-weight:700;font-style:normal;font-size:15px;text-decoration:none;letter-spacing:-0.5px;direction:ltr;color:#FFFFFF;text-align:center;mso-line-height-rule:exactly;mso-text-raise:8px;" target="_blank">""" + str(code.code) + """</a></td></tr></table>
</td></tr></table>
</td></tr><tr><td><div class="t24" style="mso-line-height-rule:exactly;mso-line-height-alt:30px;line-height:30px;font-size:1px;display:block;">&nbsp;&nbsp;</div></td></tr><tr><td align="center">
<table class="t28" role="presentation" cellpadding="0" cellspacing="0" style="Margin-left:auto;Margin-right:auto;"><tr>
<!--[if mso]>
<td width="318" class="t27" style="background-color:#F2EFF3;overflow:hidden;width:318px;border-radius:8px 8px 8px 8px;">
<![endif]-->
<!--[if !mso]>-->
<td class="t27" style="background-color:#F2EFF3;overflow:hidden;width:318px;border-radius:8px 8px 8px 8px;">
<!--<![endif]-->
<table class="t26" role="presentation" cellpadding="0" cellspacing="0" width="100%" style="width:100%;"><tr><td class="t25" style="padding:20px 30px 20px 30px;"><p class="t23" style="margin:0;Margin:0;font-family:Albert Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:18px;font-weight:500;font-style:normal;font-size:12px;text-decoration:none;text-transform:none;direction:ltr;color:#84828E;text-align:center;mso-line-height-rule:exactly;mso-text-raise:2px;">IMedTeam - 2025</p></td></tr></table>
</td></tr></table>
</td></tr></table></td></tr></table>
</td></tr></table>
</td></tr><tr><td><div class="t34" style="mso-line-height-rule:exactly;mso-line-height-alt:70px;line-height:70px;font-size:1px;display:block;">&nbsp;&nbsp;</div></td></tr></table></td></tr></table></div><div class="gmail-fix" style="display: none; white-space: nowrap; font: 15px courier; line-height: 0;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div></body>
</html>
"""
    sender = { "name": "IMedTeam", "email": "alisher.abdimuminov.2005@gmail.com" }
    to = [ { "name": "StudentX", "email": "lbek458@gmail.com" } ]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject="Emailingizni tasdiqlang")

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        print(response)
    except:
        print("dont send")

    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
def verify_code(request: HttpRequest):
    c = request.data.get("code")
    username = request.data.get("email")
    code = VerificationCode.objects.filter(user__username=username)
    if code:
        code = code.last()
        if int(code.code) == int(c):
            code.user.is_active = True
            code.user.save()
            return Response({
                "status": "success",
                "code": "200",
                "data": None
            })
        else:
            return Response({
                "status": "error",
                "code": "404",
                "data": None
            })
    else:
        return Response({
            "status": "success",
            "code": "400",
            "data": None
        })


@decorators.api_view(http_method_names=["POST"])
def generate_code(request: HttpRequest):
    username = request.data.get("email")
    user = User.objects.get(username=username)
    code = VerificationCode.objects.create(user=user, code=random.randint(1000, 9999))
    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
def change_password(requset: HttpRequest):
    user = requset.user
    username = requset.data.get("email")
    password = requset.data.get("password")
    if user.is_authenticated:
        user.set_password(password)
        user.save()
        return Response({
            "status": "success",
            "code": "200",
            "data": None
        })
    else:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return Response({
            "status": "success",
            "code": "200",
            "data": None
        })


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def profile(request: HttpRequest):
    user: User = request.user
    rating_obj = Rating.objects.filter(user=user)
    rating = RatingSerializer(rating_obj, many=True)
    lessons = Lesson.objects.filter(finishers=user).aggregate(**{ "duration": Sum("duration") })
    print(lessons)

    image = user.image
    
    if image:
        image = request.build_absolute_uri(image.url)
    else:
        image = None

    return Response({
        "status": "success",
        "code": "200",
        "data": {
            "email": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "middle_name": user.middle_name,
            "duration": lessons.get("duration"),
            "city": user.city,
            "town": user.town,
            "image": image,
            "rating": rating.data,
        }
    })


@decorators.api_view(http_method_names=["POST"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def edit_profile(request: HttpRequest):
    user_obj = request.user
    user = UserSerializer(user_obj, data=request.data)
    if user.is_valid():
        user.save()
        return Response({
            "status": "success",
            "code": "200",
            "data": None
        })
    else:
        return Response({
            "status": "error",
            "code": "400",
            "data": {
                "error": "Majburiy maydonlarni to'ldiring"
            }
        })


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def contact(request: HttpRequest):
    contact = Contact.objects.first()
    if contact:
        return Response({
            "status": "success",
            "code": "200",
            "data": {
                "name": contact.name,
                "phone": contact.phone,
                "telegram": contact.telegram,
            }
        })
    else:
        return Response({
            "status": "success",
            "code": "200",
            "data": {
                "name": "OzTech",
                "phone": "",
                "telegram": "",
            }
        })


def index(request: HttpRequest):
    if request.method == "POST":
        course = Course.objects.get(pk=request.POST.get("course"))
        user = User.objects.get(pk=request.POST.get("student"))
        time = request.POST.get("time")
        date = Date.objects.filter(user=user, course=course)
        if not date:
            if time == "month":
                course.students_month.add(user)
                date = Date.objects.create(user=user, course=course, ended=datetime.datetime.now() + datetime.timedelta(days=182))
                date.save()
            else:
                course.students_year.add(user)
                date = Date.objects.create(user=user, course=course, ended=datetime.datetime.now() + datetime.timedelta(days=365))
                date.save()
        course.save()
        print(user)
    user = request.user
    if user.is_anonymous:
        return redirect("admin:login")
    courses = Course.objects.all()
    users = User.objects.all()
    return render(request, "index.html", { "courses": courses, "users": users })
