import json
import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User


@api_view(["POST"])
@permission_classes([AllowAny])
def create(request):
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name')

    if not User.objects.filter(username=email).exists():
        user = User.objects.create_user(
            username=email,
            first_name=name,
            password=password
        )

        headers = {
            "Content-Type": "application/json"
        }

        # data = f'"username":"{email}","password":"{password}"'
        # final_data = "{" + data + "}"

        data = {
            "username":email,
            "password":password
        }

        protocol = "http://"

        if request.is_secure():
            protocol = "https://"
        
        host = request.get_host()

        url = protocol + host + "/api/v1/auth/token/"

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_data = {
                "status_code": 6000,
                "data": response.json(),
                "message": "User created successfully",
            }
        else:
            response_data = {
                "status_code": 6001,
                "message": "Failed to create user",
            }
    else:
        response_data = {
            "status_code": 6001,
            "data": "This account already exists",
        }

    return Response(response_data)
