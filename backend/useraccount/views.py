from re import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

from django.views.generic import FormView

from .models import User, UserManager, Profile
from .forms import LoginForm,UserRegisterationForm

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

class loginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = '/shop/'

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log him in.
        """
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

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


