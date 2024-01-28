
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

def get_custom_jwt(user, device):
    """
    Helper to generate a JWT for a validated OTP device.
    This resets the orig_iat timestamp, as we've re-validated the user.
    """
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_otp_payload(user, device)
    return jwt_encode_handler(payload)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        if user.totpdevice_set.exists():
            device = user.totpdevice_set.first()
            token['otp'] = device.bin_key

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def otp_is_verified(self, request):
    """
    Helper to determine if user has verified OTP.
    """
    auth = JWTAuthentication()
    header = auth.get_header(request)

    if header is None:
        return False

    raw_token = auth.get_raw_token(header)

    if raw_token is None:
        return False

    try:
        UntypedToken(raw_token)
    except (InvalidToken, TokenError):
        return False

    payload = UntypedToken(raw_token).payload
    otp_device_id = payload.get('otp_device_id')

    if otp_device_id:
        device = TOTPDevice.objects.filter(id=otp_device_id).first()

        if (device is not None) and (device.user_id != request.user.id):
            return False
        else:
            # Valid device in JWT
            return True
    else:
        return False
