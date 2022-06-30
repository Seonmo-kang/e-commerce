from json import JSONDecodeError
from re import template
from tkinter import E
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.views.generic import FormView,ListView

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.account.views import LoginView as AccountLoginView
from .models import Profile
from .forms import LoginForm,UserRegisterationForm,MyCustomLoginForm

User = get_user_model()

BASE_URL = "http://localhost:8000/"
KAKAO_CALLBACK_URI = BASE_URL + "/accounts/kakao/callback"

def test(request):
    return HttpResponse("this is account")

# def registerPage(request):
#     form = UserRegisterationForm()
#     context ={}
#     if request.method == 'POST':
#         form = UserRegisterationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             context = {}
#     context = {'form': form}
#     return render(request, 'register.html',context)

# move the view from def to class.
class RegisterView(FormView):

    form_class = UserRegisterationForm
    template_name = 'account/register.html'
    success_url = '/shop/'

    #form_valid method is called when valid form data has been POSTed.
    #It should return an HttpResponse.
    # reutrn - redirect to get_success_url()
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def homepage(request):
    context={}
    return render(request, 'homepage.html',context)

@login_required
def mypage(request):
    """
    1. login required이 필요하다.
    1-2 로그인이 안되어 있을 시에 로그인 화면으로 redirect한다.
    2-1. 로그인 확인 후, 로그인한 사용자의 ID나 정보를 받는다.
    3. 사용자의 정보로 Profile의 값을 조회
    3-1 Profile의 값이 없을 경우 form을 전송.
    4. 값이 있을 경우 값 전송
    값 전송중 문제가 있을 경우 오류 전송
    """
    current_user_id = request.user.id
    print(current_user_id)
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile=None
    if profile is None:
        profile ='There is no  profile on this user'
    context={
        'profile':profile
    }
    return render(request, 'account_custom/profile.html', context)

class KakaoSignView(View):
    """
        Auth code request to Kakao auth server
    """
    def get(self,request):
        api_key = settings.KAKAO_KEY
        redirect_uri = KAKAO_CALLBACK_URI
        print(f'api_key is {api_key}')
        print(f'redirect_uri is {redirect_uri}')
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={api_key}&redirect_uri={redirect_uri}&response_type=code"
        )
"""
    # Redirect to kakao/login/callback
    # get authorization code
    # using code, request access token
    # using access token, get email.
    # using email, sign up or sign in
"""
class KakaoCallbackView(View):
    """
        Access Token Request
    """
    def get(self,request):
        api_key = settings.KAKAO_KEY
        redirect_uri = KAKAO_CALLBACK_URI
        code = request.GET.get("code")
        token_request = request.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={api_key}&redirect_uri={redirect_uri}&code={code}"
            ,header={'Accept':'application/json',
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'})
        token_response_json = token_request.json()
        error = token_response_json.get("error",None)
        #if there is an error form token_request
        if error is not None:
            raise JSONDecodeError(error)
        access_token = token_response_json.get('access_token')
        """
            Email Request
        """
        profile_request = request.get(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"}
            )
        profile_json = profile_request.json()
        kakao_account_json = profile_json.get('kakao_account') 
        email = kakao_account_json.get('email') # email
        """
        #     Sign up or Sign in Request
        """
        try:
            user = User.objects.get(email=email) # 기존 유저 검색
            # 기존에 가입된 유저의 Provider가 Kakao가 아니면 에러
            social_user = SocialAccount.objects.get(user=user)
            if social_user is None:
                return 'err_msg: email exists bun not social user'
            if social_user.provider != 'kakao':
                return 'err_msg: no matching social type.'
            
        except user.DoesNotExist:
            print('test')
            # 기존에 가입된 유저가 없으면 Sign up




# class KakaoLoginView(SocialLoginView):
#     adapter_class = kakao_view.KakaoOAuth2Adapter
#     client_class = OAuth2Client
#     callback_url = KAKAO_CALLBACK_URI




# Test login page with AuthenticationsForm
# def loginPage(request):
#     form = AuthenticationForm()
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid:
#             login(request, form.get_user())
#             return redirect('homepage')
#     context ={
#         'form':form
#     }
#     return render(request, 'login.html',context)


# def loginPage(request):
#     form = LoginForm()
#     context = {'form':form}
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid:
#             email = request.POST['email']
#             password = request.POST['password']
#             user = authenticate(request,email=email, password=password)
#             if user is not None:
#                 print("user is not None and login success")
#                 login(request, user)
#                 # Get Profile model related with Auth.User.
#                 # Put information in context and render to homepage.
#                 #Reference : https://runebook.dev/ko/docs/django/topics/auth/default
#                 #사용자를 로그인하는 방법
#                 # 인증 백엔드 선택부터 보기
#                 context = {'login':'Log in success'}
#                 return render(request, 'homepage.html', context)
#             else:
#                 return render(request,'login.html',context)
#     return render(request, 'login.html',context)
