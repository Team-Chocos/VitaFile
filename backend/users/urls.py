from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('getuser/', GetUserView.as_view(), name='getuser'),
    re_path(r'^totp/create/$', views.TOTPCreateView.as_view(), name='totp-create'),
    re_path(r'^totp/login/(?P<token>[0-9]{6})/$', TOTPVerifyView.as_view(), name='totp-login'),
    re_path(r'^static/create/$', StaticCreateView.as_view(), name='static-create'),
    re_path(r'^static/login/(?P<token>[a-z2-9]{7,8})/$', StaticVerifyView.as_view(), name='static-login'),
]