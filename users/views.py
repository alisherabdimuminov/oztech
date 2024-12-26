from django.http import HttpRequest
from rest_framework import decorators
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer

from .models import User


@decorators.api_view(http_method_names=["POST"])
def login(request: HttpRequest):
    username = request.data.get("phone")
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

    if not user.check_password(password):
        return Response({
            "status": "error",
            "code": "400",
            "data": {
                "error": "Parol xato",
            }
        })
    
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
    username = request.data.get("phone")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    middle_name = request.data.get("middle_name")
    city = request.data.get("city")
    town = request.data.get("town")
    password = request.data.get("password")

    user = User.objects.filter(username=username)
    if user:
        return Response({
            "status": "error",
            "code": "400",
            "data": {
                "error": "Bu raqam allaqachon ro'yxatdan o'tgan"
            }
        })
    
    user = User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        city=city,
        town=town,
    )
    user.set_password(password)
    user.save()
    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })

@decorators.api_view(http_method_names=["POST"])
def edit_profile(request: HttpRequest, pk: int):
    user_obj = User.objects.get(pk=pk)
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
