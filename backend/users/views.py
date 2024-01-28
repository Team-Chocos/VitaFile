from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import views, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice
from django_otp.plugins.otp_static.models import StaticToken
from users import permissions as otp_permissions
from users.utils import get_custom_jwt
import uuid

User = get_user_model()
class TOTPDeleteView(views.APIView):
    """
    Use this endpoint to delete a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerified]

    def post(self, request, format=None):
        user = request.user
        devices = devices_for_user(user)
        for device in devices:
            device.delete()
        user.jwt_secret = uuid.uuid4()
        user.save()
        token = get_custom_jwt(user, None)
        return Response({'token': token}, status=status.HTTP_200_OK)

class StaticVerifyView(views.APIView):
    """
    Use this endpoint to verify a static token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, token, format=None):
        user = request.user
        device = get_user_static_device(self, user)
        if device is not None and device.verify_token(str.encode(token)):
            token = get_custom_jwt(user, device)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class StaticCreateView(APIView):
    """
    Use this endpoint to create static recovery codes.
    """
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerified]
    number_of_static_tokens = 6

    def get(self, request, format=None):
        device = get_user_static_device(self, request.user)
        if not device:
            device = StaticDevice.objects.create(user=request.user, name="Static")

        device.token_set.all().delete()
        tokens = []
        for n in range(self.number_of_static_tokens):
            token = StaticToken.random_token()
            device.token_set.create(token=token)
            tokens.append(token.decode('utf-8'))

        return Response(tokens, status=status.HTTP_201_CREATED)

def get_user_static_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, StaticDevice):
            return device

def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device

class TOTPCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]    
    
    def get(self, request, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)        

class TOTPVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]    
    
    def post(self, request, token, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device == None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            return Response(True, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CreateUserView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")
        email = request.data.get("username")
        dob = request.data.get("dob")  
        sex = request.data.get("sex")
        contact_no = request.data.get("contact_no")

        if not username or not password or not email:
            return Response(
                {"error": "Username, password and email are required to register a user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            return Response(
                {"error": "User with this username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_user = User.objects.create_user(
            username=username, password=password, first_name=firstname,  last_name=lastname, email=email, dob=dob, sex=sex, contact_no=contact_no
        )

        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class GetUserView(APIView):
    def get(self, request):
        user = request.user
        if user is None:
            return Response({"message": "You are not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            name = user.first_name + " " + user.last_name
            return Response(name, status=status.HTTP_200_OK)