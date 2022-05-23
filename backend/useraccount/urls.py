from unicodedata import name
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.test, name="index"),
    path('register/', views.RegisterView.as_view(), name= "register"),
    path('kakao/login',views.KakaoSignView.as_view(),name='kakao_logins'),
    path('kakao/login/callback',views.KakaoCallbackView.as_view(),name='Kakao_call_backs'),
    # path('kakao/login/finish',views.KakaoLoginView.as_view(),name='kakao_login_finish'),
    path('mypage/',views.mypage,name='mypage'),
]